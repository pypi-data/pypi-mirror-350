"""
Yahoo Finance provider implementation
"""

from typing import Dict, Any, Union, Optional, List
import pandas as pd
import yfinance as yf
from .base import BaseProvider

class YahooProvider(BaseProvider):
    """
    Yahoo Finance market data provider
    """
    
    def _standardize_dataframe(self, df: pd.DataFrame, ticker: str) -> pd.DataFrame:
        """Convert Yahoo Finance dataframe to standard format"""
        # Rename columns to standard format
        column_map = {
            'Open': 'open',
            'High': 'high',
            'Low': 'low',
            'Close': 'close',
            'Adj Close': 'adj_close',
            'Volume': 'volume',
            'Dividends': 'dividend',
            'Stock Splits': 'split'
        }

        # If DataFrame is empty, create one with the expected columns
        if df.empty:
            df = pd.DataFrame(columns=pd.MultiIndex.from_tuples([
                (ticker, col) for col in column_map.values()
            ]))
            return df

        # Swap levels to get ticker as first level
        df = df.swaplevel(axis=1)

        # Rename the second level columns
        df.columns = pd.MultiIndex.from_tuples([
            (ticker, column_map.get(col, col))
            for col in df.columns.get_level_values(1)
        ])

        return df

    def download(
        self,
        tickers: Union[str, List[str]],
        start: Optional[str] = None,
        end: Optional[str] = None,
        interval: str = "1d",
        **kwargs
    ) -> Optional[pd.DataFrame]:
        """
        Download market data from Yahoo Finance
        
        Args:
            tickers: Ticker symbol or list of ticker symbols
            start: Download start date string (YYYY-MM-DD) or _datetime
            end: Download end date string (YYYY-MM-DD) or _datetime
            interval: Data interval (e.g., "1d" for daily, "1h" for hourly)
            **kwargs: Additional Yahoo Finance specific parameters:
                - actions: Download stock dividends and stock splits events
                - threads: Use threads for mass downloading
                - ignore_tz: Ignore timezone when aligning data
                - group_by: Group by ticker or column
                - auto_adjust: Adjust all OHLC automatically
                - back_adjust: Back-adjusted data to mimic true historical prices
                - repair: Repair missing data
                - keepna: Keep NaN values
                - progress: Show download progress
                - period: Valid periods: 1d,5d,1mo,3mo,6mo,1y,2y,5y,10y,ytd,max
                - prepost: Include pre and post market data
                - proxy: Proxy URL scheme
                - rounding: Round values to 2 decimal places
                - timeout: Timeout for requests
                - session: Custom requests session
                
        Returns:
            pandas.DataFrame containing the market data or None if download fails
        """
        try:
            df = yf.download(
                tickers=tickers,
                start=start,
                end=end,
                interval=interval,
                **kwargs
            )

            # Standardize the dataframe format
            if isinstance(tickers, str):
                df = self._standardize_dataframe(df, tickers)
            else:
                # For multiple tickers, yfinance returns a multi-index dataframe
                # We need to standardize each ticker's columns
                dfs = []
                for ticker in tickers:
                    # Get all columns for this ticker at level 1
                    ticker_cols = df.columns[df.columns.get_level_values(1) == ticker]
                    if not ticker_cols.empty:
                        ticker_df = df[ticker_cols].copy()
                        ticker_df = self._standardize_dataframe(ticker_df, ticker)
                        dfs.append(ticker_df)
                    else:
                        # Create empty DataFrame with correct structure if ticker not found
                        ticker_df = pd.DataFrame()
                        ticker_df = self._standardize_dataframe(ticker_df, ticker)
                        dfs.append(ticker_df)
                df = pd.concat(dfs, axis=1)

            return df
                
        except Exception as e:
            # Handle rate limiting and other errors
            print(f"Error downloading {tickers}: {str(e)}")
            return None
