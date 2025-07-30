"""
Stooq provider implementation
"""

from typing import List, Optional, Union, Any
import io
import pandas as pd
import requests
from concurrent.futures import ThreadPoolExecutor, as_completed
from tqdm import tqdm
from ..constants import COLUMNS
from .base import BaseProvider


class StooqProvider(BaseProvider):
    """
    Stooq market data provider
    
    This provider uses the Stooq API to fetch market data.
    No API key is required.
    """
    
    BASE_URL = "https://stooq.com/q/d/l/"
    
    def __init__(self, api_key: Optional[str] = None, premium_api_key: Optional[str] = None):
        """
        Initialize the Stooq provider
        
        Args:
            api_key: Not used - Stooq does not require an API key
            premium_api_key: Not used - Stooq does not have premium features
        """
        super().__init__(api_key, premium_api_key)
        self.session = requests.Session()
    
    def _get_url(self, ticker: str, interval: str, start: Optional[str] = None, end: Optional[str] = None) -> str:
        """Construct the Stooq API URL"""
        # Convert interval to Stooq format
        interval_map = {
            "1d": "d",  # daily
            "1wk": "w",  # weekly
            "1mo": "m",  # monthly
        }
        
        if interval not in interval_map:
            raise ValueError(f"Interval '{interval}' not supported by Stooq")
            
        stooq_interval = interval_map[interval]
        
        # Add .US suffix for US stocks
        if not any(ticker.endswith(suffix) for suffix in ['.US', '.L', '.DE', '.F', '.PA', '.BE', '.DU', '.HM', '.HA', '.MU', '.SG', '.SI', '.SR', '.ST', '.CO', '.MX', '.V', '.TO', '.CN']):
            ticker = f"{ticker}.US"
        
        # Construct URL
        url = f"{self.BASE_URL}?s={ticker}&i={stooq_interval}"
        
        # Add date range if specified
        if start:
            url += f"&d1={start.replace('-', '')}"
        if end:
            url += f"&d2={end.replace('-', '')}"
            
        return url
    
    def _standardize_dataframe(self, df: pd.DataFrame, ticker: str) -> pd.DataFrame:
        """Convert Stooq dataframe to standard format"""
        # Rename columns to standard format
        column_map = {
            'Date': 'date',
            'Open': 'adj_open',    # Stooq provides adjusted prices
            'High': 'adj_high',    # Stooq provides adjusted prices
            'Low': 'adj_low',      # Stooq provides adjusted prices
            'Close': 'adj_close',  # Stooq provides adjusted prices
            'Volume': 'volume'     # Volume is not adjusted
        }
        
        # Only rename columns that exist in the dataframe
        existing_columns = {k: v for k, v in column_map.items() if k in df.columns}
        df = df.rename(columns=existing_columns)
        
        # Set date as index
        df['date'] = pd.to_datetime(df['date'])
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
            # Get data from Stooq
            url = self._get_url(ticker, interval, start, end)
            response = self.session.get(url, timeout=30)
            
            if response.status_code != 200:
                return None
                
            # Parse CSV data
            df = pd.read_csv(io.StringIO(response.text))
            
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
        Download market data from Stooq
        
        Args:
            tickers: Single ticker symbol or list of ticker symbols
            start: Download start date string (YYYY-MM-DD) or _datetime
            end: Download end date string (YYYY-MM-DD) or _datetime
            actions: Download stock dividends and stock splits events
            threads: Use threads for mass downloading
            ignore_tz: Ignore timezone when aligning data from different exchanges
            group_by: Group by ticker or column
            auto_adjust: Not used - Stooq only provides adjusted prices
            back_adjust: Not used - Stooq only provides adjusted prices
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

        # Combine all dataframes
        if not dfs:
            return self._handle_empty_dataframe(None, tickers)
        elif len(dfs) == 1:
            return self._handle_empty_dataframe(dfs[0], tickers)
        else:
            combined_df = pd.concat(dfs, axis=1)
            return self._handle_empty_dataframe(combined_df, tickers) 
