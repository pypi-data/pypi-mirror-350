"""
MarketQuery - A unified interface for market data APIs
"""

__version__ = "0.1.0"
__author__ = "troyscribner"
__license__ = "MIT"

from .client import MarketDataClient
from typing import List, Optional, Union, Any
import pandas as pd

__all__ = ["MarketDataClient", "download", "help", "clear_cache"]

def clear_cache():
    """
    Clear all cached data.
    
    This function creates a temporary client to clear the cache directory.
    """
    client = MarketDataClient()
    client.cache.clear_cache()

def help():
    """
    Display help information about MarketQuery.
    
    This function provides information about:
    - Available providers
    - Basic usage examples
    - Common parameters
    - Cache management
    - Environment variables
    """
    print("\nMarketQuery Help")
    print("===============\n")
    
    print("Quick Start:")
    print("-----------")
    print("import marketquery as mq")
    print("")
    print("# Download data for a single ticker")
    print("data = mq.download('AAPL', start='2024-01-01', end='2024-01-31')")
    print("")
    print("# Download data for multiple tickers")
    print("data = mq.download(['AAPL', 'GOOGL', 'MSFT'], start='2024-01-01', end='2024-01-31')")
    print("")
    print("# Use a different provider (e.g., Tiingo)")
    print("data = mq.download('AAPL', provider='tiingo', api_key='your_api_key')")
    print("")
    print("# Clear the cache")
    print("mq.clear_cache()")
    
    print("\nAvailable Providers:")
    print("-------------------")
    print("1. Yahoo Finance (default)")
    print("   - Free, no API key required")
    print("   - Supports most major exchanges")
    print("   - Rate limits may apply\n")
    
    print("2. Stooq")
    print("   - Free, no API key required")
    print("   - Limited to US stocks\n")
    
    print("3. Tiingo")
    print("   - Requires API key")
    print("   - Free tier available")
    print("   - Good for historical data\n")
    
    print("4. Alpha Vantage")
    print("   - Requires API key")
    print("   - Free tier available")
    print("   - Premium tier for adjusted prices\n")
    
    print("5. Polygon.io")
    print("   - Requires paid subscription")
    print("   - Professional-grade data\n")
    
    print("\nCommon Parameters:")
    print("----------------")
    print("tickers: Single ticker or list of tickers (e.g., 'AAPL' or ['AAPL', 'GOOGL'])")
    print("start: Start date (YYYY-MM-DD)")
    print("end: End date (YYYY-MM-DD)")
    print("provider: Data provider to use (default: 'yahoo' or set by MARKETQUERY_DEFAULT_PROVIDER)")
    print("api_key: API key for providers that require it")
    print("load: Load data from cache (default: True)")
    print("save: Save data to cache (default: True)")
    
    print("\nEnvironment Variables:")
    print("-------------------")
    print("To use environment variables, create a .env file in your project directory:")
    print("")
    print("# Set default provider")
    print("MARKETQUERY_DEFAULT_PROVIDER=tiingo")
    print("")
    print("# API keys for different providers")
    print("TIINGO_API_KEY=your_tiingo_api_key")
    print("ALPHA_VANTAGE_API_KEY=your_alpha_vantage_api_key")
    print("ALPHA_VANTAGE_PREMIUM_API_KEY=your_alpha_vantage_premium_api_key")
    print("")
    print("Then load the environment variables in your code:")
    print("from dotenv import load_dotenv")
    print("load_dotenv()  # Load environment variables from .env file")
    print("")
    print("Available environment variables:")
    print("- MARKETQUERY_DEFAULT_PROVIDER: Set default provider (e.g., 'yahoo', 'tiingo', 'alpha_vantage')")
    print("- TIINGO_API_KEY: API key for Tiingo")
    print("- ALPHA_VANTAGE_API_KEY: API key for Alpha Vantage")
    print("- ALPHA_VANTAGE_PREMIUM_API_KEY: Premium API key for Alpha Vantage")
    
    print("\nCache Management:")
    print("---------------")
    print("The cache is stored in your system's cache directory:")
    print("- macOS: ~/Library/Caches/marketquery")
    print("- Linux: ~/.cache/marketquery")
    print("- Windows: %LOCALAPPDATA%\\marketquery\\Cache")
    print("")
    print("To clear the cache:")
    print("mq.clear_cache()")
    print("")
    print("To disable caching:")
    print("data = mq.download('AAPL', load=False, save=False)")
    
    return None  # Explicitly return None to prevent it from being printed

def download(
    tickers: Union[str, List[str]],
    start: Optional[str] = None,
    end: Optional[str] = None,
    actions: bool = False,
    threads: bool = True,
    ignore_tz: Optional[bool] = None,
    group_by: str = 'column',
    auto_adjust: bool = False,
    back_adjust: bool = False,
    repair: bool = False,
    keepna: bool = False,
    progress: bool = True,
    period: str = "max",
    interval: str = "1d",
    prepost: bool = False,
    proxy: Optional[str] = None,
    rounding: bool = False,
    timeout: int = 10,
    session: Optional[Any] = None,
    provider: Optional[str] = None,
    api_key: Optional[str] = None,
    premium_api_key: Optional[str] = None,
    **kwargs
) -> pd.DataFrame:
    """
    Download market data for the given tickers.
    
    This function mirrors yfinance's download interface while adding support for
    multiple providers.
    
    Args:
        tickers: Single ticker symbol or list of ticker symbols
        start: Download start date string (YYYY-MM-DD) or _datetime
        end: Download end date string (YYYY-MM-DD) or _datetime
        actions: Download stock dividends and stock splits events
        threads: Use threads for mass downloading
        ignore_tz: Ignore timezone when aligning data from different exchanges
        group_by: Group by ticker or column
        auto_adjust: Adjust all OHLC automatically
        back_adjust: Back-adjusted data to mimic true historical prices
        repair: Repair missing data
        keepna: Keep NaN values
        progress: Show download progress
        period: Valid periods: 1d,5d,1mo,3mo,6mo,1y,2y,5y,10y,ytd,max
        interval: Valid intervals: 1m,2m,5m,15m,30m,60m,90m,1h,1d,5d,1wk,1mo,3mo
        prepost: Include pre and post market data
        proxy: Proxy URL scheme
        rounding: Round values to 2 decimal places
        timeout: Timeout for requests
        session: Custom requests session
        provider: Data provider to use (default: "yahoo")
        api_key: Optional API key for the provider
        premium_api_key: Optional premium API key for the provider
        **kwargs: Additional provider-specific parameters
        
    Returns:
        pandas.DataFrame containing the market data
        
    Raises:
        ValueError: If tickers is empty or invalid
    """
    client = MarketDataClient(
        provider=provider,
        api_key=api_key,
        premium_api_key=premium_api_key
    )
    
    return client.download(
        tickers=tickers,
        start=start,
        end=end,
        actions=actions,
        threads=threads,
        ignore_tz=ignore_tz,
        group_by=group_by,
        auto_adjust=auto_adjust,
        back_adjust=back_adjust,
        repair=repair,
        keepna=keepna,
        progress=progress,
        period=period,
        interval=interval,
        prepost=prepost,
        proxy=proxy,
        rounding=rounding,
        timeout=timeout,
        session=session,
        **kwargs
    ) 
