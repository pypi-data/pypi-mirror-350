from cachetools import Cache
from .constants import MAX_CACHE_SIZE, VAULT_CACHE_TTL
import time


class VaultCustomCache:
    __instance = None

    def __init__(self, maxsize=MAX_CACHE_SIZE, default_ttl=VAULT_CACHE_TTL):
        '''

        :param maxsize: Number of maximum allowed keys in cache
        '''
        self.cache = Cache(maxsize)
        self.expiry = {}
        self.default_ttl = default_ttl

    @staticmethod
    def get_instance():
        if VaultCustomCache.__instance is None:
            VaultCustomCache.__instance = VaultCustomCache()
        return VaultCustomCache.__instance

    def put(self, key, value, ttl=None):
        ttl = ttl if ttl is not None else self.default_ttl
        self.cache[key] = value
        self.expiry[key] = time.time() + ttl

    def get(self, key):
        if key in self.expiry and time.time() < self.expiry[key]:
            return self.cache[key]
        else:
            self.cache.pop(key, None)
            self.expiry.pop(key, None)
            return None
