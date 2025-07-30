# app/core/config.py
import logging
from typing import Dict


logger = logging.getLogger(__name__)


class Config:
    def __init__(self, secrets: Dict[str, str]):
        """
        Takes a dictionary of secrets (e.g., from Env or KeyVault)
        and makes them available as attributes.
        """
        self.GLOBAL_LLM_SERVICE = secrets.get("GLOBAL_LLM_SERVICE", "AzureOpenAI")
        self.AZURE_OPENAI_API_KEY = secrets.get("AZURE_OPENAI_API_KEY", "")
        self.AZURE_OPENAI_ENDPOINT = secrets.get("AZURE_OPENAI_ENDPOINT", "")
        self.AZURE_OPENAI_CHAT_DEPLOYMENT_NAME = secrets.get("AZURE_OPENAI_CHAT_DEPLOYMENT_NAME", "")
        self.AZURE_OPENAI_TEXT_DEPLOYMENT_NAME = secrets.get("AZURE_OPENAI_TEXT_DEPLOYMENT_NAME", "")
        self.AZURE_OPENAI_EMBEDDING_DEPLOYMENT_NAME = secrets.get("AZURE_OPENAI_EMBEDDING_DEPLOYMENT_NAME", "")
        self.AZURE_OPENAI_API_VERSION = secrets.get("AZURE_OPENAI_API_VERSION", "")
        self.RETTX_DOCUMENT_ANALYSIS_ENDPOINT = secrets.get("RETTX_DOCUMENT_ANALYSIS_ENDPOINT", "")
        self.RETTX_DOCUMENT_ANALYSIS_KEY = secrets.get("RETTX_DOCUMENT_ANALYSIS_KEY", "")

        # Optionally validate to ensure required secrets are present
        self._validate_secrets()

    def _validate_secrets(self):
        """
        Raises EnvironmentError if any required secrets are missing.
        """

        required_fields = [
            "GLOBAL_LLM_SERVICE",
            "AZURE_OPENAI_API_KEY",
            "AZURE_OPENAI_ENDPOINT",
            "AZURE_OPENAI_CHAT_DEPLOYMENT_NAME",
            "AZURE_OPENAI_TEXT_DEPLOYMENT_NAME",
            "AZURE_OPENAI_EMBEDDING_DEPLOYMENT_NAME",
            "AZURE_OPENAI_API_VERSION",
            "RETTX_DOCUMENT_ANALYSIS_ENDPOINT",
            "RETTX_DOCUMENT_ANALYSIS_KEY"
        ]

        missing = [f for f in required_fields if not getattr(self, f)]
        if missing:
            logger.error(f"Missing required secrets: {missing}")
            raise EnvironmentError(f"Missing required secrets: {missing}")
