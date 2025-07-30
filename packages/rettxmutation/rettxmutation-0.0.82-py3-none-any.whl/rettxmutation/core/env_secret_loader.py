# app/core/env_secret_loader.py
import os
import logging
from typing import Dict
from .secret_loader import SecretLoader

# Setup logging
logger = logging.getLogger(__name__)


class EnvSecretLoader(SecretLoader):
    def load_secrets(self) -> Dict[str, str]:
        """
        Loads secrets from environment variables.
        """
        logger.info("Loading secrets from environment variables...")
        secrets = {
            "GLOBAL_LLM_SERVICE": os.getenv("GLOBAL_LLM_SERVICE", "AzureOpenAI"),
            "AZURE_OPENAI_API_KEY": os.getenv("AZURE_OPENAI_API_KEY", ""),
            "AZURE_OPENAI_ENDPOINT": os.getenv("AZURE_OPENAI_ENDPOINT", ""),
            "AZURE_OPENAI_CHAT_DEPLOYMENT_NAME": os.getenv("AZURE_OPENAI_CHAT_DEPLOYMENT_NAME", ""),
            "AZURE_OPENAI_TEXT_DEPLOYMENT_NAME": os.getenv("AZURE_OPENAI_TEXT_DEPLOYMENT_NAME", ""),
            "AZURE_OPENAI_EMBEDDING_DEPLOYMENT_NAME": os.getenv("AZURE_OPENAI_EMBEDDING_DEPLOYMENT_NAME", ""),
            "AZURE_OPENAI_API_VERSION": os.getenv("AZURE_OPENAI_API_VERSION", ""),
            "RETTX_DOCUMENT_ANALYSIS_ENDPOINT": os.getenv("RETTX_DOCUMENT_ANALYSIS_ENDPOINT", ""),
            "RETTX_DOCUMENT_ANALYSIS_KEY": os.getenv("RETTX_DOCUMENT_ANALYSIS_KEY", "")
        }
        return secrets
