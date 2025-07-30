"""
Real-time Analytics Dashboard for WebInfo Retriever
Provides a web-based interface for monitoring performance and analytics.
"""

import json
import asyncio
from datetime import datetime, timedelta
from typing import Dict, Any, List
from pathlib import Path

try:
    from flask import Flask, render_template, jsonify, request, send_from_directory
    from flask_socketio import SocketIO, emit
    FLASK_AVAILABLE = True
except ImportError:
    FLASK_AVAILABLE = False
    print("Flask not available. Install with: pip install flask flask-socketio")

from ..core.analytics_engine import analytics_engine
from ..core.smart_cache import smart_cache
from ..api.client import WebInfoRetriever


class DashboardApp:
    """Real-time analytics dashboard application."""
    
    def __init__(self, host: str = "localhost", port: int = 5000):
        if not FLASK_AVAILABLE:
            raise ImportError("Flask is required for dashboard. Install with: pip install flask flask-socketio")
        
        self.host = host
        self.port = port
        self.app = Flask(__name__, 
                        template_folder=str(Path(__file__).parent / "templates"),
                        static_folder=str(Path(__file__).parent / "static"))
        self.app.config['SECRET_KEY'] = 'webinfo-retriever-dashboard'
        self.socketio = SocketIO(self.app, cors_allowed_origins="*")
        
        self.client = WebInfoRetriever()
        self.setup_routes()
        self.setup_socketio()
    
    def setup_routes(self):
        """Setup Flask routes."""
        
        @self.app.route('/')
        def dashboard():
            """Main dashboard page."""
            return render_template('dashboard.html')
        
        @self.app.route('/api/stats')
        def get_stats():
            """Get current performance statistics."""
            stats = analytics_engine.get_performance_stats()
            cache_stats = smart_cache.get_stats()
            
            return jsonify({
                'performance': {
                    'total_searches': stats.total_searches,
                    'avg_response_time': round(stats.avg_response_time, 2),
                    'success_rate': round(stats.success_rate, 1),
                    'avg_confidence': round(stats.avg_confidence, 1),
                    'sources_processed': stats.total_sources_processed,
                    'error_rate': round(stats.error_rate, 1),
                    'uptime_hours': round(stats.uptime / 3600, 1)
                },
                'cache': {
                    'entries': cache_stats['memory_entries'],
                    'size_mb': round(cache_stats['memory_size_mb'], 2),
                    'hit_rate': round(cache_stats['hit_rate'], 1),
                    'total_hits': cache_stats['total_hits'],
                    'total_misses': cache_stats['total_misses']
                },
                'timestamp': datetime.now().isoformat()
            })
        
        @self.app.route('/api/trends')
        def get_trends():
            """Get search trends data."""
            trends = analytics_engine.get_search_trends(hours=24)
            return jsonify(trends)
        
        @self.app.route('/api/errors')
        def get_errors():
            """Get error analysis."""
            errors = analytics_engine.get_error_analysis()
            return jsonify(errors)
        
        @self.app.route('/api/recent-searches')
        def get_recent_searches():
            """Get recent search history."""
            recent = list(analytics_engine.search_history)[-20:]  # Last 20 searches
            
            search_data = []
            for search in recent:
                search_data.append({
                    'query': search.query,
                    'search_type': search.search_type,
                    'duration': round(search.duration, 2),
                    'success_rate': round(search.success_rate * 100, 1),
                    'confidence': round(search.confidence_score * 100, 1),
                    'sources': search.sources_processed,
                    'timestamp': search.timestamp
                })
            
            return jsonify(search_data)
        
        @self.app.route('/api/search', methods=['POST'])
        def perform_search():
            """Perform a search via API."""
            data = request.get_json()
            query = data.get('query', '')
            search_type = data.get('type', 'fast')
            
            if not query:
                return jsonify({'error': 'Query is required'}), 400
            
            try:
                if search_type == 'ultra-fast':
                    response = asyncio.run(self.client.fast_comprehensive_search(
                        query=query,
                        num_sources=5,
                        answer_type="comprehensive"
                    ))
                elif search_type == 'fast':
                    response = asyncio.run(self.client.fast_search(
                        user_query=query,
                        num_results=3
                    ))
                else:
                    response = self.client.retrieve_and_summarize(query)
                
                return jsonify({
                    'success': True,
                    'response': response[:500] + "..." if len(str(response)) > 500 else str(response)
                })
            
            except Exception as e:
                return jsonify({
                    'success': False,
                    'error': str(e)
                }), 500
        
        @self.app.route('/api/clear-cache', methods=['POST'])
        def clear_cache():
            """Clear the cache."""
            smart_cache.clear()
            return jsonify({'success': True, 'message': 'Cache cleared'})
        
        @self.app.route('/api/export-analytics')
        def export_analytics():
            """Export analytics data."""
            filename = f"analytics_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            analytics_engine.export_analytics(filename)
            
            return send_from_directory('.', filename, as_attachment=True)
    
    def setup_socketio(self):
        """Setup SocketIO events for real-time updates."""
        
        @self.socketio.on('connect')
        def handle_connect():
            """Handle client connection."""
            print(f"Client connected: {request.sid}")
            emit('connected', {'message': 'Connected to WebInfo Retriever Dashboard'})
        
        @self.socketio.on('disconnect')
        def handle_disconnect():
            """Handle client disconnection."""
            print(f"Client disconnected: {request.sid}")
        
        @self.socketio.on('request_stats')
        def handle_stats_request():
            """Handle stats request."""
            stats = analytics_engine.get_performance_stats()
            cache_stats = smart_cache.get_stats()
            
            emit('stats_update', {
                'performance': {
                    'total_searches': stats.total_searches,
                    'avg_response_time': round(stats.avg_response_time, 2),
                    'success_rate': round(stats.success_rate, 1),
                    'active_searches': analytics_engine.current_metrics['active_searches']
                },
                'cache': {
                    'hit_rate': round(cache_stats['hit_rate'], 1),
                    'entries': cache_stats['memory_entries']
                }
            })
    
    def broadcast_search_update(self, search_data: Dict[str, Any]):
        """Broadcast search update to all connected clients."""
        if hasattr(self, 'socketio'):
            self.socketio.emit('search_update', search_data)
    
    def start_background_updates(self):
        """Start background task for real-time updates."""
        def background_task():
            while True:
                try:
                    # Get current stats
                    stats = analytics_engine.get_performance_stats()
                    cache_stats = smart_cache.get_stats()
                    
                    # Broadcast to all clients
                    self.socketio.emit('stats_update', {
                        'performance': {
                            'total_searches': stats.total_searches,
                            'avg_response_time': round(stats.avg_response_time, 2),
                            'success_rate': round(stats.success_rate, 1),
                            'active_searches': analytics_engine.current_metrics['active_searches']
                        },
                        'cache': {
                            'hit_rate': round(cache_stats['hit_rate'], 1),
                            'entries': cache_stats['memory_entries']
                        },
                        'timestamp': datetime.now().isoformat()
                    })
                    
                    self.socketio.sleep(5)  # Update every 5 seconds
                
                except Exception as e:
                    print(f"Background update error: {e}")
                    self.socketio.sleep(10)
        
        self.socketio.start_background_task(background_task)
    
    def run(self, debug: bool = False):
        """Run the dashboard application."""
        print(f"🚀 Starting WebInfo Retriever Dashboard")
        print(f"📊 Dashboard URL: http://{self.host}:{self.port}")
        print(f"📈 Real-time analytics and monitoring")
        
        # Start background updates
        self.start_background_updates()
        
        # Run the app
        self.socketio.run(
            self.app,
            host=self.host,
            port=self.port,
            debug=debug,
            allow_unsafe_werkzeug=True
        )


