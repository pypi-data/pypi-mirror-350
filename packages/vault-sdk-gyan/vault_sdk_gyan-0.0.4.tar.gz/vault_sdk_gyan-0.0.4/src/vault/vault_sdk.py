import requests
import os
import logging

from requests import RequestException
from requests.adapters import HTTPAdapter, Retry
from vault.utils.vault_cache import VaultCache
from vault.utils.vault_custom_cache import VaultCustomCache
from vault.utils.constants import VAULT_CACHE_TTL
from vault.utils.vault_exception import VaultException

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class VaultSdk:
    __sms_service = os.getenv("SMS_SERVICE", default="sms")
    __sms_port = int(os.getenv("SMS_SERVICE_PORT", default="5000"))
    __max_retries = int(os.getenv("SMS_MAX_RETRIES", default="5"))
    __secret_path = os.getenv("SECRET_MOUNT_PATH", default="/etc/creds")


    @staticmethod
    def fetch_secret_map(engine_type, secret_name):
        try:
            secret = VaultCache.get_instance().get(f'{secret_name}')
            if secret is not None:
                return secret
        except RequestException as e:
            logger.warning(f'Could not fetch secret with key {secret_name} from cache due to {e}')

        url = f'https://{VaultSdk.__sms_service}:{VaultSdk.__sms_port}/secret/{engine_type}/{secret_name}'

        s = requests.Session()
        retries = Retry(total=VaultSdk.__max_retries,
                        backoff_factor=0.5)

        s.mount('https://', HTTPAdapter(max_retries=retries))
        response = s.get(url, timeout=3)

        if response.ok and response.json():
            if response.status_code != 200:
                reason = response.json().get("exception")
                logger.error(f"Failed to fetch secret in path {secret_name} with statuscode: {response.status_code} and exception: {reason}")
                raise VaultException(f"Failed to fetch secrets: {reason}")
            VaultCache.get_instance().put(f"{secret_name}",response.json().get("data"))
            return response.json().get("data")
        else:
            logger.error("Could not fetch secret, retries exhausted")
            raise VaultException("Failed to fetch secrets: retries exhausted")

    @staticmethod
    def fetch_secret(engine_type, secret_name, secret_key):
        try:
            secret = VaultCache.get_instance().get(f'{secret_name}:{secret_key}')
            if secret is not None:
                return secret
        except RequestException as e:
            logger.warning(f'Could not fetch secret with key {secret_name}:{secret_key} from cache due to {e}')

        url = f'https://{VaultSdk.__sms_service}:{VaultSdk.__sms_port}/secret/{engine_type}/{secret_name}/{secret_key}'

        s = requests.Session()
        retries = Retry(total=VaultSdk.__max_retries,
                        backoff_factor=0.5)

        s.mount('https://', HTTPAdapter(max_retries=retries))
        response = s.get(url, timeout=3)

        if response.ok and response.json():
            if response.status_code != 200:
                reason = response.json().get("exception")
                logger.error(f"Failed to fetch secret in path {secret_name}/{secret_key} with statuscode: {response.status_code} and exception: {reason}")
                raise VaultException(f"Failed to fetch secrets: {reason}")
            VaultCache.get_instance().put(f"{secret_name}:{secret_key}", response.json().get("data"))
            return response.json().get("data")
        else:
            logger.error("Could not fetch secret, retries exhausted")
            raise VaultException("Failed to fetch secrets: retries exhausted")

    @staticmethod
    def fetch_secret_map_from_volume(path=None, ttl=VAULT_CACHE_TTL):
        """
        Reads all credentials (files) from the given path. But first checks in cache.

        Args:
            path (str): Path to the mounted secret directory.
            ttl (int): Ttl for a key

        Returns:
            dict: A dictionary with file names as keys and their contents as values.
        """
        path = VaultSdk.__secret_path if path is None else path
        cache_key = f"{path}"

        cached = VaultSdk._get_from_cache(cache_key)
        if cached is not None:
            return cached

        secrets = VaultSdk._read_all_files_from_path(path)
        VaultCustomCache.get_instance().put(cache_key, secrets, ttl)
        return secrets

    @staticmethod
    def fetch_secret_from_volume(key, path=None, ttl=VAULT_CACHE_TTL):
        """
        Reads a specific credential file from the given path. But first checks in cache.

        Args:
            key (str): The name of the credential file.
            path (str): Path to the mounted secret directory.
            ttl (int): Ttl for a key

        Returns:
            str: The content of the credential file.

        Raises:
            FileNotFoundError: If the credential file does not exist.
        """
        path = VaultSdk.__secret_path if path is None else path
        cache_key = f"{key}:{path}"

        cached = VaultSdk._get_from_cache(cache_key)
        if cached is not None:
            return cached

        secret = VaultSdk._read_file(os.path.join(path, key))
        VaultCustomCache.get_instance().put(cache_key, secret, ttl)
        return secret

    @staticmethod
    def _get_from_cache(cache_key):
        try:
            return VaultCustomCache.get_instance().get(cache_key)
        except RequestException as e:
            logger.info(f"Cache lookup failed for key '{cache_key}': {e}")
            return None

    @staticmethod
    def _read_all_files_from_path(path):
        if not os.path.exists(path):
            raise FileNotFoundError(f"Credentials directory not found: {path}")

        secrets = {}
        for filename in os.listdir(path):
            full_path = os.path.join(path, filename)
            if os.path.isfile(full_path):
                secrets[filename] = VaultSdk._read_file(full_path)
        return secrets

    @staticmethod
    def _read_file(filepath):
        if not os.path.isfile(filepath):
            raise FileNotFoundError(f"Credential file not found: {filepath}")

        with open(filepath, 'r') as f:
            return f.read().strip()
