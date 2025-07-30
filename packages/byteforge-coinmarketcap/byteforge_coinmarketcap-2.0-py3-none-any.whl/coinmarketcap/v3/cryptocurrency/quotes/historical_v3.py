from typing import Optional, List
import time
from datetime import datetime
from dateutil import parser
from crypto_commons.types.token_state import TokenState
from crypto_commons.types.quote import Quote
from coinmarketcap.v1.cryptocurrency.listings.common import _validate_interval
from coinmarketcap.types.quote_factory import QuoteFactory

def _quotes_historical_v3(market,
						  id: Optional[str] = None,
						  ticker: Optional[str] = None,
						  timestamp_start: Optional[int] = int(time.time()) - 60*60*24,
						  timestamp_end: Optional[int] = int(time.time()),
						  interval: str = 'hourly',
						  convert: List[str] = ['USD']) -> List[TokenState]:
	"""
	Retrieves historical price quotes for a cryptocurrency from the CoinMarketCap API.
	
	This function fetches historical price data for a specified cryptocurrency, identified
	either by its CoinMarketCap ID or by its ticker symbol. The data is returned as a list
	of TokenState objects, each containing price and market data for a specific point in time.
	
	Parameters:
		market: The CoinMarketCap API market client instance
		id (Optional[str]): The CoinMarketCap ID of the cryptocurrency (either id or ticker must be provided)
		ticker (Optional[str]): The ticker symbol of the cryptocurrency (either id or ticker must be provided)
		timestamp_start (Optional[int]): Unix timestamp for the start of the data range (default: 24 hours ago)
		timestamp_end (Optional[int]): Unix timestamp for the end of the data range (default: current time)
		interval (str): Time interval between data points. See _validate_interval for supported values.
						Default is 'hourly'.
		convert (List[str]): List of currencies to convert values to (max 3). Default is ['USD'].
	
	Returns:
		List[TokenState]: A list of TokenState objects containing historical price and market data
						 for the requested cryptocurrency at each time interval.
	
	Raises:
		ValueError: If neither id nor ticker is provided, if timestamps are invalid,
					if the interval is invalid, or if more than 3 conversion currencies are specified.
	"""
	if not id and not ticker:
		raise ValueError('Either id or ticker must be provided')

	# Check if the start timestamp is greater than the end timestamp
	if timestamp_start > timestamp_end:
		raise ValueError('The start timestamp occurr before than the end timestamp')

	# Check if the interval is valid
	_validate_interval(interval)

	# validate convert
	if (len(convert) > 3):
		raise ValueError('The convert list must have a maximum of 3 elements')

	params = {
		'time_start': timestamp_start,
		'time_end': timestamp_end,
		'interval': interval,
		'convert': ','.join(convert)
	}

	# use id if provided, otherwise use ticker
	if id:
		params['id'] = id
	else:
		params['symbol'] = ticker
		
	response = market._request('v3/cryptocurrency/quotes/historical', params=params)

	lst_token_states = []

	if id:
		# if we are querying by id, we get a simpler (although not completely simple)
		# structure to parse
		dct_quote_summary = response['data'][id]
	else:
		# if we query by ticker we get a differeint weird structure, we have to 
		# drill down into the quotes object for our ticker, we call this the quote 
	    # summary because it's the quotes, plus some extra
		# meta data we can extract for the TokenState object
		dct_quote_summary = response['data'][ticker][0]

	# and we also get some general meta-data that can go into the TokenState object
	try:
		if not id: 
			id = dct_quote_summary['id']
		name = dct_quote_summary['name']
		symbol = dct_quote_summary['symbol']
		is_active = dct_quote_summary['is_active'] == 1
		is_fiat = dct_quote_summary['is_fiat'] == 1
		
		# Verify quotes data exists
		if 'quotes' not in dct_quote_summary:
			raise KeyError('quotes')
		lst_quotes = dct_quote_summary['quotes']
	except KeyError as e:
		missing_field = str(e)
		raise ValueError(f"Required field '{missing_field}' is missing from API response. Response data might be malformed or incomplete.")
	
	# and the quotes themselves, still wrapped up in a list of convoluted stuff
	lst_quotes = dct_quote_summary['quotes']

	# for each quote block, we can create a token state
	for dct_quote_block in lst_quotes:

		# Parse the timestamp string into a datetime object
		timestamp_dt = parser.parse(dct_quote_block['timestamp'])

		# create a token state, the quotes are empty for now
		token_state = TokenState(
			id=int(id),
			name=name,
			symbol=symbol,
			last_updated=timestamp_dt,
			timestamp=int(timestamp_dt.timestamp()),
			is_active=is_active,
			quote_map={},
			is_fiat=is_fiat)

		# init each quote object and add it to the tokenstate
		for base_currency, dct_quote_data in dct_quote_block['quote'].items():
			quote = QuoteFactory.from_dict(base_currency, dct_quote_data)
			token_state.quote_map[base_currency] = quote
					
		lst_token_states.append(token_state)

	return lst_token_states
