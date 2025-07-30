"""
Advanced Analytics Engine for WebInfo Retriever
Provides real-time monitoring, performance metrics, and usage analytics.
"""

import time
import json
import asyncio
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, asdict
from collections import defaultdict, deque
import threading
from pathlib import Path


@dataclass
class SearchMetrics:
    """Metrics for a single search operation."""
    query: str
    search_type: str  # ultra-fast, comprehensive, fast
    start_time: float
    end_time: float
    duration: float
    sources_found: int
    sources_processed: int
    success_rate: float
    confidence_score: float
    error_count: int
    api_calls: int
    cache_hits: int
    timestamp: str


@dataclass
class PerformanceStats:
    """Overall performance statistics."""
    total_searches: int
    avg_response_time: float
    success_rate: float
    avg_confidence: float
    total_sources_processed: int
    cache_hit_rate: float
    error_rate: float
    peak_concurrent_searches: int
    uptime: float


class AnalyticsEngine:
    """Advanced analytics engine for monitoring and optimization."""
    
    def __init__(self, max_history: int = 10000):
        self.max_history = max_history
        self.search_history: deque = deque(maxlen=max_history)
        self.active_searches: Dict[str, Dict] = {}
        self.performance_cache = {}
        self.error_log: deque = deque(maxlen=1000)
        
        # Real-time metrics
        self.current_metrics = {
            'active_searches': 0,
            'total_searches': 0,
            'avg_response_time': 0.0,
            'success_rate': 100.0,
            'cache_hit_rate': 0.0,
            'error_rate': 0.0
        }
        
        # Performance tracking
        self.response_times: deque = deque(maxlen=1000)
        self.success_count = 0
        self.error_count = 0
        self.cache_hits = 0
        self.cache_misses = 0
        
        # Thread safety
        self.lock = threading.Lock()
        
        # Start background analytics
        self.start_time = time.time()
        self._start_background_analytics()
    
    def start_search(self, search_id: str, query: str, search_type: str) -> None:
        """Start tracking a new search operation."""
        with self.lock:
            self.active_searches[search_id] = {
                'query': query,
                'search_type': search_type,
                'start_time': time.time(),
                'sources_found': 0,
                'sources_processed': 0,
                'api_calls': 0,
                'cache_hits': 0,
                'errors': []
            }
            self.current_metrics['active_searches'] = len(self.active_searches)
    
    def update_search_progress(self, search_id: str, **kwargs) -> None:
        """Update progress for an active search."""
        with self.lock:
            if search_id in self.active_searches:
                self.active_searches[search_id].update(kwargs)
    
    def complete_search(self, search_id: str, success: bool, 
                       confidence_score: float = 0.0) -> SearchMetrics:
        """Complete a search and record metrics."""
        with self.lock:
            if search_id not in self.active_searches:
                return None
            
            search_data = self.active_searches.pop(search_id)
            end_time = time.time()
            duration = end_time - search_data['start_time']
            
            # Calculate success rate
            success_rate = 1.0 if success else 0.0
            if search_data['sources_found'] > 0:
                success_rate = search_data['sources_processed'] / search_data['sources_found']
            
            # Create metrics object
            metrics = SearchMetrics(
                query=search_data['query'],
                search_type=search_data['search_type'],
                start_time=search_data['start_time'],
                end_time=end_time,
                duration=duration,
                sources_found=search_data['sources_found'],
                sources_processed=search_data['sources_processed'],
                success_rate=success_rate,
                confidence_score=confidence_score,
                error_count=len(search_data['errors']),
                api_calls=search_data['api_calls'],
                cache_hits=search_data['cache_hits'],
                timestamp=datetime.now().isoformat()
            )
            
            # Add to history
            self.search_history.append(metrics)
            
            # Update real-time metrics
            self._update_real_time_metrics(metrics, success)
            
            # Update active searches count
            self.current_metrics['active_searches'] = len(self.active_searches)
            
            return metrics
    
    def record_error(self, search_id: str, error: Exception, context: str = "") -> None:
        """Record an error for analytics."""
        with self.lock:
            error_data = {
                'search_id': search_id,
                'error_type': type(error).__name__,
                'error_message': str(error),
                'context': context,
                'timestamp': datetime.now().isoformat()
            }
            
            self.error_log.append(error_data)
            self.error_count += 1
            
            # Update search if active
            if search_id in self.active_searches:
                self.active_searches[search_id]['errors'].append(error_data)
    
    def record_cache_hit(self, search_id: str) -> None:
        """Record a cache hit."""
        with self.lock:
            self.cache_hits += 1
            if search_id in self.active_searches:
                self.active_searches[search_id]['cache_hits'] += 1
    
    def record_cache_miss(self, search_id: str) -> None:
        """Record a cache miss."""
        with self.lock:
            self.cache_misses += 1
    
    def get_performance_stats(self) -> PerformanceStats:
        """Get current performance statistics."""
        with self.lock:
            total_searches = len(self.search_history)
            
            if total_searches == 0:
                return PerformanceStats(
                    total_searches=0,
                    avg_response_time=0.0,
                    success_rate=100.0,
                    avg_confidence=0.0,
                    total_sources_processed=0,
                    cache_hit_rate=0.0,
                    error_rate=0.0,
                    peak_concurrent_searches=0,
                    uptime=time.time() - self.start_time
                )
            
            # Calculate averages
            avg_response_time = sum(m.duration for m in self.search_history) / total_searches
            avg_confidence = sum(m.confidence_score for m in self.search_history) / total_searches
            total_sources = sum(m.sources_processed for m in self.search_history)
            
            # Calculate rates
            total_cache_operations = self.cache_hits + self.cache_misses
            cache_hit_rate = (self.cache_hits / total_cache_operations * 100) if total_cache_operations > 0 else 0
            
            success_rate = (self.success_count / total_searches * 100) if total_searches > 0 else 100
            error_rate = (self.error_count / total_searches * 100) if total_searches > 0 else 0
            
            return PerformanceStats(
                total_searches=total_searches,
                avg_response_time=avg_response_time,
                success_rate=success_rate,
                avg_confidence=avg_confidence,
                total_sources_processed=total_sources,
                cache_hit_rate=cache_hit_rate,
                error_rate=error_rate,
                peak_concurrent_searches=max(len(self.active_searches), 
                                           self.current_metrics.get('peak_concurrent', 0)),
                uptime=time.time() - self.start_time
            )
    
    def get_search_trends(self, hours: int = 24) -> Dict[str, Any]:
        """Get search trends for the specified time period."""
        cutoff_time = datetime.now() - timedelta(hours=hours)
        
        recent_searches = [
            m for m in self.search_history 
            if datetime.fromisoformat(m.timestamp) > cutoff_time
        ]
        
        if not recent_searches:
            return {'total': 0, 'trends': {}}
        
        # Group by hour
        hourly_counts = defaultdict(int)
        search_types = defaultdict(int)
        avg_confidence_by_hour = defaultdict(list)
        
        for search in recent_searches:
            hour = datetime.fromisoformat(search.timestamp).hour
            hourly_counts[hour] += 1
            search_types[search.search_type] += 1
            avg_confidence_by_hour[hour].append(search.confidence_score)
        
        # Calculate hourly averages
        hourly_confidence = {
            hour: sum(scores) / len(scores) if scores else 0
            for hour, scores in avg_confidence_by_hour.items()
        }
        
        return {
            'total': len(recent_searches),
            'hourly_distribution': dict(hourly_counts),
            'search_type_distribution': dict(search_types),
            'hourly_confidence': hourly_confidence,
            'peak_hour': max(hourly_counts.items(), key=lambda x: x[1])[0] if hourly_counts else 0
        }
    
    def get_error_analysis(self) -> Dict[str, Any]:
        """Get error analysis and patterns."""
        if not self.error_log:
            return {'total_errors': 0, 'error_types': {}, 'recent_errors': []}
        
        error_types = defaultdict(int)
        recent_errors = list(self.error_log)[-10:]  # Last 10 errors
        
        for error in self.error_log:
            error_types[error['error_type']] += 1
        
        return {
            'total_errors': len(self.error_log),
            'error_types': dict(error_types),
            'recent_errors': recent_errors,
            'error_rate': (len(self.error_log) / max(len(self.search_history), 1)) * 100
        }
    
    def export_analytics(self, filepath: str) -> None:
        """Export analytics data to JSON file."""
        analytics_data = {
            'performance_stats': asdict(self.get_performance_stats()),
            'search_history': [asdict(m) for m in list(self.search_history)],
            'search_trends': self.get_search_trends(),
            'error_analysis': self.get_error_analysis(),
            'export_timestamp': datetime.now().isoformat()
        }
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(analytics_data, f, indent=2, ensure_ascii=False)
    
    def _update_real_time_metrics(self, metrics: SearchMetrics, success: bool) -> None:
        """Update real-time metrics."""
        self.response_times.append(metrics.duration)
        
        if success:
            self.success_count += 1
        
        # Update averages
        total_searches = len(self.search_history)
        self.current_metrics.update({
            'total_searches': total_searches,
            'avg_response_time': sum(self.response_times) / len(self.response_times),
            'success_rate': (self.success_count / total_searches * 100) if total_searches > 0 else 100,
            'cache_hit_rate': (self.cache_hits / max(self.cache_hits + self.cache_misses, 1)) * 100,
            'error_rate': (self.error_count / total_searches * 100) if total_searches > 0 else 0
        })
    
    def _start_background_analytics(self) -> None:
        """Start background analytics processing."""
        def background_worker():
            while True:
                try:
                    # Clean old data periodically
                    self._cleanup_old_data()
                    time.sleep(300)  # Run every 5 minutes
                except Exception as e:
                    print(f"Background analytics error: {e}")
                    time.sleep(60)
        
        thread = threading.Thread(target=background_worker, daemon=True)
        thread.start()
    
    def _cleanup_old_data(self) -> None:
        """Clean up old analytics data."""
        # This is handled by deque maxlen, but we can add more cleanup logic here
        pass


# Global analytics instance
analytics_engine = AnalyticsEngine()
