"""
Base provider class for market data providers
"""

from abc import ABC, abstractmethod
from typing import List, Optional, Union, Any
import pandas as pd


class BaseProvider(ABC):
    """
    Base class for market data providers
    
    This class defines the interface that all market data providers must implement.
    """
    
    def __init__(self, api_key: Optional[str] = None, premium_api_key: Optional[str] = None):
        """
        Initialize the provider
        
        Args:
            api_key: Optional API key for the provider
            premium_api_key: Optional premium API key for the provider
        """
        self.api_key = api_key
        self.premium_api_key = premium_api_key
    
    def _handle_empty_dataframe(self, df: pd.DataFrame, tickers: List[str]) -> pd.DataFrame:
        """
        Handle empty dataframes and ensure all requested tickers are present
        
        Args:
            df: The dataframe to handle
            tickers: List of requested tickers
            
        Returns:
            DataFrame with all requested tickers, using NaN for missing data
        """
        if df is None or df.empty:
            # Create empty DataFrame with correct structure
            df = pd.DataFrame(index=pd.DatetimeIndex([]))
            df.columns = pd.MultiIndex.from_product([tickers, ['adj_open', 'adj_high', 'adj_low', 'adj_close', 'volume']])
            return df
            
        # Check if all requested tickers are present
        missing_tickers = set(tickers) - set(df.columns.levels[0])
        if missing_tickers:
            # Create empty columns for missing tickers
            empty_df = pd.DataFrame(index=df.index)
            empty_df.columns = pd.MultiIndex.from_product([missing_tickers, ['adj_open', 'adj_high', 'adj_low', 'adj_close', 'volume']])
            df = pd.concat([df, empty_df], axis=1)
            
        return df
    
    @abstractmethod
    def download(
        self,
        tickers: Union[str, List[str]],
        start: Optional[str] = None,
        end: Optional[str] = None,
        interval: str = "1d",
        **kwargs
    ) -> Optional[pd.DataFrame]:
        """
        Download market data for the given tickers.
        
        Args:
            tickers: Single ticker symbol or list of ticker symbols
            start: Download start date string (YYYY-MM-DD) or _datetime
            end: Download end date string (YYYY-MM-DD) or _datetime
            interval: Data interval (e.g., "1d" for daily, "1h" for hourly)
            **kwargs: Provider-specific parameters
            
        Returns:
            pandas.DataFrame containing the market data or None if download fails
        """
        raise NotImplementedError("Provider must implement download method")
