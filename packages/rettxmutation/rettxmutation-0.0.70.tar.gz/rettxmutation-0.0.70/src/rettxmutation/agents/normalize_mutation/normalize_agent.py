from semantic_kernel.connectors.ai.open_ai.services.azure_chat_completion import (
    AzureChatCompletion,
)
from semantic_kernel.agents.chat_completion.chat_completion_agent import (
    ChatCompletionAgent,
)
from semantic_kernel.functions.kernel_arguments import KernelArguments
from semantic_kernel.kernel import Kernel
from rettxmutation.core.config_factory import get_config
from .mutation_plugin import MutationNormalizerPlugin

class normalize_mutation_agent:
    def __init__(self):
        self.name = "normalize_mutation"
        self.description = "An agent that validates and normalizes MECP2 mutations in HGVS format."
        self.instructions = """
        You are an expert on normalizing MECP2 mutations in HGVS format.
        You receive a mutation in HGVS format and you need to validate it. If the format is not HGVS, return an error message and DO NOT PROCEED.
        If the mutation is valid, you get the genomic coordinate in HGVS format.
        You will also provide the mutation in transcripts NM_004992.4 and NM_001110792.2 with the protein consequences.
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
        kernel.add_plugin(
            MutationNormalizerPlugin(),
            plugin_name=MutationNormalizerPlugin.PLUGIN_NAME,
        )

        return ChatCompletionAgent(
            kernel=kernel,
            name=self.name,
            description=self.description,
            instructions=self.instructions,
        )
