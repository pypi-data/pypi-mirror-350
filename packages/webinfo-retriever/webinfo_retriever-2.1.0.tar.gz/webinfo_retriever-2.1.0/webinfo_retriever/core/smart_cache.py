"""
Advanced Smart Caching System for WebInfo Retriever
Provides intelligent caching with TTL, LRU eviction, and semantic similarity.
"""

import time
import json
import hashlib
import pickle
from datetime import datetime, timedelta
from typing import Dict, Any, Optional, List, Tuple
from dataclasses import dataclass, asdict
from pathlib import Path
import threading
from collections import OrderedDict
import sqlite3


@dataclass
class CacheEntry:
    """Cache entry with metadata."""
    key: str
    value: Any
    created_at: float
    last_accessed: float
    access_count: int
    ttl: float
    size_bytes: int
    query_hash: str
    similarity_vector: Optional[List[float]] = None


class SmartCache:
    """Advanced caching system with multiple eviction strategies."""
    
    def __init__(self, 
                 max_size_mb: int = 100,
                 default_ttl: int = 3600,
                 enable_persistence: bool = True,
                 cache_dir: str = "cache"):
        
        self.max_size_bytes = max_size_mb * 1024 * 1024
        self.default_ttl = default_ttl
        self.enable_persistence = enable_persistence
        self.cache_dir = Path(cache_dir)
        
        # In-memory cache
        self.cache: OrderedDict[str, CacheEntry] = OrderedDict()
        self.current_size = 0
        
        # Statistics
        self.stats = {
            'hits': 0,
            'misses': 0,
            'evictions': 0,
            'size_evictions': 0,
            'ttl_evictions': 0
        }
        
        # Thread safety
        self.lock = threading.RLock()
        
        # Initialize persistence
        if self.enable_persistence:
            self._init_persistence()
        
        # Start background cleanup
        self._start_cleanup_thread()
    
    def _init_persistence(self) -> None:
        """Initialize persistent cache storage."""
        self.cache_dir.mkdir(exist_ok=True)
        self.db_path = self.cache_dir / "cache.db"
        
        with sqlite3.connect(str(self.db_path)) as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS cache_entries (
                    key TEXT PRIMARY KEY,
                    value BLOB,
                    created_at REAL,
                    last_accessed REAL,
                    access_count INTEGER,
                    ttl REAL,
                    size_bytes INTEGER,
                    query_hash TEXT
                )
            """)
            conn.execute("""
                CREATE INDEX IF NOT EXISTS idx_last_accessed 
                ON cache_entries(last_accessed)
            """)
            conn.execute("""
                CREATE INDEX IF NOT EXISTS idx_query_hash 
                ON cache_entries(query_hash)
            """)
    
    def _generate_key(self, query: str, params: Dict[str, Any] = None) -> str:
        """Generate cache key from query and parameters."""
        if params is None:
            params = {}
        
        # Create deterministic key
        key_data = {
            'query': query.lower().strip(),
            'params': sorted(params.items()) if params else []
        }
        
        key_string = json.dumps(key_data, sort_keys=True)
        return hashlib.sha256(key_string.encode()).hexdigest()
    
    def _generate_query_hash(self, query: str) -> str:
        """Generate hash for semantic similarity matching."""
        # Simple hash for now, could be enhanced with embeddings
        return hashlib.md5(query.lower().strip().encode()).hexdigest()
    
    def _calculate_size(self, value: Any) -> int:
        """Calculate approximate size of value in bytes."""
        try:
            return len(pickle.dumps(value))
        except:
            return len(str(value).encode('utf-8'))
    
    def get(self, query: str, params: Dict[str, Any] = None) -> Optional[Any]:
        """Get value from cache."""
        key = self._generate_key(query, params)
        
        with self.lock:
            # Check in-memory cache first
            if key in self.cache:
                entry = self.cache[key]
                
                # Check TTL
                if time.time() - entry.created_at > entry.ttl:
                    self._remove_entry(key)
                    self.stats['ttl_evictions'] += 1
                    self.stats['misses'] += 1
                    return None
                
                # Update access info
                entry.last_accessed = time.time()
                entry.access_count += 1
                
                # Move to end (LRU)
                self.cache.move_to_end(key)
                
                self.stats['hits'] += 1
                return entry.value
            
            # Check persistent cache
            if self.enable_persistence:
                value = self._get_from_persistent(key)
                if value is not None:
                    # Load back to memory if space allows
                    self._add_to_memory(key, value, query, params)
                    self.stats['hits'] += 1
                    return value
            
            self.stats['misses'] += 1
            return None
    
    def put(self, query: str, value: Any, params: Dict[str, Any] = None, 
            ttl: Optional[int] = None) -> None:
        """Put value in cache."""
        key = self._generate_key(query, params)
        ttl = ttl or self.default_ttl
        
        with self.lock:
            # Calculate size
            size_bytes = self._calculate_size(value)
            
            # Check if value is too large
            if size_bytes > self.max_size_bytes * 0.5:  # Don't cache if > 50% of max size
                return
            
            # Create cache entry
            entry = CacheEntry(
                key=key,
                value=value,
                created_at=time.time(),
                last_accessed=time.time(),
                access_count=1,
                ttl=ttl,
                size_bytes=size_bytes,
                query_hash=self._generate_query_hash(query)
            )
            
            # Add to memory cache
            self._add_to_memory_entry(entry)
            
            # Add to persistent cache
            if self.enable_persistence:
                self._add_to_persistent(entry)
    
    def _add_to_memory(self, key: str, value: Any, query: str, 
                      params: Dict[str, Any] = None) -> None:
        """Add entry to memory cache."""
        entry = CacheEntry(
            key=key,
            value=value,
            created_at=time.time(),
            last_accessed=time.time(),
            access_count=1,
            ttl=self.default_ttl,
            size_bytes=self._calculate_size(value),
            query_hash=self._generate_query_hash(query)
        )
        self._add_to_memory_entry(entry)
    
    def _add_to_memory_entry(self, entry: CacheEntry) -> None:
        """Add cache entry to memory."""
        # Remove existing entry if present
        if entry.key in self.cache:
            old_entry = self.cache[entry.key]
            self.current_size -= old_entry.size_bytes
            del self.cache[entry.key]
        
        # Ensure we have space
        while (self.current_size + entry.size_bytes > self.max_size_bytes and 
               len(self.cache) > 0):
            self._evict_lru()
        
        # Add new entry
        self.cache[entry.key] = entry
        self.current_size += entry.size_bytes
    
    def _evict_lru(self) -> None:
        """Evict least recently used entry."""
        if not self.cache:
            return
        
        # Get LRU entry (first in OrderedDict)
        key, entry = self.cache.popitem(last=False)
        self.current_size -= entry.size_bytes
        self.stats['evictions'] += 1
        self.stats['size_evictions'] += 1
    
    def _remove_entry(self, key: str) -> None:
        """Remove entry from memory cache."""
        if key in self.cache:
            entry = self.cache[key]
            self.current_size -= entry.size_bytes
            del self.cache[key]
    
    def _get_from_persistent(self, key: str) -> Optional[Any]:
        """Get value from persistent cache."""
        try:
            with sqlite3.connect(str(self.db_path)) as conn:
                cursor = conn.execute(
                    "SELECT value, created_at, ttl FROM cache_entries WHERE key = ?",
                    (key,)
                )
                row = cursor.fetchone()
                
                if row is None:
                    return None
                
                value_blob, created_at, ttl = row
                
                # Check TTL
                if time.time() - created_at > ttl:
                    # Remove expired entry
                    conn.execute("DELETE FROM cache_entries WHERE key = ?", (key,))
                    return None
                
                # Update access time
                conn.execute(
                    "UPDATE cache_entries SET last_accessed = ?, access_count = access_count + 1 WHERE key = ?",
                    (time.time(), key)
                )
                
                return pickle.loads(value_blob)
        
        except Exception as e:
            print(f"Error reading from persistent cache: {e}")
            return None
    
    def _add_to_persistent(self, entry: CacheEntry) -> None:
        """Add entry to persistent cache."""
        try:
            with sqlite3.connect(str(self.db_path)) as conn:
                value_blob = pickle.dumps(entry.value)
                
                conn.execute("""
                    INSERT OR REPLACE INTO cache_entries 
                    (key, value, created_at, last_accessed, access_count, ttl, size_bytes, query_hash)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    entry.key, value_blob, entry.created_at, entry.last_accessed,
                    entry.access_count, entry.ttl, entry.size_bytes, entry.query_hash
                ))
        
        except Exception as e:
            print(f"Error writing to persistent cache: {e}")
    
    def find_similar(self, query: str, threshold: float = 0.8) -> List[Tuple[str, Any, float]]:
        """Find similar cached queries (simple implementation)."""
        query_words = set(query.lower().split())
        results = []
        
        with self.lock:
            for entry in self.cache.values():
                # Simple word-based similarity
                cached_words = set(entry.query_hash.lower().split())
                if cached_words:
                    similarity = len(query_words & cached_words) / len(query_words | cached_words)
                    if similarity >= threshold:
                        results.append((entry.key, entry.value, similarity))
        
        return sorted(results, key=lambda x: x[2], reverse=True)
    
    def clear(self) -> None:
        """Clear all cache entries."""
        with self.lock:
            self.cache.clear()
            self.current_size = 0
            
            if self.enable_persistence:
                try:
                    with sqlite3.connect(str(self.db_path)) as conn:
                        conn.execute("DELETE FROM cache_entries")
                except Exception as e:
                    print(f"Error clearing persistent cache: {e}")
    
    def get_stats(self) -> Dict[str, Any]:
        """Get cache statistics."""
        with self.lock:
            total_requests = self.stats['hits'] + self.stats['misses']
            hit_rate = (self.stats['hits'] / total_requests * 100) if total_requests > 0 else 0
            
            return {
                'memory_entries': len(self.cache),
                'memory_size_mb': self.current_size / (1024 * 1024),
                'max_size_mb': self.max_size_bytes / (1024 * 1024),
                'hit_rate': hit_rate,
                'total_hits': self.stats['hits'],
                'total_misses': self.stats['misses'],
                'total_evictions': self.stats['evictions'],
                'size_evictions': self.stats['size_evictions'],
                'ttl_evictions': self.stats['ttl_evictions']
            }
    
    def _start_cleanup_thread(self) -> None:
        """Start background cleanup thread."""
        def cleanup_worker():
            while True:
                try:
                    self._cleanup_expired()
                    time.sleep(300)  # Run every 5 minutes
                except Exception as e:
                    print(f"Cache cleanup error: {e}")
                    time.sleep(60)
        
        thread = threading.Thread(target=cleanup_worker, daemon=True)
        thread.start()
    
    def _cleanup_expired(self) -> None:
        """Clean up expired entries."""
        current_time = time.time()
        expired_keys = []
        
        with self.lock:
            for key, entry in self.cache.items():
                if current_time - entry.created_at > entry.ttl:
                    expired_keys.append(key)
            
            for key in expired_keys:
                self._remove_entry(key)
                self.stats['ttl_evictions'] += 1
        
        # Clean persistent cache
        if self.enable_persistence:
            try:
                with sqlite3.connect(str(self.db_path)) as conn:
                    conn.execute(
                        "DELETE FROM cache_entries WHERE ? - created_at > ttl",
                        (current_time,)
                    )
            except Exception as e:
                print(f"Error cleaning persistent cache: {e}")


# Global cache instance
smart_cache = SmartCache()
