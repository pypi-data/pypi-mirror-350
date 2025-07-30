from typing import List
from enum import Enum
from crypto_commons.types.token_info import TokenInfo
from coinmarketcap.types.token_info_factory import TokenInfoFactory

class ListingStatus(Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"
    UNTRACKED = "untracked"

class MapSortOption(Enum):
    ID = "id"
    CMC_RANK = "cmc_rank"


class MapAuxFields(Enum):
    PLATFORM = "platform"
    FIRST_HISTORICAL_DATA = "first_historical_data"
    LAST_HISTORICAL_DATA = "last_historical_data"
    IS_ACTIVE = "is_active"

def _map(market, 
         status: ListingStatus = ListingStatus.ACTIVE, 
         start: int = 1,
         limit: int = 100,
         symbols: List[str] = None,
         sort: MapSortOption = MapSortOption.ID, 
         aux_fields: List[MapAuxFields] = None):

    # quick and dirty test
    params = dict()
    params['listing_status'] = status.value
    params['start'] = start
    params['limit'] = limit
    params['sort'] = sort.value
    if symbols:
        params['symbol'] = ','.join(symbols)
    if aux_fields:
        params['aux'] = ','.join([field.value for field in aux_fields])

    response = market._request('v1/cryptocurrency/map', params=params)
   
    return [TokenInfoFactory.from_dict(item) for item in response['data']]