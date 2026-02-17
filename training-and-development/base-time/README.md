# ⏰ Base Time Utilities Module

## Overview
This module provides time management utilities for CGM applications, including timestamp handling, time zone support, and time-based calculations for glucose monitoring.

## Purpose
- Standardize time handling across the application
- Support multiple time zones
- Calculate time-based metrics (time-in-range, duration, etc.)
- Handle CGM reading intervals and timestamps
- Provide time formatting for display

## Module Structure

```
base-time/
├── README.md                    # This file
├── utils/
│   ├── time_manager.py          # Core time management utilities
│   ├── timezone_handler.py      # Time zone conversions
│   └── interval_calculator.py   # CGM interval calculations
└── examples/
    └── time_usage.py            # Example usage patterns
```

## Key Features

### 1. **Standardized Timestamps**
- Always store in ISO 8601 format with timezone
- UTC for backend storage
- Local time for display
- Consistent parsing and formatting

### 2. **CGM Interval Management**
- 5-minute standard intervals
- Handle missing readings
- Interpolation for gaps
- Validation of reading frequency

### 3. **Time Zone Support**
- Automatic timezone detection
- Conversion between timezones
- Daylight saving time handling
- Travel mode for timezone changes

### 4. **Time-Based Calculations**
- Time-in-range calculations
- Duration between events
- Time-of-day analysis
- Date range filtering

## Core Components

### TimeManager Class

```python
from datetime import datetime, timedelta
import pytz

class TimeManager:
    """
    Central time management for CGM applications
    """
    
    def __init__(self, default_timezone='UTC'):
        self.default_tz = pytz.timezone(default_timezone)
        self.local_tz = self._detect_local_timezone()
    
    def now(self) -> datetime:
        """Get current time with timezone"""
        return datetime.now(self.default_tz)
    
    def to_iso(self, dt: datetime) -> str:
        """Convert datetime to ISO 8601 string"""
        return dt.isoformat()
    
    def from_iso(self, iso_string: str) -> datetime:
        """Parse ISO 8601 string to datetime"""
        return datetime.fromisoformat(iso_string)
    
    def to_local_time(self, dt: datetime) -> datetime:
        """Convert to local timezone"""
        return dt.astimezone(self.local_tz)
    
    def time_ago(self, dt: datetime) -> str:
        """
        Human-readable time ago
        Returns: "5 minutes ago", "2 hours ago", etc.
        """
        now = self.now()
        diff = now - dt
        
        seconds = diff.total_seconds()
        if seconds < 60:
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
```

### CGM Interval Calculator

```python
class CGMIntervalCalculator:
    """
    Calculate and validate CGM reading intervals
    """
    
    STANDARD_INTERVAL_MINUTES = 5
    MAX_GAP_MINUTES = 30  # Alert if gap exceeds this
    
    def calculate_expected_readings(
        self, 
        start_time: datetime, 
        end_time: datetime
    ) -> int:
        """Calculate expected number of CGM readings"""
        duration_minutes = (end_time - start_time).total_seconds() / 60
        return int(duration_minutes / self.STANDARD_INTERVAL_MINUTES)
    
    def find_gaps(self, readings: List[Dict]) -> List[Dict]:
        """
        Find gaps in CGM readings
        Returns list of gaps with start/end times and duration
        """
        gaps = []
        for i in range(len(readings) - 1):
            current = datetime.fromisoformat(readings[i]['timestamp'])
            next_reading = datetime.fromisoformat(readings[i + 1]['timestamp'])
            
            gap_minutes = (next_reading - current).total_seconds() / 60
            
            if gap_minutes > self.MAX_GAP_MINUTES:
                gaps.append({
                    'start': readings[i]['timestamp'],
                    'end': readings[i + 1]['timestamp'],
                    'duration_minutes': gap_minutes,
                    'severity': self._classify_gap(gap_minutes)
                })
        
        return gaps
    
    def interpolate_missing(
        self, 
        readings: List[Dict], 
        max_gap_minutes: int = 15
    ) -> List[Dict]:
        """
        Interpolate missing readings for small gaps
        Only interpolates if gap is <= max_gap_minutes
        """
        interpolated = []
        
        for i in range(len(readings) - 1):
            interpolated.append(readings[i])
            
            current_time = datetime.fromisoformat(readings[i]['timestamp'])
            next_time = datetime.fromisoformat(readings[i + 1]['timestamp'])
            gap_minutes = (next_time - current_time).total_seconds() / 60
            
            if gap_minutes <= max_gap_minutes and gap_minutes > self.STANDARD_INTERVAL_MINUTES:
                # Interpolate
                num_missing = int(gap_minutes / self.STANDARD_INTERVAL_MINUTES) - 1
                current_glucose = readings[i]['glucose']
                next_glucose = readings[i + 1]['glucose']
                
                for j in range(1, num_missing + 1):
                    interp_time = current_time + timedelta(
                        minutes=j * self.STANDARD_INTERVAL_MINUTES
                    )
                    interp_glucose = current_glucose + (
                        (next_glucose - current_glucose) * j / (num_missing + 1)
                    )
                    
                    interpolated.append({
                        'glucose': round(interp_glucose, 1),
                        'timestamp': interp_time.isoformat(),
                        'interpolated': True
                    })
        
        interpolated.append(readings[-1])
        return interpolated
```

