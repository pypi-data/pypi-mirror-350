# warm_cache.py

from TestPrimeEngine.cache_engine import cache_engine

def warm_primes(limit: int):
    """Preload is_prime for 2 and all odd candidates ending in 1/3/7/9 up to `limit`."""
    cache_engine.get('is_prime', 2)
    for n in range(3, limit + 1, 2):
        if str(n)[-1] in {'1','3','7','9'}:
            cache_engine.get('is_prime', n)

def warm_composite(limit: int):
    """Preload COMPOSITE? for every n up to `limit`."""
    for n in range(2, limit + 1):
        cache_engine.get('COMPOSITE?', n)

def warm_mersenne(max_p: int):
    """Preload MERSENNE(2**p-1) for p in [2..max_p]."""
    for p in range(2, max_p + 1):
        m = 2**p - 1
        cache_engine.get('MERSENNE', m)

def warm_twin(limit: int):
    """Preload TWIN(n) for every n up to `limit`."""
    for n in range(2, limit + 1):
        cache_engine.get('TWIN', n)

if __name__ == "__main__":
    print("Warming is_prime up to 10_000…")
    warm_primes(10_000)
    print("Warming COMPOSITE? up to 10_000…")
    warm_composite(10_000)
    print("Warming MERSENNE for p≤20…")
    warm_mersenne(20)
    print("Warming TWIN up to 10_000…")
    warm_twin(10_000)
    print("✅ Done warming all tiers.")
def warm_cache(limit: int) -> dict:
    """
    Populate all caches up to limit and return as a dict:
      {
        'primes': [...],
        'composite': [...],
        'mersenne': [...],
        'twin': [...]
      }
    """
    return {
        'primes'   : warm_primes(limit),
        'composite': warm_composite(limit),
        'mersenne' : warm_mersenne(limit),
        'twin'     : warm_twin(limit),
    }
