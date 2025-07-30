# app/core/config_factory.py
import os
import logging
import threading
from typing import Optional
from .config import Config
from .env_secret_loader import EnvSecretLoader


# Setup logging
logger = logging.getLogger(__name__)


_cached_config: Optional[Config] = None
_lock = threading.Lock()

def get_config() -> Config:
    """
    Returns a cached Config object. On the first call, it will load
    secrets from either environment variables or Key Vault, depending
    on the ENVIRONMENT variable. Subsequent calls return the same object.
    """
    global _cached_config
    if _cached_config is None:
        with _lock:
            if _cached_config is None:
                _cached_config = _create_config()
    return _cached_config

def _create_config() -> Config:
    env = os.getenv("ENVIRONMENT", "prod").lower()
    logger.info(f"Creating Config for environment: {env}")

    env = "dev"

    if env == "dev":
        logger.info("Using EnvSecretLoader (dev mode).")
        loader = EnvSecretLoader()
    else:
        logger.info("Using KeyVaultSecretLoader (prod mode).")
        loader = None

    secrets = loader.load_secrets()
    return Config(secrets)


# Optional: If you need to clear the cache for testing or dynamic reload
def clear_config_cache() -> None:
    global _cached_config
    with _lock:
        _cached_config = None
