"""
Integration tests for the StooqProvider class
"""

import pytest
import pandas as pd
from marketquery import MarketDataClient, download as mq_download


class TestStooqProvider:
    """Integration test suite for StooqProvider"""
    
    def test_download_aapl_adjusted_client(self):
        """Test downloading adjusted AAPL data using MarketDataClient"""
        client = MarketDataClient(provider="stooq")
        
        # Download data for AAPL for the last month
        data = client.download(
            tickers="AAPL",
            start="2025-01-01",
            end="2025-01-31",
            load=False,  # Don't load from cache
            save=False   # Don't save to cache
        )
        
        # Verify the data
        assert isinstance(data, pd.DataFrame)
        assert not data.empty
        
        # Check the date range
        assert data.index.min() >= pd.Timestamp("2025-01-01")
        assert data.index.max() <= pd.Timestamp("2025-01-31")
        
        # Check the columns - Stooq provides adjusted prices by default
        expected_columns = ['adj_open', 'adj_high', 'adj_low', 'adj_close', 'volume']
        assert all(col in data.columns.levels[1] for col in expected_columns)
        
        # Check the data types
        assert all(data[('AAPL', col)].dtype in [float, int] for col in expected_columns)
        
        # Verify that we don't have unadjusted columns
        unadjusted_columns = ['open', 'high', 'low', 'close']
        assert not any(col in data.columns.levels[1] for col in unadjusted_columns)

    def test_download_aapl_adjusted_mq(self):
        """Test downloading adjusted AAPL data using mq.download()"""
        # Download data for AAPL for the last month
        data = mq_download(
            tickers="AAPL",
            start="2025-01-01",
            end="2025-01-31",
            load=False,  # Don't load from cache
            save=False,  # Don't save to cache
            provider="stooq"
        )
        
        # Verify the data
        assert isinstance(data, pd.DataFrame)
        assert not data.empty
        
        # Check the date range
        assert data.index.min() >= pd.Timestamp("2025-01-01")
        assert data.index.max() <= pd.Timestamp("2025-01-31")
        
        # Check the columns - Stooq provides adjusted prices by default
        expected_columns = ['adj_open', 'adj_high', 'adj_low', 'adj_close', 'volume']
        assert all(col in data.columns.levels[1] for col in expected_columns)
        
        # Check the data types
        assert all(data[('AAPL', col)].dtype in [float, int] for col in expected_columns)
        
        # Verify that we don't have unadjusted columns
        unadjusted_columns = ['open', 'high', 'low', 'close']
        assert not any(col in data.columns.levels[1] for col in unadjusted_columns)

    def test_download_with_invalid_symbol_client(self):
        """Test downloading data with both valid and invalid symbols using MarketDataClient"""
        client = MarketDataClient(provider="stooq")
        
        # Download data for valid symbols (AAPL, GOOGL) and invalid symbol (SQ)
        data = client.download(
            tickers=["AAPL", "GOOGL", "SQ"],
            start="2025-01-01",
            end="2025-03-01",
            load=False,
            save=False
        )
        
        # Verify the data structure
        assert isinstance(data, pd.DataFrame)
        
        # Check that all requested symbols are present in columns
        expected_symbols = ["AAPL", "GOOGL", "SQ"]
        assert all(symbol in data.columns.levels[0] for symbol in expected_symbols)
        
        # Check that all symbols have the same set of columns
        expected_columns = ['adj_open', 'adj_high', 'adj_low', 'adj_close', 'volume']
        for symbol in expected_symbols:
            assert all(col in data[symbol].columns for col in expected_columns)
        
        # Verify that valid symbols have data
        assert not data[("AAPL", "adj_close")].isna().all()
        assert not data[("GOOGL", "adj_close")].isna().all()
        
        # Verify that invalid symbol has all NaN values
        assert data[("SQ", "adj_close")].isna().all()
        
        # Check that all symbols have the same date index
        assert len(data.index) > 0  # Should have some dates
        for symbol in expected_symbols:
            assert all(data[("AAPL", "adj_close")].index == data[(symbol, "adj_close")].index)

    def test_download_with_invalid_symbol_mq(self):
        """Test downloading data with both valid and invalid symbols using mq.download()"""
        # Download data for valid symbols (AAPL, GOOGL) and invalid symbol (SQ)
        data = mq_download(
            tickers=["AAPL", "GOOGL", "SQ"],
            start="2025-01-01",
            end="2025-03-01",
            load=False,
            save=False,
            provider="stooq"
        )
        
        # Verify the data structure
        assert isinstance(data, pd.DataFrame)
        
        # Check that all requested symbols are present in columns
        expected_symbols = ["AAPL", "GOOGL", "SQ"]
        assert all(symbol in data.columns.levels[0] for symbol in expected_symbols)
        
        # Check that all symbols have the same set of columns
        expected_columns = ['adj_open', 'adj_high', 'adj_low', 'adj_close', 'volume']
        for symbol in expected_symbols:
            assert all(col in data[symbol].columns for col in expected_columns)
        
        # Verify that valid symbols have data
        assert not data[("AAPL", "adj_close")].isna().all()
        assert not data[("GOOGL", "adj_close")].isna().all()
        
        # Verify that invalid symbol has all NaN values
        assert data[("SQ", "adj_close")].isna().all()
        
        # Check that all symbols have the same date index
        assert len(data.index) > 0  # Should have some dates
        for symbol in expected_symbols:
            assert all(data[("AAPL", "adj_close")].index == data[(symbol, "adj_close")].index)
