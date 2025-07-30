from typing import Dict
from datetime import datetime
from crypto_commons.types.token_info import TokenInfo

class TokenInfoFactory:
    @staticmethod
    def from_dict(data: Dict) -> 'TokenInfo':
        """Create a TokenInfo instance from a dictionary."""
        return TokenInfo(
            id=data['id'],
            rank=data.get('rank'),
            name=data['name'],
            symbol=data['symbol'],
            slug=data['slug'],
            is_active=data.get('is_active'),
            status=data['status'],
            first_historical_data=datetime.fromisoformat(data['first_historical_data'].replace('Z', '+00:00')) if 'first_historical_data' in data else None,
            last_historical_data=datetime.fromisoformat(data['last_historical_data'].replace('Z', '+00:00')) if 'last_historical_data' in data else None,
            platform=data.get('platform')
        ) 