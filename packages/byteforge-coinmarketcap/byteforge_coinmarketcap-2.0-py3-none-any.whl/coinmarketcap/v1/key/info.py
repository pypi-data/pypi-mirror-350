from dateutil import parser  
from datetime import datetime, timezone

def _key_info(market):
    """
    Retrieves key configuration and usage information from the market API.

    This function requests the API endpoint associated with key credentials and specific limits
    or configurations that are set for the user's API key, and returns these configuration details.
    
    Parameters:
        market (Market): An instance of the Market class, configured for API access.

    Returns:
        dict: A dictionary containing detailed key configuration information such as API limits.
    """
    dct_response = market._request('v1/key/info', ignore_cache=True)
    return dct_response['data']


def _safe_daily_call_limit(market):
    """
    Calculates the safe number of API calls that can be made per day, based on the remaining quota and time until the reset.

    This function estimates the daily call limit by dividing the remaining quota by the number of days left until the quota reset.
    The estimation is based on equal usage allocation each day until the reset date.

    Parameters:
        market (Market): An instance of the Market class, which handles the API communications.

    Returns:
        int: Approximate number of API calls that can be safely made per day, based on remaining monthly quota
             and days until the quota reset.
    """
    dct_response = market._request('v1/key/info', no_cache=True)
    quota_reset_dt = parser.parse(dct_response['data']['plan']['credit_limit_monthly_reset_timestamp'])
    monthly_calls_remaining = dct_response['data']['usage']['current_month']['credits_left']

    # Ensure the current datetime is timezone-aware with UTC timezone
    now_datetime = datetime.now(timezone.utc)

    # Calculate the timedelta
    time_difference = quota_reset_dt - now_datetime

    # Extract the number of days as an integer
    number_of_days = time_difference.days + 1

    # Convert daily calls calculation into an integer
    return int(monthly_calls_remaining / number_of_days) if number_of_days > 0 else 0  # Added safety for division
