"""
Integration tests for Yahoo provider caching behavior
"""

import os
import shutil
import pytest
import pandas as pd
from marketquery import MarketDataClient
from marketquery.cache import CacheManager



class TestYahooCaching:
    """Test suite for Yahoo provider caching behavior"""
    
    @pytest.fixture(autouse=True)
    def setup_and_teardown(self):
        """Setup and teardown for each test"""
        # Create a temporary cache directory
        self.cache_dir = "test_cache"
        if os.path.exists(self.cache_dir):
            shutil.rmtree(self.cache_dir)
        os.makedirs(self.cache_dir)
        
        # Initialize client with test cache directory
        self.client = MarketDataClient(
            provider="yahoo",
            cache_dir=self.cache_dir
        )
        
        yield
        
        # Cleanup after test
        # if os.path.exists(self.cache_dir):
        #     shutil.rmtree(self.cache_dir)
    
    def test_batch_download_caching(self):
        """Test that batch downloads are properly cached per symbol"""
        # Clear any existing cache
        self.client.clear_cache()
        
        # Download data for multiple symbols
        df = self.client.download(
            tickers=["AAPL", "GOOGL"],
            start="2025-01-01",
            end="2025-01-10",
            interval="1d"
        )

        # Verify the downloaded data
        assert isinstance(df, pd.DataFrame)
        assert not df.empty
        assert "AAPL" in df.columns.levels[0]
        assert "GOOGL" in df.columns.levels[0]
        
        # Check cache files
        cache = CacheManager(self.cache_dir)
        yahoo_cache_dir = os.path.join(self.cache_dir, 'yahoo')
        cache_files = os.listdir(yahoo_cache_dir)
        
        # Should have two cache files (one for each symbol)
        assert len(cache_files) == 2
        
        # Verify each symbol has its own cache file
        for symbol in ["AAPL", "GOOGL"]:
            # Find the cache file for this symbol
            symbol_cache_files = [f for f in cache_files if f == f"{symbol}.pkl"]
            assert len(symbol_cache_files) == 1
            
            # Load the cached data
            cached_data = cache.load_data(
                provider="yahoo",
                symbol=symbol,
                start_date="2025-01-01",
                end_date="2025-01-10",
                interval="1d"
            )

            print(cached_data)
            
            # Verify cached data
            assert isinstance(cached_data, pd.DataFrame)
            assert not cached_data.empty
            assert symbol in cached_data.columns.levels[0]
            
            # Verify date range
            assert cached_data.index.min() >= pd.Timestamp("2025-01-01")
            assert cached_data.index.max() <= pd.Timestamp("2025-01-10")

    def test_load_false_behavior(self):
        """Test that load=False forces all symbols to be downloaded"""
        # First download and cache some data
        self.client.download(
            tickers=["AAPL", "GOOGL"],
            start="2025-01-01",
            end="2025-01-10",
            interval="1d"
        )
    
        # Verify cache files exist in yahoo directory
        yahoo_cache_dir = os.path.join(self.cache_dir, 'yahoo')
        cache_files = os.listdir(yahoo_cache_dir)
        print(cache_files)
        assert len(cache_files) == 2
