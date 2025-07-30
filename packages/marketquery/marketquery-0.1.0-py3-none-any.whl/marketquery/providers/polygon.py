"""
Polygon.io provider implementation
"""

from typing import List, Optional, Union, Any
import pandas as pd
from tqdm import tqdm
from polygon import RESTClient
from ..constants import COLUMNS
from .base import BaseProvider
from concurrent.futures import ThreadPoolExecutor, as_completed


class PolygonProvider(BaseProvider):
    """
    Polygon.io market data provider
    
    This provider uses the Polygon.io API to fetch market data.
    An API key is required.
    """
    
    def __init__(self, api_key: Optional[str] = None, premium_api_key: Optional[str] = None):
        """
        Initialize the Polygon provider
        
        Args:
            api_key: Required API key for Polygon.io
            premium_api_key: Not used - Polygon.io does not have premium features
        """
        super().__init__(api_key, premium_api_key)
        if not api_key:
            raise ValueError("API key is required for Polygon.io")
        self.client = RESTClient(api_key=api_key)
    
    def _standardize_dataframe(self, df: pd.DataFrame, ticker: str) -> pd.DataFrame:
        """Convert Polygon.io dataframe to standard format"""
        # Rename columns to standard format
        column_map = {
            'o': 'open',
            'h': 'high',
            'l': 'low',
            'c': 'close',
            'v': 'volume',
            'vw': 'vwap',
            't': 'date'
        }
        
        # Only rename columns that exist in the dataframe
        existing_columns = {k: v for k, v in column_map.items() if k in df.columns}
        df = df.rename(columns=existing_columns)
        
        # Set date as index
        df['date'] = pd.to_datetime(df['date'], unit='ms')
        df.set_index('date', inplace=True)
        
        # Create multi-index columns
        df.columns = pd.MultiIndex.from_product([[ticker], df.columns])
        
        return df
    
    def _download_symbol(
        self,
        ticker: str,
        start: Optional[str],
        end: Optional[str],
        interval: str
    ) -> Optional[pd.DataFrame]:
        """Download data for a single symbol"""
        try:
            # Convert interval to Polygon format
            interval_map = {
                "1m": "minute",
                "5m": "minute",
                "15m": "minute",
                "30m": "minute",
                "60m": "minute",
                "1d": "day",
                "1wk": "week",
                "1mo": "month"
            }
            
            if interval not in interval_map:
                raise ValueError(f"Interval '{interval}' not supported by Polygon.io")
                
            # Get data from Polygon
            if interval_map[interval] == "minute":
                data = self.client.stocks_equities_aggregates(
                    ticker=ticker,
                    multiplier=1,
                    timespan=interval_map[interval],
                    from_=start,
                    to=end,
                    limit=50000
                )
            else:
                data = self.client.stocks_equities_aggregates(
                    ticker=ticker,
                    multiplier=1,
                    timespan=interval_map[interval],
                    from_=start,
                    to=end
                )
                
            # Convert to DataFrame
            df = pd.DataFrame(data.results)
            
            if df.empty:
                return None
                
            # Standardize dataframe format
            return self._standardize_dataframe(df, ticker)
            
        except Exception as e:
            print(f"Error downloading {ticker}: {str(e)}")
            return None
    
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
        Download market data from Polygon.io
        
        Args:
            tickers: Single ticker symbol or list of ticker symbols
            start: Download start date string (YYYY-MM-DD) or _datetime
            end: Download end date string (YYYY-MM-DD) or _datetime
            actions: Download stock dividends and stock splits events
            threads: Use threads for mass downloading
            ignore_tz: Ignore timezone when aligning data from different exchanges
            group_by: Group by ticker or column
            auto_adjust: Not used - Polygon.io provides unadjusted prices
            back_adjust: Not used - Polygon.io provides unadjusted prices
            repair: Repair missing data
            keepna: Keep NaN values
            progress: Show download progress
            period: Valid periods: 1d,5d,1mo,3mo,6mo,1y,2y,5y,10y,ytd,max
            interval: Valid intervals: 1m,5m,15m,30m,60m,1d,1wk,1mo
            prepost: Include pre and post market data
            proxy: Proxy URL scheme
            rounding: Round values to 2 decimal places
            timeout: Timeout for requests
            session: Custom requests session
            **kwargs: Additional provider-specific parameters
            
        Returns:
            pandas.DataFrame containing the market data or None if download fails
        """
        # Convert single ticker to list
        if isinstance(tickers, str):
            tickers = [tickers]
            
        if not threads or len(tickers) == 1:
            # Single-threaded download
            dfs = []
            ticker_iter = tickers if not progress else tqdm(tickers, desc="Downloading symbols")
            
            for ticker in ticker_iter:
                df = self._download_symbol(ticker, start, end, interval)
                if df is not None:
                    dfs.append(df)
        else:
            # Multi-threaded download with fixed pool size (like yfinance)
            dfs = []
            with ThreadPoolExecutor(max_workers=3) as executor:
                # Submit all download tasks
                future_to_ticker = {
                    executor.submit(self._download_symbol, ticker, start, end, interval): ticker
                    for ticker in tickers
                }
                
                # Process results as they complete
                if progress:
                    futures = tqdm(as_completed(future_to_ticker), total=len(tickers), desc="Downloading symbols")
                else:
                    futures = as_completed(future_to_ticker)
                
                for future in futures:
                    df = future.result()
                    if df is not None:
                        dfs.append(df)
            
        if not dfs:
            return None
            
        # Combine all dataframes
        if len(dfs) == 1:
            return self._handle_empty_dataframe(dfs[0], tickers)
        else:
            combined_df = pd.concat(dfs, axis=1)
            return self._handle_empty_dataframe(combined_df, tickers) 
