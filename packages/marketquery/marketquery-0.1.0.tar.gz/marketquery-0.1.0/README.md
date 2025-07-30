# MarketQuery

A unified interface for market data APIs, providing a simple way to download historical market data from multiple providers.

## Features

- Support for multiple data providers:
  - Yahoo Finance (default)
  - Stooq
  - Tiingo
  - Alpha Vantage
  - Polygon.io
- Built-in caching system
- Consistent data format across providers
- Easy-to-use interface
- Support for multiple tickers
- Progress bars for long downloads

## Installation

```bash
pip install marketquery
```

## Quick Start

```python
import marketquery as mq

# Download data for a single ticker
data = mq.download('AAPL', start='2024-01-01', end='2024-01-31')

# Download data for multiple tickers
data = mq.download(['AAPL', 'GOOGL', 'MSFT'], start='2024-01-01', end='2024-01-31')

# Use a different provider
data = mq.download('AAPL', provider='tiingo', api_key='your_api_key')
```

## Environment Variables

MarketQuery supports configuration through environment variables. To use them:

1. Create a `.env` file in your project directory:
```bash
# Set default provider
MARKETQUERY_DEFAULT_PROVIDER=tiingo

# API keys for different providers
TIINGO_API_KEY=your_tiingo_api_key
ALPHA_VANTAGE_API_KEY=your_alpha_vantage_api_key
ALPHA_VANTAGE_PREMIUM_API_KEY=your_alpha_vantage_premium_api_key
```

2. Load the environment variables in your code:
```python
from dotenv import load_dotenv
load_dotenv()  # Load environment variables from .env file

import marketquery as mq
data = mq.download('AAPL')  # Will use settings from .env file
```

Available environment variables:
- `MARKETQUERY_DEFAULT_PROVIDER`: Set default provider (e.g., 'yahoo', 'tiingo', 'alpha_vantage')
- `TIINGO_API_KEY`: API key for Tiingo
- `ALPHA_VANTAGE_API_KEY`: API key for Alpha Vantage
- `ALPHA_VANTAGE_PREMIUM_API_KEY`: Premium API key for Alpha Vantage

## Documentation

For detailed documentation, run:
```python
import marketquery as mq
mq.help()
```

## Cache Management

MarketQuery includes a built-in caching system to improve performance and reduce API calls. The cache is stored in your system's cache directory:

- macOS: `~/Library/Caches/marketquery`
- Linux: `~/.cache/marketquery`
- Windows: `%LOCALAPPDATA%\marketquery\Cache`

You can control caching behavior with the following parameters:
- `load=True/False`: Enable/disable loading from cache
- `save=True/False`: Enable/disable saving to cache
- `cache_dir`: Specify a custom cache directory

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
