"""
Data Synchronization Module
Handles synchronization of CGM and experiment data between devices and backend
"""

import json
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Set
from pathlib import Path
import hashlib


class DataSyncManager:
    """
    Manage synchronization of data between local storage and backend
    """
    
    def __init__(self, local_storage_path: str = "local_data", sync_interval_minutes: int = 5):
        self.local_storage = Path(local_storage_path)
        self.local_storage.mkdir(exist_ok=True)
        self.sync_interval = timedelta(minutes=sync_interval_minutes)
        self.last_sync = None
        self.pending_sync = []
        
    def add_to_sync_queue(self, data_type: str, data: Dict):
        """
        Add data to sync queue for next sync operation
        
        Args:
            data_type: Type of data (cgm_reading, meal, experiment, etc.)
            data: Data dictionary to sync
        """
        sync_item = {
            "type": data_type,
            "data": data,
            "timestamp": datetime.now().isoformat(),
            "id": self._generate_id(data),
            "synced": False
        }
        self.pending_sync.append(sync_item)
        self._save_pending_sync()
        return sync_item["id"]
    
    def sync_now(self, backend_api=None) -> Dict:
        """
        Perform immediate synchronization
        
        Args:
            backend_api: Backend API client instance
            
        Returns:
            Dictionary with sync results
        """
        if not self.pending_sync:
            return {
                "success": True,
                "message": "No data to sync",
                "synced_count": 0
            }
        
        synced_items = []
        failed_items = []
        
        for item in self.pending_sync:
            try:
                if backend_api:
                    # Send to backend
                    success = self._send_to_backend(item, backend_api)
                    if success:
                        item["synced"] = True
                        synced_items.append(item)
                    else:
                        failed_items.append(item)
                else:
                    # Just mark as synced for testing
                    item["synced"] = True
                    synced_items.append(item)
            except Exception as e:
                print(f"Sync error for item {item['id']}: {e}")
                failed_items.append(item)
        
        # Remove synced items from queue
        self.pending_sync = [item for item in self.pending_sync if not item["synced"]]
        self._save_pending_sync()
        
        self.last_sync = datetime.now()
        
        return {
            "success": len(failed_items) == 0,
            "synced_count": len(synced_items),
            "failed_count": len(failed_items),
            "timestamp": self.last_sync.isoformat(),
            "failed_items": [item["id"] for item in failed_items]
        }
    
    def check_sync_needed(self) -> bool:
        """Check if sync is needed based on interval and pending items"""
        if not self.pending_sync:
            return False
        
        if self.last_sync is None:
            return True
        
        time_since_sync = datetime.now() - self.last_sync
        return time_since_sync >= self.sync_interval
    
    def get_pending_count(self) -> int:
        """Get count of items pending sync"""
        return len(self.pending_sync)
    
    def resolve_conflicts(self, local_data: Dict, remote_data: Dict) -> Dict:
        """
        Resolve conflicts between local and remote data
        Uses last-write-wins strategy by default
        """
        local_time = datetime.fromisoformat(local_data.get("timestamp", "1970-01-01"))
        remote_time = datetime.fromisoformat(remote_data.get("timestamp", "1970-01-01"))
        
        if local_time > remote_time:
            return {
                "resolved_data": local_data,
                "source": "local",
                "reason": "Local data is newer"
            }
        else:
            return {
                "resolved_data": remote_data,
                "source": "remote",
                "reason": "Remote data is newer"
            }
    
    def export_data(self, filename: Optional[str] = None) -> str:
        """
        Export all local data to JSON file
        """
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"data_export_{timestamp}.json"
        
        export_path = self.local_storage / filename
        
        export_data = {
            "export_timestamp": datetime.now().isoformat(),
            "pending_sync_count": len(self.pending_sync),
            "last_sync": self.last_sync.isoformat() if self.last_sync else None,
            "data": self.pending_sync
        }
        
        with open(export_path, 'w') as f:
            json.dump(export_data, f, indent=2)
        
        return str(export_path)
    
    def import_data(self, filename: str) -> Dict:
        """
        Import data from JSON file
        """
        import_path = self.local_storage / filename
        
        with open(import_path, 'r') as f:
            import_data = json.load(f)
        
        imported_count = 0
        for item in import_data.get("data", []):
            # Check for duplicates
            if not self._is_duplicate(item):
                self.pending_sync.append(item)
                imported_count += 1
        
        self._save_pending_sync()
        
        return {
            "success": True,
            "imported_count": imported_count,
            "total_in_file": len(import_data.get("data", [])),
            "duplicates_skipped": len(import_data.get("data", [])) - imported_count
        }
    
    def _generate_id(self, data: Dict) -> str:
        """Generate unique ID for data item"""
        data_str = json.dumps(data, sort_keys=True)
        return hashlib.md5(data_str.encode()).hexdigest()[:16]
    
    def _is_duplicate(self, item: Dict) -> bool:
        """Check if item is already in sync queue"""
        item_id = item.get("id")
        return any(existing["id"] == item_id for existing in self.pending_sync)
    
    def _save_pending_sync(self):
        """Save pending sync queue to disk"""
        sync_file = self.local_storage / "pending_sync.json"
        with open(sync_file, 'w') as f:
            json.dump(self.pending_sync, f, indent=2)
    
    def _load_pending_sync(self):
        """Load pending sync queue from disk"""
        sync_file = self.local_storage / "pending_sync.json"
        if sync_file.exists():
            with open(sync_file, 'r') as f:
                self.pending_sync = json.load(f)
    
    def _send_to_backend(self, item: Dict, backend_api) -> bool:
        """
        Send item to backend API
        Override this method to implement actual backend communication
        """
        # This is a placeholder - implement actual API calls
        data_type = item["type"]
        data = item["data"]
        
        # Example API call structure:
        # if data_type == "cgm_reading":
        #     response = backend_api.post_cgm_reading(data)
        # elif data_type == "meal":
        #     response = backend_api.post_meal(data)
        # return response.success
        
        # For now, always return True (simulated success)
        return True


