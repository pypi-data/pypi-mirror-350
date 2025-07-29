# Import main classes/functions that users will need
from .vault_sdk import VaultSdk # or whatever your main class is called
from .utils.vault_exception import VaultException  # your custom exceptions

# Make version available
__version__ = "0.1.0"

# Optional: define what gets imported with "from vault import *"
__all__ = ['VaultSdk', 'VaultException']