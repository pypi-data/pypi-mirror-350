"""
Alpha Vantage provider implementation
"""

import os
from typing import List, Optional, Union, Any
import pandas as pd
from tqdm import tqdm
from alpha_vantage.timeseries import TimeSeries
from ..constants import ALPHA_VANTAGE_COLUMNS, INTERVALS, ENV_VARS
from .base import BaseProvider


class AlphaVantageProvider(BaseProvider):
    """
    Alpha Vantage market data provider
    
    This provider supports both premium and regular API keys:
    - Premium key: ALPHA_VANTAGE_PREMIUM_API_KEY
    - Regular key: ALPHA_VANTAGE_API_KEY
    
    Premium keys provide access to adjusted prices and additional data.
    If a premium key is available, it will be used by default.
    """
    
    def __init__(self, api_key: Optional[str] = None, premium_api_key: Optional[str] = None):
        """
        Initialize the Alpha Vantage provider.
        
        Args:
            api_key: Optional regular API key for Alpha Vantage
            premium_api_key: Optional premium API key for Alpha Vantage
        """
        super().__init__(api_key=api_key, premium_api_key=premium_api_key)
        self._get_api_keys()
    
    def _get_api_keys(self) -> None:
        """Get API keys from various sources"""
        print(f"\nGetting API keys. Current state:")
        print(f"Constructor api_key: {self.api_key}")
        print(f"Constructor premium_api_key: {self.premium_api_key}")
        
        # If API keys were provided in constructor, use them
        if self.api_key or self.premium_api_key:
            print("Keys already in memory, returning")
            return
            
        # Try to get API keys from environment variables
        self.premium_api_key = os.getenv(ENV_VARS['premium_api_key'])
        self.api_key = os.getenv(ENV_VARS['api_key'])
        
        print(f"\nAfter environment check:")
        print(f"api_key: {self.api_key}")
        print(f"premium_api_key: {self.premium_api_key}")
        
        if self.premium_api_key or self.api_key:
            print("Found keys in environment, returning")
            return
            
        # Prompt user for API key
        print("\nAlpha Vantage API key is required.")
        print("You can get a free API key from: https://www.alphavantage.co/support/#api-key")
        print("For adjusted prices, a premium API key is required.")
        print("To avoid entering the API key each time, you can:")
        print("1. Pass it when creating the client: MarketDataClient(api_key='your_key')")
        print("2. Add it to your .env file:")
        print(f"   {ENV_VARS['premium_api_key']}=your_premium_key")
        print(f"   {ENV_VARS['api_key']}=your_key")
        
        premium_key = input("Enter your premium API key (press Enter to skip): ")
        if premium_key:
            self.premium_api_key = premium_key
        else:
            self.api_key = input("Enter your regular API key: ")
            
        print(f"\nFinal state:")
        print(f"api_key: {self.api_key}")
        print(f"premium_api_key: {self.premium_api_key}")
    
    def _get_time_series(self) -> TimeSeries:
        """Get TimeSeries instance with appropriate API key"""
        if self.premium_api_key:
            return TimeSeries(key=self.premium_api_key, output_format='pandas')
        return TimeSeries(key=self.api_key, output_format='pandas')
    
    def _standardize_dataframe(self, df: pd.DataFrame, ticker: str) -> pd.DataFrame:
        """Convert Alpha Vantage dataframe to standard format"""
        # Create a copy of the dataframe to avoid modifying the original
        df = df.copy()
        
        # Only keep columns that exist in our mapping
        valid_columns = [col for col in df.columns if col in ALPHA_VANTAGE_COLUMNS]
        df = df[valid_columns]
        
        # Rename columns to standard format
        df = df.rename(columns=ALPHA_VANTAGE_COLUMNS)
        
        # Create multi-index columns
        df.columns = pd.MultiIndex.from_product([[ticker], df.columns])
        
        return df
    
    def download(
        self,
        tickers: Union[str, List[str]],
        start: Optional[str] = None,
        end: Optional[str] = None,
        actions: bool = False,
        threads: bool = True,
        ignore_tz: Optional[bool] = None,
        group_by: str = 'column',
        auto_adjust: Optional[bool] = None,
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
        **kwargs
    ) -> Optional[pd.DataFrame]:
        """
        Download market data from Alpha Vantage
        
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
            **kwargs: Additional provider-specific parameters
            
        Returns:
            pandas.DataFrame containing the market data or None if download fails
        """
        if interval not in INTERVALS:
            raise ValueError(f"Interval '{interval}' not supported by Alpha Vantage")
            
        av_interval = INTERVALS[interval]
        
        # Initialize Alpha Vantage client
        ts = self._get_time_series()
        
        # Convert single ticker to list
        if isinstance(tickers, str):
            tickers = [tickers]
            
        # Download data for each ticker
        dfs = []
        ticker_iter = tickers if not progress else tqdm(tickers, desc="Downloading symbols")
        
        for ticker in ticker_iter:
            try:
                if av_interval in ["1min", "5min", "15min", "30min", "60min"]:
                    data, _ = ts.get_intraday(symbol=ticker, interval=av_interval, outputsize='full')
                elif av_interval == "daily":
                    # Use adjusted data if we have a premium key and auto_adjust is True
                    if self.premium_api_key and (auto_adjust is True or back_adjust):
                        data, _ = ts.get_daily_adjusted(symbol=ticker, outputsize='full')
                    else:
                        data, _ = ts.get_daily(symbol=ticker, outputsize='full')
                elif av_interval == "weekly":
                    data, _ = ts.get_weekly(symbol=ticker)
                elif av_interval == "monthly":
                    data, _ = ts.get_monthly(symbol=ticker)

                # Standardize dataframe format
                data = self._standardize_dataframe(data, ticker)
                
                # Filter by date range if specified
                if start:
                    data = data[data.index >= pd.to_datetime(start)]
                if end:
                    data = data[data.index <= pd.to_datetime(end)]
                    
                if not data.empty:
                    dfs.append(data)
                    
            except Exception as e:
                if "premium" in str(e).lower():
                    print(f"Warning: Premium API key required for adjusted data. Using unadjusted data for {ticker}.")
                    data, _ = ts.get_daily(symbol=ticker, outputsize='full')
                    data = self._standardize_dataframe(data, ticker)
                    if not data.empty:
                        dfs.append(data)
                else:
                    print(f"Error downloading {ticker}: {str(e)}")
            
        if not dfs:
            return None
            
        # Combine all dataframes
        if len(dfs) == 1:
            return self._handle_empty_dataframe(dfs[0], tickers)
        else:
            combined_df = pd.concat(dfs, axis=1)
            return self._handle_empty_dataframe(combined_df, tickers) 