class OfflineCache:
    """
    Cache data locally when offline
    """
    
    def __init__(self, cache_dir: str = "cache"):
        self.cache_dir = Path(cache_dir)
        self.cache_dir.mkdir(exist_ok=True)
        
    def cache_data(self, key: str, data: Dict, ttl_hours: int = 24):
        """
        Cache data with expiration
        
        Args:
            key: Unique cache key
            data: Data to cache
            ttl_hours: Time to live in hours
        """
        cache_entry = {
            "data": data,
            "cached_at": datetime.now().isoformat(),
            "expires_at": (datetime.now() + timedelta(hours=ttl_hours)).isoformat()
        }
        
        cache_file = self.cache_dir / f"{key}.json"
        with open(cache_file, 'w') as f:
            json.dump(cache_entry, f, indent=2)
    
    def get_cached(self, key: str) -> Optional[Dict]:
        """
        Retrieve cached data if not expired
        """
        cache_file = self.cache_dir / f"{key}.json"
        
        if not cache_file.exists():
            return None
        
        with open(cache_file, 'r') as f:
            cache_entry = json.load(f)
        
        expires_at = datetime.fromisoformat(cache_entry["expires_at"])
        if datetime.now() > expires_at:
            # Cache expired
            cache_file.unlink()
            return None
        
        return cache_entry["data"]
    
    def clear_cache(self, older_than_hours: Optional[int] = None):
        """
        Clear cache entries
        
        Args:
            older_than_hours: If specified, only clear entries older than this
        """
        for cache_file in self.cache_dir.glob("*.json"):
            if older_than_hours:
                with open(cache_file, 'r') as f:
                    cache_entry = json.load(f)
                cached_at = datetime.fromisoformat(cache_entry["cached_at"])
                age_hours = (datetime.now() - cached_at).total_seconds() / 3600
                if age_hours > older_than_hours:
                    cache_file.unlink()
            else:
                cache_file.unlink()


if __name__ == "__main__":
    # Example usage
    print("Data Sync Manager Example")
    print("-" * 60)
    
    # Initialize sync manager
    sync_manager = DataSyncManager(local_storage_path="test_sync_data")
    
    # Add some data to sync queue
    cgm_reading = {
        "glucose": 120,
        "timestamp": datetime.now().isoformat(),
        "source": "cgm_sensor"
    }
    
    meal_entry = {
        "meal_type": "breakfast",
        "foods": ["oatmeal", "banana"],
        "carbs": 45,
        "timestamp": datetime.now().isoformat()
    }
    
    sync_manager.add_to_sync_queue("cgm_reading", cgm_reading)
    sync_manager.add_to_sync_queue("meal", meal_entry)
    
    print(f"Pending sync items: {sync_manager.get_pending_count()}")
    
    # Perform sync
    result = sync_manager.sync_now()
    print(f"\nSync result: {result}")
    
    # Test offline cache
    cache = OfflineCache(cache_dir="test_cache")
    cache.cache_data("user_001_glucose", {"glucose": 125}, ttl_hours=1)
    
    cached_data = cache.get_cached("user_001_glucose")
    print(f"\nCached data retrieved: {cached_data}")
    
    print("\nData sync examples completed successfully!")
