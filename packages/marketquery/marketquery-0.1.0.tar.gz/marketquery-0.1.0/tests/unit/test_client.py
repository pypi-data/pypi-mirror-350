"""
Unit tests for the MarketDataClient class
"""

import pytest
from marketquery import MarketDataClient


class TestMarketDataClient:
    """Test suite for MarketDataClient class"""
    
    def test_init_default_provider(self):
        """Test initialization with default provider"""
        client = MarketDataClient()
        assert client.provider.__class__.__name__ == "YahooProvider"
        
    def test_init_with_api_key(self):
        """Test initialization with API key"""
        api_key = "test_key"
        client = MarketDataClient(api_key=api_key)
        assert client.provider.api_key == api_key
        
    def test_init_invalid_provider(self):
        """Test initialization with invalid provider"""
        with pytest.raises(ValueError) as exc_info:
            MarketDataClient(provider="invalid")
        assert "Provider 'invalid' not supported" in str(exc_info.value)
        
    def test_download_empty_tickers(self):
        """Test download with empty tickers"""
        client = MarketDataClient()
        with pytest.raises(ValueError) as exc_info:
            client.download(tickers=[])
        assert "At least one ticker must be provided" in str(exc_info.value)
        
    def test_download_single_ticker(self, mocker):
        """Test download with single ticker"""
        client = MarketDataClient()
        mock_data = {"AAPL": "data"}
        mocker.patch.object(client.provider, "download", return_value=mock_data)
        
        result = client.download(tickers="AAPL")
        assert result == mock_data
        client.provider.download.assert_called_once_with(
            tickers=["AAPL"],
            start_date=None,
            end_date=None,
            interval="1d"
        )
        
    def test_download_multiple_tickers(self, mocker):
        """Test download with multiple tickers"""
        client = MarketDataClient()
        mock_data = {"AAPL": "data1", "MSFT": "data2"}
        mocker.patch.object(client.provider, "download", return_value=mock_data)
        
        result = client.download(tickers=["AAPL", "MSFT"])
        assert result == mock_data
        client.provider.download.assert_called_once_with(
            tickers=["AAPL", "MSFT"],
            start_date=None,
            end_date=None,
            interval="1d"
        ) 