def create_dashboard_templates():
    """Create dashboard HTML templates."""
    templates_dir = Path(__file__).parent / "templates"
    templates_dir.mkdir(exist_ok=True)
    
    # Main dashboard template
    dashboard_html = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>WebInfo Retriever Dashboard</title>
    <script src="https://cdn.socket.io/4.0.0/socket.io.min.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <style>
        body { font-family: Arial, sans-serif; margin: 0; padding: 20px; background: #f5f5f5; }
        .header { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 20px; border-radius: 10px; margin-bottom: 20px; }
        .stats-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 20px; margin-bottom: 20px; }
        .stat-card { background: white; padding: 20px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }
        .stat-value { font-size: 2em; font-weight: bold; color: #667eea; }
        .stat-label { color: #666; margin-top: 5px; }
        .chart-container { background: white; padding: 20px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); margin-bottom: 20px; }
        .search-box { background: white; padding: 20px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); margin-bottom: 20px; }
        .search-input { width: 70%; padding: 10px; border: 1px solid #ddd; border-radius: 5px; }
        .search-btn { padding: 10px 20px; background: #667eea; color: white; border: none; border-radius: 5px; cursor: pointer; margin-left: 10px; }
        .recent-searches { background: white; padding: 20px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }
        .search-item { padding: 10px; border-bottom: 1px solid #eee; }
        .status-indicator { display: inline-block; width: 10px; height: 10px; border-radius: 50%; margin-right: 10px; }
        .status-online { background: #28a745; }
        .status-offline { background: #dc3545; }
    </style>
</head>
<body>
    <div class="header">
        <h1>🚀 WebInfo Retriever Dashboard</h1>
        <p>Real-time Analytics & Monitoring</p>
        <span class="status-indicator status-online" id="connectionStatus"></span>
        <span id="connectionText">Connected</span>
    </div>

    <div class="stats-grid">
        <div class="stat-card">
            <div class="stat-value" id="totalSearches">0</div>
            <div class="stat-label">Total Searches</div>
        </div>
        <div class="stat-card">
            <div class="stat-value" id="avgResponseTime">0s</div>
            <div class="stat-label">Avg Response Time</div>
        </div>
        <div class="stat-card">
            <div class="stat-value" id="successRate">0%</div>
            <div class="stat-label">Success Rate</div>
        </div>
        <div class="stat-card">
            <div class="stat-value" id="cacheHitRate">0%</div>
            <div class="stat-label">Cache Hit Rate</div>
        </div>
    </div>

    <div class="search-box">
        <h3>🔍 Test Search</h3>
        <input type="text" id="searchInput" class="search-input" placeholder="Enter your search query...">
        <button class="search-btn" onclick="performSearch()">Search</button>
        <button class="search-btn" onclick="clearCache()">Clear Cache</button>
        <div id="searchResult" style="margin-top: 15px; padding: 10px; background: #f8f9fa; border-radius: 5px; display: none;"></div>
    </div>

    <div class="chart-container">
        <h3>📈 Performance Trends</h3>
        <canvas id="performanceChart" width="400" height="200"></canvas>
    </div>

    <div class="recent-searches">
        <h3>📋 Recent Searches</h3>
        <div id="recentSearchesList"></div>
    </div>

    <script>
        const socket = io();
        let performanceChart;

        // Initialize chart
        const ctx = document.getElementById('performanceChart').getContext('2d');
        performanceChart = new Chart(ctx, {
            type: 'line',
            data: {
                labels: [],
                datasets: [{
                    label: 'Response Time (s)',
                    data: [],
                    borderColor: '#667eea',
                    backgroundColor: 'rgba(102, 126, 234, 0.1)',
                    tension: 0.4
                }]
            },
            options: {
                responsive: true,
                scales: {
                    y: { beginAtZero: true }
                }
            }
        });

        // Socket events
        socket.on('connect', function() {
            document.getElementById('connectionStatus').className = 'status-indicator status-online';
            document.getElementById('connectionText').textContent = 'Connected';
            socket.emit('request_stats');
        });

        socket.on('disconnect', function() {
            document.getElementById('connectionStatus').className = 'status-indicator status-offline';
            document.getElementById('connectionText').textContent = 'Disconnected';
        });

        socket.on('stats_update', function(data) {
            updateStats(data);
        });

        function updateStats(data) {
            document.getElementById('totalSearches').textContent = data.performance.total_searches;
            document.getElementById('avgResponseTime').textContent = data.performance.avg_response_time + 's';
            document.getElementById('successRate').textContent = data.performance.success_rate + '%';
            document.getElementById('cacheHitRate').textContent = data.cache.hit_rate + '%';

            // Update chart
            const now = new Date().toLocaleTimeString();
            performanceChart.data.labels.push(now);
            performanceChart.data.datasets[0].data.push(data.performance.avg_response_time);
            
            if (performanceChart.data.labels.length > 20) {
                performanceChart.data.labels.shift();
                performanceChart.data.datasets[0].data.shift();
            }
            
            performanceChart.update();
        }

        function performSearch() {
            const query = document.getElementById('searchInput').value;
            if (!query) return;

            const resultDiv = document.getElementById('searchResult');
            resultDiv.style.display = 'block';
            resultDiv.innerHTML = '🔍 Searching...';

            fetch('/api/search', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ query: query, type: 'fast' })
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    resultDiv.innerHTML = `✅ <strong>Result:</strong><br>${data.response}`;
                } else {
                    resultDiv.innerHTML = `❌ <strong>Error:</strong> ${data.error}`;
                }
            })
            .catch(error => {
                resultDiv.innerHTML = `❌ <strong>Error:</strong> ${error}`;
            });
        }

        function clearCache() {
            fetch('/api/clear-cache', { method: 'POST' })
            .then(response => response.json())
            .then(data => {
                alert('✅ Cache cleared successfully!');
            })
            .catch(error => {
                alert('❌ Error clearing cache: ' + error);
            });
        }

        // Load recent searches
        function loadRecentSearches() {
            fetch('/api/recent-searches')
            .then(response => response.json())
            .then(data => {
                const list = document.getElementById('recentSearchesList');
                list.innerHTML = '';
                
                data.forEach(search => {
                    const item = document.createElement('div');
                    item.className = 'search-item';
                    item.innerHTML = `
                        <strong>${search.query}</strong> 
                        <span style="color: #666;">(${search.search_type})</span><br>
                        <small>
                            Duration: ${search.duration}s | 
                            Success: ${search.success_rate}% | 
                            Confidence: ${search.confidence}% |
                            ${new Date(search.timestamp).toLocaleString()}
                        </small>
                    `;
                    list.appendChild(item);
                });
            });
        }

        // Load initial data
        loadRecentSearches();
        setInterval(loadRecentSearches, 30000); // Refresh every 30 seconds
    </script>
</body>
</html>
    """
    
    with open(templates_dir / "dashboard.html", "w", encoding="utf-8") as f:
        f.write(dashboard_html)


# Global dashboard instance
dashboard_app = None

def start_dashboard(host: str = "localhost", port: int = 5000, debug: bool = False):
    """Start the analytics dashboard."""
    global dashboard_app
    
    if not FLASK_AVAILABLE:
        print("❌ Flask not available. Install with: pip install flask flask-socketio")
        return
    
    # Create templates
    create_dashboard_templates()
    
    # Create and start dashboard
    dashboard_app = DashboardApp(host, port)
    dashboard_app.run(debug=debug)


if __name__ == "__main__":
    start_dashboard(debug=True)
