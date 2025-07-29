# tests/test_cache_integration.py

import sys, os
# ensure the repo root is on sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pytest
from TestPrimeEngine.cache_engine import cache_engine

@pytest.fixture(autouse=True)
def clear_cache_and_metrics():
    for tier in cache_engine.tiers.values():
        if hasattr(tier, 'shards'):
            for shard in tier.shards:
                shard.clear()
        else:
            tier.store.clear()
    cache_engine.metrics.clear()
    yield

@pytest.mark.parametrize("symbol,arg,expected", [
    ('is_prime',    7,  True),
    ('is_prime',    8,  False),
    ('COMPOSITE?',  7,  False),
    ('COMPOSITE?',  8,  True),
    ('MERSENNE',    31, True),
    ('MERSENNE',    27, False),
    ('TWIN',        5,  True),
    ('TWIN',        9,  False),
])
def test_compute_and_cache(symbol, arg, expected):
    # first call ? miss + compute
    val1 = cache_engine.get(symbol, arg)
    assert val1 == expected
    assert cache_engine.metrics[f"miss_{symbol}"] == 1
    assert cache_engine.metrics.get(f"hit_{symbol}", 0) == 0

    # second call ? cache hit
    val2 = cache_engine.get(symbol, arg)
    assert val2 == expected
    assert cache_engine.metrics[f"hit_{symbol}"] == 1
    assert cache_engine.metrics[f"miss_{symbol}"] == 1
