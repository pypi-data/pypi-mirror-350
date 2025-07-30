"""
Cache manager for market data
"""

import os
import json
import pickle
from datetime import datetime
from pathlib import Path
from typing import Optional, Dict, Any, Union
import pandas as pd
from appdirs import user_cache_dir


class CacheManager:
    """Manages caching of market data"""
    
    def __init__(self, cache_dir: Optional[str] = None):
        """
        Initialize cache manager
        
        Args:
            cache_dir: Optional custom cache directory. Defaults to platform-specific cache directory.
        """
        # Use appdirs to get the correct cache directory for the platform
        if cache_dir:
            # Expand environment variables in custom cache directory
            self.cache_dir = os.path.expandvars(cache_dir)
        else:
            # Use platform-specific cache directory
            self.cache_dir = user_cache_dir("marketquery")
            
        self._ensure_cache_structure()
    
    def _ensure_cache_structure(self):
        """Create cache directory structure if it doesn't exist"""
        # Create base cache directory
        Path(self.cache_dir).mkdir(parents=True, exist_ok=True)
        
        # Create provider directories
        for provider in ["stooq", "yahoo", "tiingo", "alpha_vantage", "polygon"]:
            Path(self.cache_dir, provider).mkdir(parents=True, exist_ok=True)
    
    def _get_cache_path(
        self,
        provider: str,
        symbol: str,
        start_date: str,
        end_date: str,
        interval: str
    ) -> str:
        """
        Get the cache path for the given parameters
        
        Args:
            provider: Provider name
            symbol: Ticker symbol
            start_date: Start date
            end_date: End date
            interval: Data interval
            
        Returns:
            Path to cache file
        """
        # Create filename from symbol only
        filename = f"{symbol}.pkl"
        
        # Create full path
        return os.path.join(
            self.cache_dir,
            provider,
            filename
        )
    
    def save_data(
        self,
        provider: str,
        symbol: str,
        start_date: str,
        end_date: str,
        interval: str,
        data: pd.DataFrame
    ) -> None:
        """
        Save data to cache
        
        Args:
            provider: Provider name
            symbol: Ticker symbol
            start_date: Start date
            end_date: End date
            interval: Data interval
            data: DataFrame to cache
        """
        # Create cache path
        data_path = self._get_cache_path(
            provider=provider,
            symbol=symbol,
            start_date=start_date,
            end_date=end_date,
            interval=interval
        )
        
        # Ensure directory exists
        os.makedirs(os.path.dirname(data_path), exist_ok=True)
        
        # Create metadata
        metadata = {
            "start_date": start_date,
            "end_date": end_date,
            "interval": interval,
            "cached_at": datetime.now().isoformat()
        }
        
        # Ensure data has symbol level in columns
        if isinstance(data.columns, pd.MultiIndex):
            if data.columns.names[0] != 'Symbol':
                data.columns = pd.MultiIndex.from_product([[symbol], data.columns], names=['Symbol', 'Field'])
        else:
            data.columns = pd.MultiIndex.from_product([[symbol], data.columns], names=['Symbol', 'Field'])
        
        # Save both data and metadata
        cache_data = {
            "metadata": metadata,
            "data": data
        }
        
        # Save to cache
        with open(data_path, 'wb') as f:
            pickle.dump(cache_data, f)
    
    def load_data(
        self,
        provider: str,
        symbol: str,
        start_date: str,
        end_date: str,
        interval: str
    ) -> Optional[pd.DataFrame]:
        """
        Load data from cache if available and valid
        
        Args:
            provider: Data provider
            symbol: Stock symbol
            start_date: Requested start date
            end_date: Requested end date
            interval: Requested interval
            
        Returns:
            Cached DataFrame if available and valid, None otherwise
        """
        data_path = self._get_cache_path(
            provider=provider,
            symbol=symbol,
            start_date=start_date,
            end_date=end_date,
            interval=interval
        )
        
        # Check if cache exists
        if not os.path.exists(data_path):
            return None
            
        try:
            # Load cache data
            with open(data_path, 'rb') as f:
                cache_data = pickle.load(f)
                
            # Check if metadata matches
            metadata = cache_data["metadata"]
            if (
                metadata["start_date"] == start_date and
                metadata["end_date"] == end_date and
                metadata["interval"] == interval
            ):
                return cache_data["data"]
                
            return None
            
        except Exception as e:
            return None
    
    def clear_cache(self, provider: Optional[str] = None):
        """
        Clear cache for a specific provider or all providers
        
        Args:
            provider: Optional provider to clear cache for. If None, clears all caches.
        """
        if provider:
            # Clear specific provider
            provider_path = Path(self.cache_dir, provider)
            if provider_path.exists():
                for file in provider_path.glob("*"):
                    file.unlink()
        else:
            # Clear all caches
            for provider_path in Path(self.cache_dir).glob("*"):
                if provider_path.is_dir():
                    for file in provider_path.glob("*"):
                        file.unlink() 
