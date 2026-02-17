"""
Time Manager Module
Core time management utilities for CGM applications
"""

from datetime import datetime, timedelta
from typing import Optional, List, Dict, Tuple
import pytz
from zoneinfo import ZoneInfo
import time


class TimeManager:
    """
    Central time management for CGM applications
    Handles timezone-aware datetime operations
    """
    
    def __init__(self, default_timezone: str = 'UTC'):
        """
        Initialize TimeManager
        
        Args:
            default_timezone: Default timezone string (e.g., 'UTC', 'America/New_York')
        """
        self.default_tz = ZoneInfo(default_timezone)
        self.local_tz = self._detect_local_timezone()
        
    def _detect_local_timezone(self) -> ZoneInfo:
        """
        Detect the local system timezone
        Currently defaults to UTC for consistency across deployments
        """
        # Default to UTC for consistency
        # In production, could use tzlocal library for better detection
        return ZoneInfo('UTC')
    
    def now(self, timezone: Optional[str] = None) -> datetime:
        """
        Get current time with timezone
        
        Args:
            timezone: Optional timezone string, defaults to default_tz
            
        Returns:
            Current datetime with timezone
        """
        tz = ZoneInfo(timezone) if timezone else self.default_tz
        return datetime.now(tz)
    
    def to_iso(self, dt: datetime) -> str:
        """
        Convert datetime to ISO 8601 string
        
        Args:
            dt: Datetime object
            
        Returns:
            ISO 8601 formatted string
        """
        return dt.isoformat()
    
    def from_iso(self, iso_string: str) -> datetime:
        """
        Parse ISO 8601 string to datetime
        
        Args:
            iso_string: ISO 8601 formatted string
            
        Returns:
            Datetime object
        """
        return datetime.fromisoformat(iso_string)
    
    def to_local_time(self, dt: datetime) -> datetime:
        """
        Convert datetime to local timezone
        
        Args:
            dt: Datetime object
            
        Returns:
            Datetime in local timezone
        """
        return dt.astimezone(self.local_tz)
    
    def to_utc(self, dt: datetime) -> datetime:
        """
        Convert datetime to UTC
        
        Args:
            dt: Datetime object
            
        Returns:
            Datetime in UTC
        """
        return dt.astimezone(ZoneInfo('UTC'))
    
    def time_ago(self, dt: datetime) -> str:
        """
        Human-readable time ago string
        
        Args:
            dt: Past datetime
            
        Returns:
            String like "5 minutes ago", "2 hours ago", etc.
        """
        now = self.now()
        
        # Ensure both datetimes have timezone info
        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=self.default_tz)
        if now.tzinfo is None:
            now = now.replace(tzinfo=self.default_tz)
        
        diff = now - dt
        seconds = diff.total_seconds()
        
        if seconds < 0:
            return "in the future"
        elif seconds < 60:
            return "just now"
        elif seconds < 3600:
            minutes = int(seconds / 60)
            return f"{minutes} minute{'s' if minutes != 1 else ''} ago"
        elif seconds < 86400:
            hours = int(seconds / 3600)
            return f"{hours} hour{'s' if hours != 1 else ''} ago"
        else:
            days = int(seconds / 86400)
            return f"{days} day{'s' if days != 1 else ''} ago"
    
    def format_display_time(self, dt: datetime, format_type: str = 'short') -> str:
        """
        Format datetime for display
        
        Args:
            dt: Datetime to format
            format_type: 'short', 'medium', 'long', or 'relative'
            
        Returns:
            Formatted string
        """
        local_dt = self.to_local_time(dt)
        
        if format_type == 'short':
            return local_dt.strftime("%I:%M %p")
        elif format_type == 'medium':
            return local_dt.strftime("%b %d, %I:%M %p")
        elif format_type == 'long':
            return local_dt.strftime("%B %d, %Y %I:%M:%S %p")
        elif format_type == 'relative':
            return self.time_ago(dt)
        else:
            return local_dt.isoformat()
    
    def calculate_duration(self, start: datetime, end: datetime) -> Dict[str, float]:
        """
        Calculate duration between two datetimes
        
        Args:
            start: Start datetime
            end: End datetime
            
        Returns:
            Dictionary with duration in various units
        """
        duration = end - start
        seconds = duration.total_seconds()
        
        return {
            'seconds': seconds,
            'minutes': seconds / 60,
            'hours': seconds / 3600,
            'days': seconds / 86400,
            'formatted': self._format_duration(seconds)
        }
    
    def _format_duration(self, seconds: float) -> str:
        """Format duration in human-readable format"""
        if seconds < 60:
            return f"{int(seconds)} seconds"
        elif seconds < 3600:
            minutes = int(seconds / 60)
            return f"{minutes} minute{'s' if minutes != 1 else ''}"
        elif seconds < 86400:
            hours = int(seconds / 3600)
            minutes = int((seconds % 3600) / 60)
            if minutes > 0:
                return f"{hours}h {minutes}m"
            return f"{hours} hour{'s' if hours != 1 else ''}"
        else:
            days = int(seconds / 86400)
            hours = int((seconds % 86400) / 3600)
            if hours > 0:
                return f"{days}d {hours}h"
            return f"{days} day{'s' if days != 1 else ''}"
    
    def is_same_day(self, dt1: datetime, dt2: datetime) -> bool:
        """Check if two datetimes are on the same day"""
        local1 = self.to_local_time(dt1)
        local2 = self.to_local_time(dt2)
        return local1.date() == local2.date()
    
    def start_of_day(self, dt: datetime) -> datetime:
        """Get start of day (00:00:00) for given datetime"""
        local = self.to_local_time(dt)
        start = local.replace(hour=0, minute=0, second=0, microsecond=0)
        return start
    
    def end_of_day(self, dt: datetime) -> datetime:
        """Get end of day (23:59:59) for given datetime"""
        local = self.to_local_time(dt)
        end = local.replace(hour=23, minute=59, second=59, microsecond=999999)
        return end


