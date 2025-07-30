from typing import List, Optional, Dict, Union
import time
from pprint import pprint


from coinmarketcap.v1.cryptocurrency.listings.common import _validate_interval
from coinmarketcap.types.quote_factory import QuoteFactory

def _fear_and_greed_historical(market, start: int = 1, limit: int = 500) -> List[Dict[str, Union[str, int]]]:
	"""
	Retrieves historical fear and greed index data from the CoinMarketCap API.

	Returns:
		List[Dict[str, Union[str, int]]]: A list of dictionaries containing:
			- timestamp (str): Unix timestamp of the measurement
			- value (int): The fear and greed index value (0-100)
			- value_classification (str): Classification of the value (e.g., 'Greed', 'Fear', etc.)
	"""
	params = {
		'start': start,
		'limit': limit
	}

	response = market._request('/v3/fear-and-greed/historical', params=params)
	return response.get('data', [])