### Time Zone Handler

```python
class TimezoneHandler:
    """
    Handle timezone conversions and travel mode
    """
    
    def __init__(self):
        self.user_timezone = self._detect_timezone()
        self.travel_mode = False
        self.travel_timezone = None
    
    def enable_travel_mode(self, destination_timezone: str):
        """Enable travel mode with destination timezone"""
        self.travel_mode = True
        self.travel_timezone = pytz.timezone(destination_timezone)
    
    def disable_travel_mode(self):
        """Disable travel mode and return to user timezone"""
        self.travel_mode = False
        self.travel_timezone = None
    
    def get_display_timezone(self) -> pytz.timezone:
        """Get timezone for display (travel or home)"""
        if self.travel_mode and self.travel_timezone:
            return self.travel_timezone
        return self.user_timezone
    
    def convert_timestamp(
        self, 
        timestamp: str, 
        target_timezone: str
    ) -> datetime:
        """Convert timestamp to target timezone"""
        dt = datetime.fromisoformat(timestamp)
        target_tz = pytz.timezone(target_timezone)
        return dt.astimezone(target_tz)
```

## Common Use Cases

### 1. Time Since Last Reading
```python
time_mgr = TimeManager()
last_reading_time = time_mgr.from_iso("2026-02-17T10:30:00Z")
time_ago_str = time_mgr.time_ago(last_reading_time)
print(f"Last reading: {time_ago_str}")
# Output: "Last reading: 5 minutes ago"
```

### 2. Calculate Time in Range
```python
def calculate_time_in_range(
    readings: List[Dict],
    target_range: Tuple[float, float] = (70, 180)
) -> float:
    """Calculate percentage of time in target range"""
    if not readings:
        return 0.0
    
    in_range_count = sum(
        1 for r in readings 
        if target_range[0] <= r['glucose'] <= target_range[1]
    )
    
    return (in_range_count / len(readings)) * 100
```

### 3. Filter by Time Range
```python
def filter_by_date_range(
    readings: List[Dict],
    start_date: datetime,
    end_date: datetime
) -> List[Dict]:
    """Filter readings within date range"""
    return [
        r for r in readings
        if start_date <= datetime.fromisoformat(r['timestamp']) <= end_date
    ]
```

### 4. Group by Time of Day
```python
def group_by_time_of_day(readings: List[Dict]) -> Dict[str, List]:
    """Group readings by time of day periods"""
    periods = {
        'night': [],      # 00:00-06:00
        'morning': [],    # 06:00-12:00
        'afternoon': [],  # 12:00-18:00
        'evening': []     # 18:00-24:00
    }
    
    for reading in readings:
        dt = datetime.fromisoformat(reading['timestamp'])
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
```

## Time Formatting

### Display Formats
```python
# Short time: "10:30 AM"
dt.strftime("%I:%M %p")

# Date and time: "Feb 17, 2026 10:30 AM"
dt.strftime("%b %d, %Y %I:%M %p")

# ISO format: "2026-02-17T10:30:00Z"
dt.isoformat()

# Relative: "5 minutes ago"
time_manager.time_ago(dt)
```

## Best Practices

1. **Always Use Timezone-Aware Datetimes**
   - Never use naive datetimes
   - Store in UTC, display in local time

2. **Validate Timestamps**
   - Check for future timestamps
   - Validate CGM reading intervals
   - Handle clock changes

3. **Handle Edge Cases**
   - Daylight saving time transitions
   - Leap seconds
   - Time zone changes during travel

4. **Consistent Formatting**
   - Use ISO 8601 for storage
   - Use localized formats for display
   - Include timezone information

## Testing Time-Dependent Code

```python
from unittest.mock import patch
from datetime import datetime

# Mock current time for testing
with patch('datetime.datetime') as mock_datetime:
    mock_datetime.now.return_value = datetime(2026, 2, 17, 10, 30, 0)
    # Test code here
```

## Configuration

```python
# config.py
TIME_CONFIG = {
    'default_timezone': 'UTC',
    'cgm_interval_minutes': 5,
    'max_gap_minutes': 30,
    'date_format': '%Y-%m-%d',
    'time_format': '%H:%M',
    'datetime_format': '%Y-%m-%d %H:%M:%S'
}
```

---

**Next Steps**:
1. Install required packages (`pip install pytz`)
2. Review time management utilities
3. Integrate with CGM data processing
4. Test with different timezones
5. Handle edge cases

For questions or support, refer to the main [Training & Development](../README.md) guide.
