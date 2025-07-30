"""
Shared fixtures for tests
"""

import pytest
from marketquery import MarketDataClient


@pytest.fixture
def market_client():
    """Create a MarketDataClient instance"""
    return MarketDataClient() 
