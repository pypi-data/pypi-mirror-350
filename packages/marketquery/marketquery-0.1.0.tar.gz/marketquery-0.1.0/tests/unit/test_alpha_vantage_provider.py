"""
Unit tests for the AlphaVantageProvider class
"""

import os
import pytest
import pandas as pd
from unittest.mock import patch, MagicMock
from marketquery import MarketDataClient
from marketquery.constants import ALPHA_VANTAGE_COLUMNS


class TestAlphaVantageProvider:
    """Unit test suite for AlphaVantageProvider"""
    
    @pytest.fixture
    def mock_alpha_vantage(self):
        """Mock Alpha Vantage API responses"""
        with patch('marketquery.providers.alpha_vantage.AlphaVantageProvider._get_time_series') as mock_ts:
            # Create mock data for unadjusted prices
            mock_unadjusted = pd.DataFrame({
                '1. open': [100.0, 101.0],
                '2. high': [102.0, 103.0],
                '3. low': [99.0, 100.0],
                '4. close': [101.0, 102.0],
                '5. volume': [1000000, 1100000]
            }, index=pd.date_range('2023-01-01', periods=2))
            
            # Create mock data for adjusted prices
            mock_adjusted = pd.DataFrame({
                '1. open': [100.0, 101.0],
                '2. high': [102.0, 103.0],
                '3. low': [99.0, 100.0],
                '4. close': [101.0, 102.0],
                '5. adjusted close': [100.5, 101.5],
                '6. volume': [1000000, 1100000],
                '7. dividend amount': [0.0, 0.5],
                '8. split coefficient': [1.0, 1.0]
            }, index=pd.date_range('2023-01-01', periods=2))
            
            # Create a mock TimeSeries instance
            mock_ts_instance = MagicMock()
            
            # Set up mock methods to return different data based on the method called
            def get_daily_adjusted(*args, **kwargs):
                return (mock_adjusted, None)
                
            def get_daily(*args, **kwargs):
                return (mock_unadjusted, None)
                
            mock_ts_instance.get_daily_adjusted = get_daily_adjusted
            mock_ts_instance.get_daily = get_daily
            mock_ts_instance.get_intraday.return_value = (mock_unadjusted, None)
            mock_ts_instance.get_weekly.return_value = (mock_unadjusted, None)
            mock_ts_instance.get_monthly.return_value = (mock_unadjusted, None)
            
            # Set the mock to return our mock instance
            mock_ts.return_value = mock_ts_instance
            yield mock_ts
    
    @pytest.fixture
    def mock_input(self):
        """Mock the input function to avoid stdin capture issues"""
        with patch('builtins.input', return_value=""):
            yield
    
    def test_premium_api_key_from_constructor(self, mock_alpha_vantage, mock_input):
        """Test premium API key provided in constructor"""
        premium_key = "premium_key"
        client = MarketDataClient(provider="alpha_vantage", premium_api_key=premium_key)
        
        # Get the TimeSeries instance to trigger the mock
        ts = client.provider._get_time_series()
        
        # Verify premium API key was passed to Alpha Vantage
        mock_alpha_vantage.assert_called_once()
        
        # Test data download with adjusted prices
        data = client.download(tickers="AAPL", auto_adjust=True, load=False, save=False)
        assert isinstance(data, pd.DataFrame)
        assert not data.empty
        assert "adj_close" in data.columns.levels[1]
        assert "dividend" in data.columns.levels[1]
        assert "split" in data.columns.levels[1]
    
    def test_regular_api_key_from_constructor(self, mock_alpha_vantage, mock_input):
        """Test regular API key provided in constructor"""
        regular_key = "regular_key"
        client = MarketDataClient(provider="alpha_vantage", api_key=regular_key)

        # Get the TimeSeries instance to trigger the mock
        ts = client.provider._get_time_series()

        # Verify _get_time_series was called
        mock_alpha_vantage.assert_called_once()

        # Test data download with unadjusted prices
        data = client.download(tickers="AAPL", auto_adjust=False, load=False, save=False)
        assert isinstance(data, pd.DataFrame)
        assert not data.empty
        assert "close" in data.columns.levels[1]
        assert "adj_close" not in data.columns.levels[1]
        assert "dividend" not in data.columns.levels[1]
        assert "split" not in data.columns.levels[1]

    def test_premium_api_key_from_env(self, mock_alpha_vantage, mock_input, monkeypatch):
        """Test premium API key from environment variable"""
        premium_key = "premium_key"
        monkeypatch.setenv("ALPHA_VANTAGE_PREMIUM_API_KEY", premium_key)

        client = MarketDataClient(provider="alpha_vantage")

        # Get the TimeSeries instance to trigger the mock
        ts = client.provider._get_time_series()

        # Verify premium API key was passed to Alpha Vantage
        mock_alpha_vantage.assert_called_once()

        # Test data download with adjusted prices
        data = client.download(tickers="AAPL", auto_adjust=True, load=False, save=False)
        assert isinstance(data, pd.DataFrame)
        assert not data.empty
        assert "adj_close" in data.columns.levels[1]
        assert "dividend" in data.columns.levels[1]
        assert "split" in data.columns.levels[1]

    def test_regular_api_key_from_env(self, mock_alpha_vantage, mock_input, monkeypatch):
        """Test regular API key from environment variable"""
        regular_key = "regular_key"
        monkeypatch.setenv("ALPHA_VANTAGE_API_KEY", regular_key)

        client = MarketDataClient(provider="alpha_vantage")

        # Get the TimeSeries instance to trigger the mock
        ts = client.provider._get_time_series()

        # Verify regular API key was passed to Alpha Vantage
        mock_alpha_vantage.assert_called_once()

        # Test data download with unadjusted prices
        data = client.download(tickers="AAPL", auto_adjust=False, load=False, save=False)
        assert isinstance(data, pd.DataFrame)
        assert not data.empty
        assert "close" in data.columns.levels[1]
        assert "adj_close" not in data.columns.levels[1]
        assert "dividend" not in data.columns.levels[1]
        assert "split" not in data.columns.levels[1]

    def test_api_key_prompt(self, mock_alpha_vantage, monkeypatch):
        """Test API key prompt when no key is provided"""
        # Clear environment variables
        monkeypatch.delenv("ALPHA_VANTAGE_API_KEY", raising=False)
        monkeypatch.delenv("ALPHA_VANTAGE_PREMIUM_API_KEY", raising=False)

        # Mock input function to return a key
        with patch('builtins.input', return_value="prompted_key"):
            client = MarketDataClient(provider="alpha_vantage")

            # Get the TimeSeries instance to trigger the mock
            ts = client.provider._get_time_series()

            # Verify prompted key was passed to Alpha Vantage
            mock_alpha_vantage.assert_called_once()

            # Test data download with unadjusted prices
            data = client.download(tickers="AAPL", auto_adjust=False, load=False, save=False)
            assert isinstance(data, pd.DataFrame)
            assert not data.empty
            assert "close" in data.columns.levels[1]
            assert "adj_close" not in data.columns.levels[1]
            assert "dividend" not in data.columns.levels[1]
            assert "split" not in data.columns.levels[1]

    def test_premium_fallback_to_regular(self, mock_alpha_vantage, mock_input):
        """Test fallback to regular API when premium fails"""
        premium_key = "premium_key"
        regular_key = "regular_key"

        # Track calls to our mock methods
        daily_adjusted_called = False
        daily_called = False

        def get_daily_adjusted(*args, **kwargs):
            nonlocal daily_adjusted_called
            daily_adjusted_called = True
            raise Exception("Premium API error")

        def get_daily(*args, **kwargs):
            nonlocal daily_called
            daily_called = True
            return (pd.DataFrame({
                '1. open': [100.0, 101.0],
                '2. high': [102.0, 103.0],
                '3. low': [99.0, 100.0],
                '4. close': [101.0, 102.0],
                '5. volume': [1000000, 1100000]
            }, index=pd.date_range('2023-01-01', periods=2)), None)

        # Set up the mock instance with our tracking functions
        mock_ts_instance = mock_alpha_vantage.return_value
        mock_ts_instance.get_daily_adjusted = get_daily_adjusted
        mock_ts_instance.get_daily = get_daily

        client = MarketDataClient(
            provider="alpha_vantage",
            premium_api_key=premium_key,
            api_key=regular_key
        )

        # Get the TimeSeries instance to trigger the mock
        ts = client.provider._get_time_series()

        # Verify premium API key was passed to Alpha Vantage
        mock_alpha_vantage.assert_called_once()

        # Test data download with auto_adjust=True
        data = client.download(tickers="AAPL", auto_adjust=True, load=False, save=False)

        # Verify both premium and regular API were called
        assert daily_adjusted_called, "get_daily_adjusted was not called"
        assert daily_called, "get_daily was not called"

        # Verify data is unadjusted (from regular API)
        assert isinstance(data, pd.DataFrame)
        assert not data.empty
        assert "close" in data.columns.levels[1]
        assert "adj_close" not in data.columns.levels[1]
        assert "dividend" not in data.columns.levels[1]
        assert "split" not in data.columns.levels[1]

    def test_date_filtering(self, mock_alpha_vantage, mock_input):
        """Test date filtering of downloaded data"""
        client = MarketDataClient(provider="alpha_vantage", api_key="test_key")

        # Test with date range
        data = client.download(
            tickers="AAPL",
            start="2023-01-01",
            end="2023-01-02"
        )

        assert isinstance(data, pd.DataFrame)
        assert not data.empty
        assert len(data) == 2  # Should have 2 days of data

    def test_multiple_tickers(self, mock_alpha_vantage, mock_input):
        """Test downloading data for multiple tickers"""
        client = MarketDataClient(provider="alpha_vantage", api_key="test_key")

        # Test with multiple tickers
        data = client.download(tickers=["AAPL", "MSFT"])

        assert isinstance(data, pd.DataFrame)
        assert not data.empty
        assert len(data.columns.levels[0]) == 2  # Should have 2 tickers

    def test_invalid_interval(self, mock_alpha_vantage, mock_input):
        """Test handling of invalid interval"""
        client = MarketDataClient(provider="alpha_vantage", api_key="test_key")

        # Test with invalid interval
        with pytest.raises(ValueError):
            client.download(tickers="AAPL", interval="invalid")
