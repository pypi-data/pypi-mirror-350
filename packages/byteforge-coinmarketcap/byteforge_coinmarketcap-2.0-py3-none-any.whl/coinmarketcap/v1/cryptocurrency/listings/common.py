from typing import List, Optional
from enum import Enum
from dataclasses import dataclass

@dataclass
class FilterOptions:
    price_min: Optional[float] = None
    price_max: Optional[float] = None
    market_cap_min: Optional[float] = None
    market_cap_max: Optional[float] = None
    volume_24h_min: Optional[float] = None
    volume_24h_max: Optional[float] = None
    circulating_supply_min: Optional[float] = None
    circulating_supply_max: Optional[float] = None
    percent_change_24h_min: Optional[float] = None
    percent_change_24h_max: Optional[float] = None
    tags: Optional[List[str]] = None


class AuxFields(Enum):
    NUM_MARKET_PAIRS = "num_market_pairs"
    CMC_RANK = "cmc_rank"
    DATE_ADDED = "date_added"
    TAGS = "tags"
    PLATFORM = "platform"
    MAX_SUPPLY = "max_supply"
    TOTAL_SUPPLY = "total_supply"
    MARKET_CAP_BY_TOTAL_SUPPLY = "market_cap_by_total_supply"
    VOLUME_24H_REPORTED = "volume_24h_reported"
    VOLUME_7D = "volume_7d"
    VOLUME_7D_REPORTED = "volume_7d_reported"
    VOLUME_30D = "volume_30d"
    VOLUME_30D_REPORTED = "volume_30d_reported"
    IS_MARKET_CAP_INCLUDED = "is_market_cap_included_in_calc"

class SortDir(Enum):
	ASC = "asc"
	DESC = "desc"

class SortOption(Enum):
    MARKET_CAP = "market_cap"
    MARKET_CAP_STRICT = "market_cap_strict"
    NAME = "name"
    SYMBOL = "symbol"
    DATE_ADDED = "date_added"
    PRICE = "price"
    CIRCULATING_SUPPLY = "circulating_supply"
    TOTAL_SUPPLY = "total_supply"
    MAX_SUPPLY = "max_supply"
    NUM_MARKET_PAIRS = "num_market_pairs"
    MARKET_CAP_BY_TOTAL_SUPPLY_STRICT = "market_cap_by_total_supply_strict"
    VOLUME_24H = "volume_24h"
    VOLUME_7D = "volume_7d"
    VOLUME_30D = "volume_30d"
    PERCENT_CHANGE_1H = "percent_change_1h"
    PERCENT_CHANGE_24H = "percent_change_24h"
    PERCENT_CHANGE_7D = "percent_change_7d"

def _validate_interval(interval: str) -> None:
    """
    Validates that the given interval string is a supported time interval format.
    
    Parameters:
        interval (str): The time interval to validate. Must be one of the supported calendar 
                        intervals ('hourly', 'daily', 'weekly', 'monthly', 'yearly') or 
                        relative time intervals (e.g., '5m', '1h', '1d', etc.).
    
    Raises:
        ValueError: If the provided interval is not in the list of supported formats.
    """
    # Define allowed calendar year and time constants
    calendar_intervals = {"hourly", "daily", "weekly", "monthly", "yearly"}

    # Define allowed relative time intervals
    relative_intervals = {
        "5m", "10m", "15m", "30m", "45m",
        "1h", "2h", "3h", "4h", "6h", "12h",
        "1d", "2d", "3d", "7d", "14d", "15d", "30d", "60d", "90d", "365d"
    }

    # Check if the interval is in one of the allowed sets
    if interval not in calendar_intervals and interval not in relative_intervals:
        # If not, raise a ValueError with a message about the invalid interval
        raise ValueError(f"Invalid interval: '{interval}'. Please provide a valid interval.")