class TimezoneHandler:
    """
    Handle timezone conversions and travel mode
    """
    
    def __init__(self, user_timezone: str = 'UTC'):
        """
        Initialize TimezoneHandler
        
        Args:
            user_timezone: User's home timezone
        """
        self.user_timezone = ZoneInfo(user_timezone)
        self.travel_mode = False
        self.travel_timezone = None
    
    def enable_travel_mode(self, destination_timezone: str):
        """
        Enable travel mode with destination timezone
        
        Args:
            destination_timezone: Destination timezone string
        """
        self.travel_mode = True
        self.travel_timezone = ZoneInfo(destination_timezone)
    
    def disable_travel_mode(self):
        """Disable travel mode and return to user timezone"""
        self.travel_mode = False
        self.travel_timezone = None
    
    def get_display_timezone(self) -> ZoneInfo:
        """Get timezone for display (travel or home)"""
        if self.travel_mode and self.travel_timezone:
            return self.travel_timezone
        return self.user_timezone
    
    def convert_timestamp(
        self, 
        timestamp: str, 
        target_timezone: str
    ) -> datetime:
        """
        Convert timestamp to target timezone
        
        Args:
            timestamp: ISO format timestamp
            target_timezone: Target timezone string
            
        Returns:
            Datetime in target timezone
        """
        dt = datetime.fromisoformat(timestamp)
        target_tz = ZoneInfo(target_timezone)
        return dt.astimezone(target_tz)
    
    def get_timezone_offset(self, timezone: str) -> float:
        """
        Get timezone offset from UTC in hours
        
        Args:
            timezone: Timezone string
            
        Returns:
            Offset in hours
        """
        tz = ZoneInfo(timezone)
        now = datetime.now(tz)
        offset = now.utcoffset()
        return offset.total_seconds() / 3600 if offset else 0


class DateRangeFilter:
    """
    Filter data by date ranges
    """
    
    @staticmethod
    def filter_by_date_range(
        readings: List[Dict],
        start_date: datetime,
        end_date: datetime,
        timestamp_key: str = 'timestamp'
    ) -> List[Dict]:
        """
        Filter readings within date range
        
        Args:
            readings: List of reading dictionaries
            start_date: Start datetime
            end_date: End datetime
            timestamp_key: Key for timestamp in reading dict
            
        Returns:
            Filtered list of readings
        """
        return [
            r for r in readings
            if start_date <= datetime.fromisoformat(r[timestamp_key]) <= end_date
        ]
    
    @staticmethod
    def filter_last_n_hours(
        readings: List[Dict],
        hours: int,
        timestamp_key: str = 'timestamp'
    ) -> List[Dict]:
        """Filter readings from last N hours"""
        cutoff = datetime.now(ZoneInfo('UTC')) - timedelta(hours=hours)
        return [
            r for r in readings
            if datetime.fromisoformat(r[timestamp_key]) >= cutoff
        ]
    
    @staticmethod
    def filter_last_n_days(
        readings: List[Dict],
        days: int,
        timestamp_key: str = 'timestamp'
    ) -> List[Dict]:
        """Filter readings from last N days"""
        cutoff = datetime.now(ZoneInfo('UTC')) - timedelta(days=days)
        return [
            r for r in readings
            if datetime.fromisoformat(r[timestamp_key]) >= cutoff
        ]
    
    @staticmethod
    def group_by_time_of_day(
        readings: List[Dict],
        timestamp_key: str = 'timestamp'
    ) -> Dict[str, List[Dict]]:
        """
        Group readings by time of day periods
        
        Returns:
            Dictionary with keys: 'night', 'morning', 'afternoon', 'evening'
        """
        periods = {
            'night': [],      # 00:00-06:00
            'morning': [],    # 06:00-12:00
            'afternoon': [],  # 12:00-18:00
            'evening': []     # 18:00-24:00
        }
        
        for reading in readings:
            dt = datetime.fromisoformat(reading[timestamp_key])
            hour = dt.hour
            
            if 0 <= hour < 6:
                periods['night'].append(reading)
            elif 6 <= hour < 12:
                periods['morning'].append(reading)
            elif 12 <= hour < 18:
                periods['afternoon'].append(reading)
            else:
                periods['evening'].append(reading)
        
        return periods


if __name__ == "__main__":
    # Example usage
    print("Time Manager Example")
    print("-" * 60)
    
    # Initialize time manager
    time_mgr = TimeManager(default_timezone='UTC')
    
    # Current time
    now = time_mgr.now()
    print(f"Current time (UTC): {time_mgr.to_iso(now)}")
    print(f"Current time (local): {time_mgr.to_local_time(now)}")
    
    # Time ago
    past_time = now - timedelta(minutes=45)
    print(f"\nTime ago: {time_mgr.time_ago(past_time)}")
    
    # Format display
    print(f"Short format: {time_mgr.format_display_time(now, 'short')}")
    print(f"Medium format: {time_mgr.format_display_time(now, 'medium')}")
    
    # Duration calculation
    start = now - timedelta(hours=3, minutes=25)
    duration = time_mgr.calculate_duration(start, now)
    print(f"\nDuration: {duration['formatted']}")
    
    # Timezone handler
    tz_handler = TimezoneHandler(user_timezone='America/New_York')
    tz_handler.enable_travel_mode('Europe/London')
    print(f"\nTravel mode enabled to: {tz_handler.travel_timezone}")
    
    print("\nTime management examples completed successfully!")
