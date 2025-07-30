from semantic_kernel.connectors.ai.open_ai.services.azure_chat_completion import (
    AzureChatCompletion,
)
from semantic_kernel.agents.chat_completion.chat_completion_agent import (
    ChatCompletionAgent,
)
from semantic_kernel.kernel import Kernel
from rettxmutation.core.config_factory import get_config

class validate_patient_agent():

    def __init__(self, name: str, surname: str):
        self.name = "validate_patient_agent"
        self.description = "A chat that validates if the report refers to a given patient using name and surname"
        self.patient_name = name
        self.patient_surname = surname
        self.instructions = f"""
        You are a medical assistant that validates if the report refers to {self.patient_name} {self.patient_surname}.
        You will answer with 'yes' or 'no' and provide no further explanation with a confidence score between 0 and 1.
        Both the name and surname are required to be present, but if the surname is incomplete, you must reduce the confidence score.
        """
        self.config = get_config()

    def build_agent(self):
        kernel = Kernel()
        kernel.add_service(
            AzureChatCompletion(
                deployment_name=self.config.AZURE_OPENAI_CHAT_DEPLOYMENT_NAME,
                api_key=self.config.AZURE_OPENAI_API_KEY,
                endpoint=self.config.AZURE_OPENAI_ENDPOINT,
                api_version=self.config.AZURE_OPENAI_API_VERSION
            )
        )

        return ChatCompletionAgent(
            kernel=kernel,
            name=self.name,
            description=self.description,
            instructions=self.instructions,
        )
