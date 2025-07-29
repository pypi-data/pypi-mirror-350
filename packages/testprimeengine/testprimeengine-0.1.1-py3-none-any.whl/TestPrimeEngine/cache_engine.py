# cache_engine.py

import threading
from collections import defaultdict
from TestPrimeEngine.symbolic_factoring import PRIME_FUNCTIONS

class SymbolControlTier:
    def __init__(self):
        self.routing_map = {}
        self.promotion_threshold = 10
        self.eviction_threshold = 0.7

    def register(self, symbol, tier):
        self.routing_map[symbol] = tier

    def get_tier(self, symbol):
        return self.routing_map.get(symbol)

    def should_promote(self, symbol, hits):
        return hits > self.promotion_threshold

class BaseTierCache:
    def __init__(self):
        self.store = {}
        self.lock = threading.Lock()
    def lookup(self, key):
        return self.store.get(key)
    def insert(self, key, value=True):
        with self.lock:
            self.store[key] = value

class Tier1Cache(BaseTierCache):
    def __init__(self, shards=4):
        super().__init__()
        self.shards = [dict() for _ in range(shards)]
        self.shards_n = shards
    def _shard(self, key):
        return hash(key) % self.shards_n
    def lookup(self, key):
        return self.shards[self._shard(key)].get(key)
    def insert(self, key, value=True):
        self.shards[self._shard(key)][key] = value

class Tier2Cache(BaseTierCache): pass
class Tier3Cache(BaseTierCache): pass

class SymbolicCacheEngine:
    def __init__(self, beta):
        self.control = SymbolControlTier()
        self.tiers = {
            1: Tier1Cache(),
            2: Tier2Cache(),
            3: Tier3Cache(),
        }
        self.metrics = defaultdict(int)
        self.beta = beta
        self._register_symbols()

    def _register_symbols(self):
        for sym, t in [
            ('is_prime',    1),
            ('COMPOSITE?',  1),
            ('MERSENNE',    2),
            ('TWIN',        2),
            ('PRIME_GAPS',  3),
        ]:
            self.control.register(sym, t)

    def get(self, symbol, arg):
        tier = self.control.get_tier(symbol)
        val = self.tiers[tier].lookup(arg)
        if val is not None:
            self.metrics[f"hit_{symbol}"] += 1
            return val
        self.metrics[f"miss_{symbol}"] += 1
        func = PRIME_FUNCTIONS.get(symbol)
        if func is None:
            raise KeyError(f"No function for symbol {symbol!r}")
        result = func(arg)
        self.tiers[tier].insert(arg, result)
        return result

beta_value = 18446744073709551557
cache_engine = SymbolicCacheEngine(beta_value)
