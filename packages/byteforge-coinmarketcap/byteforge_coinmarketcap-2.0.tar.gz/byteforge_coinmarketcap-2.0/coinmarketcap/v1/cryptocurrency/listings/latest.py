from typing import List
import time

from crypto_commons.types.token_state import TokenState
from .common import SortOption, AuxFields, SortDir, FilterOptions
from coinmarketcap.types.token_state_factory import TokenStateFactory

def _listings_latest(market, 
					sort_by: SortOption = SortOption.MARKET_CAP, 
					sort_dir: SortDir = SortDir.DESC, 
					start: int = 1, 
					limit: int = 100, 
					convert: List[str] = ['USD'],
					aux_fields: AuxFields = None, 
					filters: FilterOptions = None) -> List[TokenState]:
		
	params = {
		'sort': sort_by.value,
		'sort_dir': sort_dir.value,
		'start': start,
		'limit': limit
	}

	# validate convert
	if (len(convert) > 3):
		raise ValueError('The convert list must have a maximum of 3 elements')
		
	if convert:
		params['convert'] = ','.join(convert)

	if aux_fields:
		# Include the "aux" fields in the params
		aux_field_values = [field.value for field in aux_fields]
		params['aux'] = ','.join(aux_field_values)

	if filters:
		if filters.price_min is not None:
			params['price_min'] = filters.price_min
		if filters.price_max is not None:
			params['price_max'] = filters.price_max
		if filters.market_cap_min is not None:
			params['market_cap_min'] = filters.market_cap_min
		if filters.market_cap_max is not None:
			params['market_cap_max'] = filters.market_cap_max
		if filters.volume_24h_min is not None:
			params['volume_24h_min'] = filters.volume_24h_min
		if filters.volume_24h_max is not None:
			params['volume_24h_max'] = filters.volume_24h_max
		if filters.circulating_supply_min is not None:
			params['circulating_supply_min'] = filters.circulating_supply_min
		if filters.circulating_supply_max is not None:
			params['circulating_supply_max'] = filters.circulating_supply_max
		if filters.percent_change_24h_min is not None:
			params['percent_change_24h_min'] = filters.percent_change_24h_min
		if filters.percent_change_24h_max is not None:
			params['percent_change_24h_max'] = filters.percent_change_24h_max
		if filters.tags:
			params['tag'] = ','.join(filters.tags)

	response = market._request('v1/cryptocurrency/listings/latest', params=params, no_cache=True)

	token_states = []
	for dct_token in response['data']:
		# Add timestamp if not present (and not expected to be for this API)
		dct_token['timestamp'] = int(time.time())
		token_states.append(TokenStateFactory.from_dict(dct_token))

	return token_states
