import os
import sys
import json
import requests
import tempfile
import time
import requests_cache
from typing import Optional, List, Dict, Union

from requests_ratelimiter import LimiterAdapter

from .v1.cryptocurrency.map import ListingStatus
from crypto_commons.types.token_state import TokenState
from crypto_commons.types.token_info import TokenInfo
from .v2.cryptocurrency.quotes.historical import _quotes_historical_v2
from .v3.cryptocurrency.quotes.historical_v3 import _quotes_historical_v3
from .v1.cryptocurrency.listings.latest import _listings_latest
from .v1.cryptocurrency.listings.common import SortOption, AuxFields, SortDir, FilterOptions
from .v1.key.info import _key_info
from .v1.key.info import _safe_daily_call_limit
from .v1.cryptocurrency.map import _map, MapSortOption, MapAuxFields
from .v3.fear_and_greed.historical import _fear_and_greed_historical

class ServerException(Exception):
    def __init__(self, status_code, message):
        self.status_code = status_code
        self.message = message
        super().__init__(f"Server returned {status_code} - {message}")


class Market(object):

	_session = None
	_caching_session = None
	_debug_mode = False
	_api_key = None
	_limiter = None
	__DEFAULT_BASE_URL = 'https://pro-api.coinmarketcap.com/'
	__DEFAULT_TIMEOUT = 30
	__TEMPDIR_CACHE = True

	def __init__(self, api_key = None, 
			  base_url = __DEFAULT_BASE_URL, 
			  request_timeout = __DEFAULT_TIMEOUT, 
			  tempdir_cache = __TEMPDIR_CACHE,
			  rate_limit_per_minute = -1,
			  debug_mode = False):
		
		self._api_key = api_key
		self.base_url = base_url
		self.request_timeout = request_timeout
		self._debug_mode = debug_mode
		self.cache_filename = 'coinmarketcap_cache'
		self.cache_name = os.path.join(tempfile.gettempdir(), self.cache_filename) if tempdir_cache else self.cache_filename
		
		if not self._api_key:
			raise ValueError('An API key is required for using the coinmarketcap API. Please visit https://pro.coinmarketcap.com/signup/ for more information.')
		
		if rate_limit_per_minute > 0:
			self._limiter = LimiterAdapter(per_minute=rate_limit_per_minute)

	@property
	def caching_session(self):
		if not self._caching_session:
			# define a a session with caching
			self._caching_session = requests_cache.CachedSession(
			 	cache_name=self.cache_name,
			 	backend='sqlite', 
			 	expire_after=120)
			
			if self._limiter:
				self._caching_session.mount('https://', self._limiter)
			
			self._caching_session.headers.update({
					'Accept': 'application/json',
				  	'X-CMC_PRO_API_KEY': self._api_key,
				})

		return self._caching_session

	@property
	def session(self):
		if not self._session:
		
			# and a normal (non-caching) session
			self._session = requests.Session()

			self._session.headers.update({
					'Accept': 'application/json',
				  	'X-CMC_PRO_API_KEY': self._api_key,
				})
			
			if self._limiter:
				self._session.mount('https://', self._limiter)
			
		return self._session
	

	def _request(self, endpoint, params = {}, no_cache = False):
		if self._debug_mode:
			print('Request URL: ' + self.base_url + endpoint)
			if params:
				print("Request Payload:\n" + json.dumps(params, indent=4))

		try:
			if no_cache:
				response_object = self.session.get(self.base_url + endpoint, params=params, timeout=self.request_timeout)
			else:
				response_object = self.caching_session.get(self.base_url + endpoint, params=params, timeout=self.request_timeout)
			
			if self._debug_mode:
				print('Response Code: ' + str(response_object.status_code))
				if hasattr(response_object, 'from_cache'):
					print('From Cache?: ' + str(response_object.from_cache))
				print("Response Payload:\n" + json.dumps(response_object.json(), indent=4))

			if response_object.status_code == requests.codes.ok:
				return response_object.json()
			else:
				raise ServerException(response_object.status_code, response_object.text)
		except Exception as e:
			raise e

	def fear_and_greed_historical(self, start: int, limit: int) -> List[Dict[str, Union[str, int]]]:
		"""
		Retrieves historical fear and greed index data from the CoinMarketCap API.

		Returns:
			List[Dict[str, Union[str, int]]]: A list of dictionaries containing:
				- timestamp (str): Unix timestamp of the measurement
				- value (int): The fear and greed index value (0-100)
				- value_classification (str): Classification of the value (e.g., 'Greed', 'Fear', etc.)
		"""
		return _fear_and_greed_historical(self, start, limit)

	def map(self, 
			listing_status: ListingStatus = ListingStatus.ACTIVE, 
			start: int = 1,
			limit: int = 100,
			symbols: List[str] = None,
			sort: MapSortOption = MapSortOption.ID,
			aux_fields: List[MapAuxFields] = None) -> List[TokenInfo]:
		"""Returns a mapping of all cryptocurrencies to their CoinMarketCap IDs.

		This method provides a mapping of all cryptocurrencies to their CoinMarketCap IDs, 
		which can be used to make other API calls. The mapping includes basic information 
		about each cryptocurrency.

		Args:
			listing_status (ListingStatus, optional): Filter by listing status. 
				Can be ACTIVE, INACTIVE, or UNTRACKED. Defaults to ACTIVE.
			start (int, optional): Starting point for pagination. Defaults to 1.
			limit (int, optional): Number of results to return. Defaults to 100.
			symbols (List[str], optional): List of cryptocurrency symbols to filter by. 
				If None, returns all cryptocurrencies. Defaults to None.
			sort (MapSortOption, optional): Field to sort results by. Can be ID or CMC_RANK. 
				Defaults to ID.
			aux_fields (List[MapAuxFields], optional): Additional fields to include in response. 
				Can include PLATFORM, FIRST_HISTORICAL_DATA, LAST_HISTORICAL_DATA, IS_ACTIVE. 
				Defaults to None.

		Returns:
			List[TokenInfo]: List of TokenInfo objects containing cryptocurrency mapping data.

		Raises:
			ServerException: If the API request fails.
		"""
		
		return _map(self, listing_status, start, limit, symbols, sort, aux_fields)

	def quotes_historical(self,
						  id: Optional[str] = None,
						  ticker: Optional[str] = None,
						  timestamp_start: Optional[int] = int(time.time()) - 60*60*24,
						  timestamp_end: Optional[int] = int(time.time()),
						  interval: str = 'hourly',
						  convert: List[str] = ['USD']) -> List[TokenState]:
		
		return _quotes_historical_v2(self,
							   id=id,
							   ticker=ticker,
							   timestamp_start=timestamp_start,
							   timestamp_end=timestamp_end,
							   interval=interval,
							   convert=convert)
	
	
	def quotes_historical_v3(self,
						  id: Optional[str] = None,
						  ticker: Optional[str] = None,
						  timestamp_start: Optional[int] = int(time.time()) - 60*60*24,
						  timestamp_end: Optional[int] = int(time.time()),
						  interval: str = 'hourly',
						  convert: List[str] = ['USD']) -> List[TokenState]:
		
		return _quotes_historical_v3(self,
							   id=id,
							   ticker=ticker,
							   timestamp_start=timestamp_start,
							   timestamp_end=timestamp_end,
							   interval=interval,
							   convert=convert)

	def listings_latest(self, sort_by: SortOption = SortOption.MARKET_CAP, 
					sort_dir: SortDir = SortDir.DESC, 
					start: int = 1, 
					limit: int = 100, 
					convert: List[str] = ['USD'],
					aux_fields: AuxFields = None, 
					filters: FilterOptions = None) -> List[TokenState]:
		
		return _listings_latest(self, sort_by, sort_dir, start, limit, convert, aux_fields, filters)
	

	def safe_daily_call_limit(self):
		"""
		Calculates how many API calls are left for today, based on the service plan's monthly call limit.

		This function takes the user's API call limit and subtracts the number of calls used to date,
		providing a simple ratio to estimate daily available calls until the reset date. Note that 
		this is an approximation based on equal usage each day until the reset.

		Parameters:
			market (Market): An instance of the Market class, which handles the API communications.

		Returns:
			int: Approximate number of API calls left for the current day, based on daily usage 
				till the reset date and a monthly limit.
		"""		
		return _safe_daily_call_limit(self)
