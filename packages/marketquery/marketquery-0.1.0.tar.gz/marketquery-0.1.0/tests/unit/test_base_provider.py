"""
Unit tests for the BaseProvider class
"""

import pytest
from marketquery.providers.base import BaseProvider


class TestBaseProvider:
    """Test suite for BaseProvider class"""
    
    def test_init_with_api_key(self):
        """Test initialization with API key"""
        api_key = "test_key"
        provider = BaseProvider(api_key=api_key)
        assert provider.api_key == api_key
        
    def test_init_without_api_key(self):
        """Test initialization without API key"""
        provider = BaseProvider()
        assert provider.api_key is None
        
    def test_download_not_implemented(self):
        """Test that download method raises NotImplementedError"""
        provider = BaseProvider()
        with pytest.raises(NotImplementedError):
            provider.download(tickers="AAPL") 
