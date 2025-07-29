"""
Utility functions for handling time and dates in the Universal History system.
"""
from datetime import datetime, timedelta, date
from typing import Dict, List, Optional, Tuple, Union
import re

def parse_iso_date(date_str: str) -> datetime:
    """
    Parse an ISO format date string into a datetime object.
    
    Args:
        date_str (str): The ISO format date string
        
    Returns:
        datetime: The parsed datetime
        
    Raises:
        ValueError: If the string is not a valid ISO format date
    """
    return datetime.fromisoformat(date_str)

def format_iso_date(dt: Union[datetime, date]) -> str:
    """
    Format a datetime or date object as an ISO format string.
    
    Args:
        dt (Union[datetime, date]): The datetime or date to format
        
    Returns:
        str: The ISO format string
    """
    return dt.isoformat()

def date_range(start_date: datetime, end_date: datetime, interval: timedelta = timedelta(days=1)) -> List[datetime]:
    """
    Generate a list of dates within a range.
    
    Args:
        start_date (datetime): The start date
        end_date (datetime): The end date
        interval (timedelta): The interval between dates
        
    Returns:
        List[datetime]: List of dates
    """
    result = []
    current_date = start_date
    
    while current_date <= end_date:
        result.append(current_date)
        current_date += interval
    
    return result

def group_by_period(items: List[Dict], 
                   date_key: str, 
                   period: str = 'month') -> Dict[str, List[Dict]]:
    """
    Group items by a time period.
    
    Args:
        items (List[Dict]): The items to group
        date_key (str): The key to use for the date
        period (str): The period to group by ('day', 'week', 'month', 'year')
        
    Returns:
        Dict[str, List[Dict]]: Dictionary mapping period keys to lists of items
    """
    result = {}
    
    for item in items:
        if date_key not in item:
            continue
            
        date_value = item[date_key]
        if isinstance(date_value, str):
            try:
                dt = datetime.fromisoformat(date_value)
            except ValueError:
                continue
        elif isinstance(date_value, (datetime, date)):
            dt = date_value
        else:
            continue
            
        if period == 'day':
            key = dt.strftime('%Y-%m-%d')
        elif period == 'week':
            # ISO week format: YYYY-Www
            key = f"{dt.isocalendar()[0]}-W{dt.isocalendar()[1]:02d}"
        elif period == 'month':
            key = dt.strftime('%Y-%m')
        elif period == 'year':
            key = dt.strftime('%Y')
        else:
            raise ValueError(f"Invalid period: {period}. Must be 'day', 'week', 'month', or 'year'.")
            
        if key not in result:
            result[key] = []
            
        result[key].append(item)
    
    return result

def calculate_time_difference(start_date: Union[str, datetime], 
                             end_date: Union[str, datetime],
                             unit: str = 'days') -> float:
    """
    Calculate the difference between two dates.
    
    Args:
        start_date (Union[str, datetime]): The start date
        end_date (Union[str, datetime]): The end date
        unit (str): The unit of the result ('seconds', 'minutes', 'hours', 'days', 'weeks', 'months', 'years')
        
    Returns:
        float: The time difference in the specified unit
        
    Raises:
        ValueError: If the unit is invalid
    """
    # Convert strings to datetime objects if necessary
    if isinstance(start_date, str):
        start_date = datetime.fromisoformat(start_date)
    if isinstance(end_date, str):
        end_date = datetime.fromisoformat(end_date)
        
    # Calculate the difference in seconds
    diff_seconds = (end_date - start_date).total_seconds()
    
    # Convert to the requested unit
    if unit == 'seconds':
        return diff_seconds
    elif unit == 'minutes':
        return diff_seconds / 60
    elif unit == 'hours':
        return diff_seconds / 3600
    elif unit == 'days':
        return diff_seconds / 86400
    elif unit == 'weeks':
        return diff_seconds / 604800
    elif unit == 'months':
        # Approximate
        return diff_seconds / 2592000  # 30 days
    elif unit == 'years':
        # Approximate
        return diff_seconds / 31536000  # 365 days
    else:
        raise ValueError(f"Invalid unit: {unit}. Must be 'seconds', 'minutes', 'hours', 'days', 'weeks', 'months', or 'years'.")

