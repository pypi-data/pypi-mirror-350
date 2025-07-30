from typing import Dict
import json
import logging
from dateutil import parser
from crypto_commons.types.quote import Quote

class QuoteFactory:
    @staticmethod
    def from_dict(currency: str, dct_quote_data: Dict) -> 'Quote':
        if 'price' not in dct_quote_data:
            print(f"Payload: {json.dumps(dct_quote_data, indent=4)}")
            raise ValueError("Payload must contain 'price' field.")

        # insure integers are handled as floats (so 1 becomes 1.0)
        dct_quote_data['price'] = float(dct_quote_data['price'])

        # convert market_cap to float, if it's not a float, set it to -1.0
        try:
            dct_quote_data['market_cap'] = float(dct_quote_data['market_cap'])
        except TypeError as e:
            logging.warning(f"Error converting market_cap to float: {e}")
            dct_quote_data['market_cap'] = 0.0

        # Handle both 'last_updated' and 'timestamp' for the last_updated field
        if 'last_updated' in dct_quote_data:
            last_updated_str = dct_quote_data['last_updated']
        elif 'timestamp' in dct_quote_data:
            last_updated_str = dct_quote_data['timestamp']
        else:
            raise ValueError("Payload must contain either 'last_updated' or 'timestamp' field.")

        # Remove both possible keys to avoid errors in the constructor
        dct_quote_data.pop('last_updated', None)
        dct_quote_data.pop('timestamp', None)

        last_updated = parser.parse(last_updated_str)
        
        return Quote(base_currency=currency, last_updated=last_updated, **dct_quote_data)
