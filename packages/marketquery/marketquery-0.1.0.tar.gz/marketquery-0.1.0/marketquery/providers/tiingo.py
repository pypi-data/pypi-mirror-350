"""
Tiingo provider implementation
"""

from typing import List, Optional, Union, Any
import pandas as pd
from tqdm import tqdm
from tiingo import TiingoClient
from concurrent.futures import ThreadPoolExecutor, as_completed
from ..constants import COLUMNS
from .base import BaseProvider


class TiingoProvider(BaseProvider):
    """
    Tiingo market data provider
    
    This provider uses the Tiingo API to fetch market data.
    An API key is required for all access.
    """
    
    def __init__(self, api_key: Optional[str] = None, premium_api_key: Optional[str] = None):
        """
        Initialize the Tiingo provider
        
        Args:
            api_key: Required API key for Tiingo
            premium_api_key: Not used - Tiingo does not have premium features
        """
        super().__init__(api_key, premium_api_key)
        if not api_key:
            raise ValueError("Tiingo requires an API key")
        config = {"api_key": api_key, "session": True}
        self.client = TiingoClient(config)

    def _standardize_dataframe(self, df: pd.DataFrame, ticker: str) -> pd.DataFrame:
        """Convert Tiingo dataframe to standard format"""
        # Rename columns to standard format
        column_map = {
            'open': 'open',
            'high': 'high',
            'low': 'low',
            'close': 'close',
            'volume': 'volume',
            'adjOpen': 'adj_open',
            'adjHigh': 'adj_high',
            'adjLow': 'adj_low',
            'adjClose': 'adj_close',
            'adjVolume': 'adj_volume',
            'divCash': 'dividend',
            'splitFactor': 'split'
        }
        
        # Only rename columns that exist in the dataframe
        existing_columns = {k: v for k, v in column_map.items() if k in df.columns}
        df = df.rename(columns=existing_columns)
        
        # Convert timezone-aware datetime to timezone-naive
        df.index = df.index.tz_localize(None)

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
            # Convert interval to Tiingo format
            interval_map = {
                "1d": "daily",
                "1wk": "weekly",
                "1mo": "monthly"
            }

            if interval not in interval_map:
                raise ValueError(f"Interval '{interval}' not supported by Tiingo")

            # Get data from Tiingo
            df = self.client.get_dataframe(
                ticker,
                startDate=start,
                endDate=end
            )

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
        Download market data from Tiingo
        
        Args:
            tickers: Single ticker symbol or list of ticker symbols
            start: Download start date string (YYYY-MM-DD) or _datetime
            end: Download end date string (YYYY-MM-DD) or _datetime
            actions: Download stock dividends and stock splits events
            threads: Use threads for mass downloading
            ignore_tz: Ignore timezone when aligning data from different exchanges
            group_by: Group by ticker or column
            auto_adjust: Use adjusted prices if True
            back_adjust: Back-adjusted data to mimic true historical prices
            repair: Repair missing data
            keepna: Keep NaN values
            progress: Show download progress
            period: Valid periods: 1d,5d,1mo,3mo,6mo,1y,2y,5y,10y,ytd,max
            interval: Valid intervals: 1d,1wk,1mo
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
