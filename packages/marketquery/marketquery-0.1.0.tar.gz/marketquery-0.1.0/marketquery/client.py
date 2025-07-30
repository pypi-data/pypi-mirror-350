"""
MarketDataClient - Main client class for interacting with market data providers
"""

from typing import Dict, List, Optional, Union, Any
from tqdm import tqdm
import pandas as pd
import os
from .providers.base import BaseProvider
from .providers.yahoo import YahooProvider
from .providers.alpha_vantage import AlphaVantageProvider
from .providers.stooq import StooqProvider
from .providers.polygon import PolygonProvider
from .providers.tiingo import TiingoProvider
from .cache import CacheManager
from .constants import ENV_VARS

class MarketDataClient:
    """
    Main client class for interacting with market data providers.
    
    This class provides a unified interface for downloading market data
    from various providers. It handles provider initialization and data
    retrieval in a consistent way.
    """
    
    def __init__(
        self,
        provider: str = "yahoo",
        api_key: Optional[str] = None,
        premium_api_key: Optional[str] = None,
        cache_dir: Optional[str] = None
    ):
        """
        Initialize the MarketDataClient
        
        Args:
            provider: Name of the provider to use (default: "yahoo")
            api_key: Optional API key for the provider
            premium_api_key: Optional premium API key for the provider
            cache_dir: Optional directory to store cached data
        """
        self.provider = self._get_provider(provider, api_key, premium_api_key)
        self.cache = CacheManager(cache_dir)
    
    def _get_provider(self, provider: str, api_key: Optional[str], premium_api_key: Optional[str]) -> BaseProvider:
        """
        Get the appropriate provider instance.
        
        Args:
            provider: Name of the provider
            api_key: Optional API key
            premium_api_key: Optional premium API key
            
        Returns:
            BaseProvider instance
            
        Raises:
            ValueError: If provider is not supported
        """
        providers = {
            "yahoo": YahooProvider,
            "alpha_vantage": AlphaVantageProvider,
            "stooq": StooqProvider,
            "polygon": PolygonProvider,
            "tiingo": TiingoProvider
        }
        
        if provider not in providers:
            raise ValueError(f"Provider '{provider}' not supported. Available providers: {list(providers.keys())}")
            
        # Stooq doesn't need an API key
        if provider == "stooq":
            return providers[provider]()
            
        # Check for API key in environment variables if not provided
        if api_key is None:
            if provider == "tiingo":
                api_key = os.getenv('TIINGO_API_KEY')
            elif provider == "alpha_vantage":
                api_key = os.getenv('ALPHA_VANTAGE_API_KEY')
                if premium_api_key is None:  # Only get from env if not provided in constructor
                    premium_api_key = os.getenv('ALPHA_VANTAGE_PREMIUM_API_KEY')
            
        return providers[provider](api_key=api_key, premium_api_key=premium_api_key)
    
    def download(
        self,
        tickers: Union[str, List[str]],
        start: Optional[str] = None,
        end: Optional[str] = None,
        interval: str = "1d",
        save: bool = True,
        load: bool = True,
        **kwargs
    ) -> pd.DataFrame:
        """
        Download market data for the given tickers.
        
        Args:
            tickers: Single ticker symbol or list of ticker symbols
            start: Download start date string (YYYY-MM-DD) or _datetime
            end: Download end date string (YYYY-MM-DD) or _datetime
            interval: Data interval (e.g., "1d" for daily, "1h" for hourly)
            save: Whether to save downloaded data to cache
            load: Whether to load data from cache if available
            **kwargs: Provider-specific parameters
            
        Returns:
            pandas.DataFrame containing the market data
            
        Raises:
            ValueError: If tickers is empty or invalid
        """
        # Convert single ticker to list
        if isinstance(tickers, str):
            tickers = [tickers]
            
        if not tickers:
            raise ValueError("No tickers provided")
            
        # Check cache for each symbol
        cached_symbols = []
        uncached_symbols = []
        cached_dfs = []
        
        if load:
            for ticker in tickers:
                cached_data = self.cache.load_data(
                    provider=self.provider.__class__.__name__.lower().replace("provider", ""),
                    symbol=ticker,
                    start_date=start or "max",
                    end_date=end or "today",
                    interval=interval
                )
                if cached_data is not None:
                    cached_symbols.append(ticker)
                    cached_dfs.append(cached_data)
                else:
                    uncached_symbols.append(ticker)
        else:
            # If load=False, all symbols need to be downloaded
            uncached_symbols = tickers

        print(uncached_symbols)

        # If we have uncached symbols, download them in a batch
        if uncached_symbols:
            if kwargs.get('progress', True):
                print(f"Downloading {len(uncached_symbols)} symbols: {', '.join(uncached_symbols)}")
                
            fresh_df = self.provider.download(
                tickers=uncached_symbols,
                start=start,
                end=end,
                interval=interval,
                **kwargs
            )
            
            if fresh_df is None:
                raise Exception("No data was successfully downloaded")
                
            # Save each symbol to cache separately
            if save:
                for ticker in uncached_symbols:
                    if ticker in fresh_df.columns.levels[0]:
                        ticker_df = fresh_df[ticker]
                        self.cache.save_data(
                            provider=self.provider.__class__.__name__.lower().replace("provider", ""),
                            symbol=ticker,
                            data=ticker_df,
                            start_date=start or "max",
                            end_date=end or "today",
                            interval=interval
                        )
            
            cached_dfs.append(fresh_df)
        
        # Combine all dataframes
        if not cached_dfs:
            raise Exception("No data was successfully downloaded")
            
        if len(cached_dfs) == 1:
            df = cached_dfs[0]
        else:
            df = pd.concat(cached_dfs, axis=1)
            
        # Show summary
        if kwargs.get('progress', True):
            if cached_symbols:
                print(f"Loaded {len(cached_symbols)} symbols from cache: {', '.join(cached_symbols)}")
            if uncached_symbols:
                print(f"Downloaded {len(uncached_symbols)} symbols: {', '.join(uncached_symbols)}")
                
        return df
    
    def clear_cache(self, provider: Optional[str] = None):
        """
        Clear cache for a specific provider or all providers
        
        Args:
            provider: Optional provider to clear cache for. If None, clears all caches.
        """
        self.cache.clear_cache(provider) 
