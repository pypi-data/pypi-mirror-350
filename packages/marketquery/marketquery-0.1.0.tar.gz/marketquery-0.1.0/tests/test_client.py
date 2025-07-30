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
            start=None,
            end=None,
            actions=False,
            threads=True,
            ignore_tz=None,
            group_by='column',
            auto_adjust=None,
            back_adjust=False,
            repair=False,
            keepna=False,
            progress=True,
            period="max",
            interval="1d",
            prepost=False,
            proxy=None,
            rounding=False,
            timeout=10,
            session=None
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
            start=None,
            end=None,
            actions=False,
            threads=True,
            ignore_tz=None,
            group_by='column',
            auto_adjust=None,
            back_adjust=False,
            repair=False,
            keepna=False,
            progress=True,
            period="max",
            interval="1d",
            prepost=False,
            proxy=None,
            rounding=False,
            timeout=10,
            session=None
        )

def test_get_crypto_data():
    """Test getting crypto data"""
    client = MarketDataClient()
    data = client.get_crypto_data("BTC", provider="yahoo")
    
    assert data is not None
    assert "info" in data
    assert "history" in data
    assert "provider" in data
    assert data["provider"] == "yahoo"

def test_invalid_provider():
    """Test that invalid provider raises ValueError"""
    client = MarketDataClient()
    with pytest.raises(ValueError):
        client.get_stock_data("AAPL", provider="invalid_provider") 
