from cachetools import TTLCache
import os


class VaultCache:
    # Deprecate this and use VaultCustomCache
    __instance = None
    __max_cache_size = int(os.getenv("MAX_CACHE_SIZE", default=50))
    __vault_cache_ttl = int(os.getenv("VAULT_CACHE_TTL", default=1200)) # TTL is in seconds

    def __init__(self):
        self.vault_cache = TTLCache(maxsize=VaultCache.__max_cache_size, ttl=VaultCache.__vault_cache_ttl)

    @staticmethod
    def get_instance():
        if VaultCache.__instance is None:
            VaultCache.__instance = VaultCache()
        return VaultCache.__instance

    def get(self, cache_key):
        return self.vault_cache.get(cache_key)

    def put(self, cache_key, secret):
        self.vault_cache[cache_key] = secret