def parse_duration(duration_str: str) -> timedelta:
    """
    Parse an ISO 8601 duration string into a timedelta object.
    
    Args:
        duration_str (str): The ISO 8601 duration string (e.g., 'P1Y2M3DT4H5M6S')
        
    Returns:
        timedelta: The parsed duration
        
    Raises:
        ValueError: If the string is not a valid ISO 8601 duration
    """
    # Regular expression to parse duration components
    pattern = re.compile(r'P(?:(?P<years>\d+)Y)?(?:(?P<months>\d+)M)?(?:(?P<days>\d+)D)?'
                         r'(?:T(?:(?P<hours>\d+)H)?(?:(?P<minutes>\d+)M)?(?:(?P<seconds>\d+)S)?)?')
    
    match = pattern.match(duration_str)
    if not match:
        raise ValueError(f"Invalid ISO 8601 duration: {duration_str}")
    
    parts = match.groupdict()
    # Convert to integers, handling None values
    parts = {k: int(v) if v else 0 for k, v in parts.items()}
    
    # Calculate total days (approximate for years and months)
    days = parts['days'] + parts['years'] * 365 + parts['months'] * 30
    
    # Create timedelta
    return timedelta(
        days=days,
        hours=parts['hours'],
        minutes=parts['minutes'],
        seconds=parts['seconds']
    )

def format_duration(td: timedelta) -> str:
    """
    Format a timedelta object as an ISO 8601 duration string.
    
    Args:
        td (timedelta): The timedelta to format
        
    Returns:
        str: The ISO 8601 duration string
    """
    # Convert to total seconds
    total_seconds = int(td.total_seconds())
    
    # Extract components
    seconds = total_seconds % 60
    total_minutes = total_seconds // 60
    minutes = total_minutes % 60
    total_hours = total_minutes // 60
    hours = total_hours % 24
    days = total_hours // 24
    
    # Format as ISO 8601 duration
    result = 'P'
    
    if days:
        result += f'{days}D'
        
    if hours or minutes or seconds:
        result += 'T'
        
        if hours:
            result += f'{hours}H'
            
        if minutes:
            result += f'{minutes}M'
            
        if seconds:
            result += f'{seconds}S'
            
    if result == 'P':
        result = 'PT0S'  # Zero duration
        
    return result

def get_time_periods_between(start_date: Union[str, datetime],
                            end_date: Union[str, datetime],
                            period: str = 'month') -> List[Tuple[datetime, datetime]]:
    """
    Get a list of time periods between two dates.
    
    Args:
        start_date (Union[str, datetime]): The start date
        end_date (Union[str, datetime]): The end date
        period (str): The period type ('day', 'week', 'month', 'year')
        
    Returns:
        List[Tuple[datetime, datetime]]: List of (period_start, period_end) tuples
        
    Raises:
        ValueError: If the period is invalid
    """
    # Convert strings to datetime objects if necessary
    if isinstance(start_date, str):
        start_date = datetime.fromisoformat(start_date)
    if isinstance(end_date, str):
        end_date = datetime.fromisoformat(end_date)
    
    result = []
    
    if period == 'day':
        # Get list of days
        days = date_range(start_date, end_date, timedelta(days=1))
        for day in days:
            day_start = datetime(day.year, day.month, day.day, 0, 0, 0)
            day_end = datetime(day.year, day.month, day.day, 23, 59, 59)
            result.append((day_start, day_end))
            
    elif period == 'week':
        # Start from the beginning of the week containing start_date
        week_start = start_date - timedelta(days=start_date.weekday())
        week_start = datetime(week_start.year, week_start.month, week_start.day, 0, 0, 0)
        
        current_start = week_start
        while current_start <= end_date:
            current_end = current_start + timedelta(days=6, hours=23, minutes=59, seconds=59)
            if current_end >= start_date:  # Only include weeks that overlap with the range
                result.append((max(current_start, start_date), min(current_end, end_date)))
            current_start = current_start + timedelta(days=7)
            
    elif period == 'month':
        # Start from the beginning of the month containing start_date
        month_start = datetime(start_date.year, start_date.month, 1, 0, 0, 0)
        
        current_start = month_start
        while current_start <= end_date:
            # Determine the last day of the current month
            if current_start.month == 12:
                next_month = datetime(current_start.year + 1, 1, 1, 0, 0, 0)
            else:
                next_month = datetime(current_start.year, current_start.month + 1, 1, 0, 0, 0)
            
            current_end = next_month - timedelta(seconds=1)
            
            if current_end >= start_date:  # Only include months that overlap with the range
                result.append((max(current_start, start_date), min(current_end, end_date)))
                
            current_start = next_month
            
    elif period == 'year':
        # Start from the beginning of the year containing start_date
        year_start = datetime(start_date.year, 1, 1, 0, 0, 0)
        
        current_start = year_start
        while current_start <= end_date:
            current_end = datetime(current_start.year, 12, 31, 23, 59, 59)
            
            if current_end >= start_date:  # Only include years that overlap with the range
                result.append((max(current_start, start_date), min(current_end, end_date)))
                
            current_start = datetime(current_start.year + 1, 1, 1, 0, 0, 0)
    
    else:
        raise ValueError(f"Invalid period: {period}. Must be 'day', 'week', 'month', or 'year'.")
    
    return result