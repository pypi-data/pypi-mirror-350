import os

MAX_CACHE_SIZE = int(os.getenv("MAX_CACHE_SIZE", 50))
VAULT_CACHE_TTL = int(os.getenv("VAULT_CACHE_TTL", 300))  # in seconds