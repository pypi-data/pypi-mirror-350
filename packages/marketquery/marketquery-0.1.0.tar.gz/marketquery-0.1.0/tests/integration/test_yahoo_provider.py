"""
Integration tests for the YahooProvider class
"""

import pytest
import pandas as pd
from marketquery import MarketDataClient, download as mq_download


class TestYahooProvider:
    """Integration test suite for YahooProvider"""
    
    def test_download_aapl_unadjusted_client(self):
        """Test downloading unadjusted AAPL data using MarketDataClient"""
        client = MarketDataClient(provider="yahoo")
        
        # Download data for AAPL for the last month
        data = client.download(
            tickers="AAPL",
            start="2025-01-01",
            end="2025-01-31",
            auto_adjust=False,  # Get unadjusted prices
            load=False,  # Don't load from cache
            save=False   # Don't save to cache
        )
        
        # Verify the data
        assert isinstance(data, pd.DataFrame)
        assert not data.empty
        
        # Check the date range
        assert data.index.min() >= pd.Timestamp("2025-01-01")
        assert data.index.max() <= pd.Timestamp("2025-01-31")
        
        # Check the columns - Yahoo Finance provides unadjusted prices when auto_adjust=False
        expected_columns = ['open', 'high', 'low', 'close', 'adj_close', 'volume']
        assert all(col in data.columns.levels[1] for col in expected_columns)
        
        # Check the data types
        assert all(data[('AAPL', col)].dtype in [float, int] for col in expected_columns)
        
        # Verify that we don't have adjusted columns
        adjusted_columns = ['adj_open', 'adj_high', 'adj_low']
        assert not any(col in data.columns.levels[1] for col in adjusted_columns)

    def test_download_aapl_unadjusted_mq(self):
        """Test downloading unadjusted AAPL data using mq.download()"""
        # Download data for AAPL for the last month
        data = mq_download(
            tickers="AAPL",
            start="2025-01-01",
            end="2025-01-31",
            auto_adjust=False,  # Get unadjusted prices
            load=False,  # Don't load from cache
            save=False,  # Don't save to cache
            provider="yahoo"
        )
        
        # Verify the data
        assert isinstance(data, pd.DataFrame)
        assert not data.empty
        
        # Check the date range
        assert data.index.min() >= pd.Timestamp("2025-01-01")
        assert data.index.max() <= pd.Timestamp("2025-01-31")
        
        # Check the columns - Yahoo Finance provides unadjusted prices when auto_adjust=False
        expected_columns = ['open', 'high', 'low', 'close', 'adj_close', 'volume']
        assert all(col in data.columns.levels[1] for col in expected_columns)
        
        # Check the data types
        assert all(data[('AAPL', col)].dtype in [float, int] for col in expected_columns)
        
        # Verify that we don't have adjusted columns
        adjusted_columns = ['adj_open', 'adj_high', 'adj_low']
        assert not any(col in data.columns.levels[1] for col in adjusted_columns)

    def test_download_with_invalid_symbol_client(self):
        """Test downloading data with both valid and invalid symbols using MarketDataClient"""
        client = MarketDataClient(provider="yahoo")
        
        # Download data for valid symbols (AAPL, GOOGL) and invalid symbol (SQ)
        data = client.download(
            tickers=["AAPL", "GOOGL", "SQ"],
            start="2025-01-01",
            end="2025-03-01",
            auto_adjust=False,
            load=False,
            save=False
        )
        
        # Verify the data structure
        assert isinstance(data, pd.DataFrame)
        
        # Check that all requested symbols are present in columns
        expected_symbols = ["AAPL", "GOOGL", "SQ"]
        assert all(symbol in data.columns.levels[0] for symbol in expected_symbols)
        
        # Check that all symbols have the same set of columns
        expected_columns = ['open', 'high', 'low', 'close', 'adj_close', 'volume']
        for symbol in expected_symbols:
            assert all(col in data[symbol].columns for col in expected_columns)
        
        # Verify that valid symbols have data
        assert not data[("AAPL", "close")].isna().all()
        assert not data[("GOOGL", "close")].isna().all()
        
        # Verify that invalid symbol has all NaN values
        assert data[("SQ", "close")].isna().all()
        
        # Check that all symbols have the same date index
        assert len(data.index) > 0  # Should have some dates
        for symbol in expected_symbols:
            assert all(data[("AAPL", "close")].index == data[(symbol, "close")].index)

    def test_download_with_invalid_symbol_mq(self):
        """Test downloading data with both valid and invalid symbols using mq.download()"""
        # Download data for valid symbols (AAPL, GOOGL) and invalid symbol (SQ)
        data = mq_download(
            tickers=["AAPL", "GOOGL", "SQ"],
            start="2025-01-01",
            end="2025-03-01",
            auto_adjust=False,
            load=False,
            save=False,
            provider="yahoo"
        )
        
        # Verify the data structure
        assert isinstance(data, pd.DataFrame)
        
        # Check that all requested symbols are present in columns
        expected_symbols = ["AAPL", "GOOGL", "SQ"]
        assert all(symbol in data.columns.levels[0] for symbol in expected_symbols)
        
        # Check that all symbols have the same set of columns
        expected_columns = ['open', 'high', 'low', 'close', 'adj_close', 'volume']
        for symbol in expected_symbols:
            assert all(col in data[symbol].columns for col in expected_columns)
        
        # Verify that valid symbols have data
        assert not data[("AAPL", "close")].isna().all()
        assert not data[("GOOGL", "close")].isna().all()
        
        # Verify that invalid symbol has all NaN values
        assert data[("SQ", "close")].isna().all()
        
        # Check that all symbols have the same date index
        assert len(data.index) > 0  # Should have some dates
        for symbol in expected_symbols:
            assert all(data[("AAPL", "close")].index == data[(symbol, "close")].index)
