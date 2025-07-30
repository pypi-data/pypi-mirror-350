from typing import Dict
from crypto_commons.types.token_state import TokenState
from .quote_factory import QuoteFactory

class TokenStateFactory:
    @staticmethod
    def from_dict(data: Dict) -> 'TokenState':
        data = data.copy()

        # Convert 'is_market_cap_included_in_calc' from 0/1 to False/True
        if 'is_market_cap_included_in_calc' in data:
            data['is_market_cap_included_in_calc'] = bool(data['is_market_cap_included_in_calc'])

        quote_map = {}
        dct_quote_data = data.pop('quote')
        for currency, dct_quote_data in dct_quote_data.items():
            quote_map[currency] = QuoteFactory.from_dict(currency, dct_quote_data)
        data['quote_map'] = quote_map

        # Remap date_added to creation_date
        if 'date_added' in data:
            data['creation_date'] = data.pop('date_added')

        # Set optional attributes to None if not present in the data
        optional_fields = [
            'num_market_pairs', 'tags', 'max_supply', 'circulating_supply',
            'total_supply', 'platform', 'cmc_rank', 'self_reported_circulating_supply',
            'self_reported_market_cap', 'tvl_ratio', 'creation_date'
        ]

        for attr_name in optional_fields:
            if attr_name not in data:
                data[attr_name] = None

        return TokenState(**data)
