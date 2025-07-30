"""
Integration tests for provider selection with environment variables
"""

import os
import pytest
import pandas as pd
from dotenv import load_dotenv
import marketquery as mq


@pytest.fixture
def setup_env():
    """Setup and teardown environment variables for testing"""
    # Load test environment variables first
    load_dotenv()
    print(f"\nEnvironment after loading .env:")
    print(f"MARKETQUERY_DEFAULT_PROVIDER: {os.getenv('MARKETQUERY_DEFAULT_PROVIDER')}")
    print(f"TIINGO_API_KEY exists: {os.getenv('TIINGO_API_KEY') is not None}")
    
    # Store original environment variables after loading .env
    original_provider = os.environ.get('MARKETQUERY_DEFAULT_PROVIDER')
    original_tiingo_key = os.environ.get('TIINGO_API_KEY')
    
    yield
    
    # Restore original environment variables
    if original_provider is not None:
        os.environ['MARKETQUERY_DEFAULT_PROVIDER'] = original_provider
    else:
        os.environ.pop('MARKETQUERY_DEFAULT_PROVIDER', None)
        
    if original_tiingo_key is not None:
        os.environ['TIINGO_API_KEY'] = original_tiingo_key
    else:
        os.environ.pop('TIINGO_API_KEY', None)


def test_default_provider_without_env():
    """Test that default provider is yahoo when no environment variables are set"""
    # Clear environment variables
    os.environ.pop('MARKETQUERY_DEFAULT_PROVIDER', None)
    
    # Create client without specifying provider
    client = mq.MarketDataClient()
    
    # Verify it's using Yahoo provider
    assert isinstance(client.provider, mq.providers.yahoo.YahooProvider)


def test_default_provider_with_env(setup_env):
    """Test that default provider is set from environment variable"""
    if not os.getenv('TIINGO_API_KEY'):
        pytest.skip("TIINGO_API_KEY environment variable not set")
    
    # Set environment variable
    os.environ['MARKETQUERY_DEFAULT_PROVIDER'] = 'tiingo'
    print(f"\nTesting with provider: {os.getenv('MARKETQUERY_DEFAULT_PROVIDER')}")
    
    # Create client without specifying provider
    client = mq.MarketDataClient()
    
    # Verify it's using Tiingo provider
    assert isinstance(client.provider, mq.providers.tiingo.TiingoProvider)


def test_download_with_env_provider(setup_env):
    """Test that download uses provider from environment variable"""
    if not os.getenv('TIINGO_API_KEY'):
        pytest.skip("TIINGO_API_KEY environment variable not set")
    
    # Set environment variable
    os.environ['MARKETQUERY_DEFAULT_PROVIDER'] = 'tiingo'
    print(f"\nTesting download with provider: {os.getenv('MARKETQUERY_DEFAULT_PROVIDER')}")
    
    # Download data without specifying provider
    data = mq.download('AAPL', start='2024-01-01', end='2024-01-31')
    
    # Verify data is from Tiingo (check for Tiingo-specific columns)
    assert isinstance(data, pd.DataFrame)
    assert 'adj_open' in data.columns.get_level_values(1)
    assert 'adj_close' in data.columns.get_level_values(1)


def test_explicit_provider_overrides_env(setup_env):
    """Test that explicitly specified provider overrides environment variable"""
    # Set environment variable
    os.environ['MARKETQUERY_DEFAULT_PROVIDER'] = 'tiingo'
    print(f"\nTesting explicit provider override with env: {os.getenv('MARKETQUERY_DEFAULT_PROVIDER')}")
    
    # Create client with explicit provider
    client = mq.MarketDataClient(provider='yahoo')
    
    # Verify it's using Yahoo provider despite environment variable
    assert isinstance(client.provider, mq.providers.yahoo.YahooProvider)


def test_invalid_provider_env(setup_env):
    """Test that invalid provider in environment variable raises error"""
    if not os.getenv('TIINGO_API_KEY'):
        pytest.skip("TIINGO_API_KEY environment variable not set")
    
    # Set invalid provider in environment
    os.environ['MARKETQUERY_DEFAULT_PROVIDER'] = 'invalid_provider'
    print(f"\nTesting invalid provider: {os.getenv('MARKETQUERY_DEFAULT_PROVIDER')}")
    
    # Verify it raises ValueError
    with pytest.raises(ValueError):
        mq.MarketDataClient() 
