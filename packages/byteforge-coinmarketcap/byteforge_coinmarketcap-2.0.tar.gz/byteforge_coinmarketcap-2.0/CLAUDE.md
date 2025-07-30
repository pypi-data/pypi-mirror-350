# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This project is a Python SDK for the CoinMarketCap API. It's a fork of Martin Simon's 'coinmarketcap' module that has been extensively reworked to be compatible with the current CoinMarketCap API. The library provides access to cryptocurrency market data through various CoinMarketCap API endpoints.

## Development Commands

### Installation

```bash
# Install dependencies
pip install -r requirements.txt

# Install the package in development mode
pip install -e .
```

### Testing

```bash
# Run all tests (requires COIN_MARKET_CAP_API_KEY environment variable)
pytest tests/

# Run specific test file
pytest tests/test_coinmarketcap.py

# Run a specific test
pytest tests/test_coinmarketcap.py::test_listings_latest
```

Note: Tests require a valid CoinMarketCap API key set as an environment variable:
```bash
export COIN_MARKET_CAP_API_KEY=your_api_key_here
```

### Building and Publishing

```bash
# Clean build files
rm -rf dist/ build/ *.egg-info/

# Build the package
python -m build

# Upload to PyPI (requires credentials)
twine upload dist/*
```

## Project Architecture

The SDK is organized by API version and endpoint structure:

1. **Core Module** (`coinmarketcap/core.py`): Contains the main `Market` class that handles authentication, rate limiting, and caching.

2. **API Version Structure**:
   - `/v1/` - Version 1 endpoints
   - `/v2/` - Version 2 endpoints
   - `/v3/` - Version 3 endpoints

3. **Factories and Types**:
   - `types/` folder contains factory classes for creating data objects
   - Depends on the `byteforge-crypto-commons` package for base types

4. **Key Features**:
   - Request caching with `requests-cache`
   - Rate limiting with `requests-ratelimiter`
   - Support for multiple cryptocurrency quote conversions
   - Pagination and filtering options
   - Historical data retrieval

## Supported API Endpoints

- `v1/cryptocurrency/listings/latest`: Get latest market data for all cryptocurrencies
- `v1/cryptocurrency/map`: Get mapping of cryptocurrencies to CoinMarketCap IDs
- `v2/cryptocurrency/quotes/historical`: Get historical quotes (Hobbyist tier+)
- `v3/cryptocurrency/quotes/historical`: Enhanced historical quotes (Hobbyist tier+)

## Important Notes

- Free API key from CoinMarketCap only provides access to `listings_latest` and `map` endpoints
- Historical data requires a paid subscription (Hobbyist tier or higher)
- The API has rate limits that should be managed with the `rate_limit_per_minute` parameter
- Use the `safe_daily_call_limit()` method to track API usage against monthly limits