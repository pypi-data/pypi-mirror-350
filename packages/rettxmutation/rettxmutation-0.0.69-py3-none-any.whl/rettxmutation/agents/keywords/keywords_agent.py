from semantic_kernel.connectors.ai.open_ai.services.azure_chat_completion import (
    AzureChatCompletion,
)
from semantic_kernel.agents.chat_completion.chat_completion_agent import (
    ChatCompletionAgent,
)
from semantic_kernel.functions.kernel_arguments import KernelArguments
from semantic_kernel.kernel import Kernel
from rettxmutation.core.config_factory import get_config
from .keywords_plugin import RawMutationPlugin

class mutation_detector_agent:

    def __init__(self):
        self.name = "detector"
        self.description = "Agent that detects genetic mutations in text."
        self.instructions = """
            You are an expert in genetics.
            You must only extract MECP2 cDNA mutations explicitly mentioned in the provided text.
            These mutations are typically in a format like c.916C>T, c.1035A>G or c.1140_1160del.
            If you find more than one mutation, list each on a new line in the format: "
            transcript:gene_variation;confidence=score "
            Examples: "
            1) NM_004992.4:c.916C>T;confidence=1.0 "
            2) NM_001110792.1:c.538C>T;confidence=0.8 "
            3) NM_004992.4:c.1035A>G;confidence=0.6 "
            4) NM_004992.4:c.1152_1195del;confidence=1.0 "
            5) NM_004992.4:c.378-2A>G;confidence=0.9 "
            6) NM_001110792.2:c.414-2A>G;confidence=0.7 "
            If the text only describes a deletion of exons (or no explicit cDNA nomenclature),
            then output 'No mutation found'."
            Guidelines:"
            1) Do NOT fabricate or infer cDNA variants from exon-level deletions.
            If cDNA notation is not present, respond with 'No mutation found'."
            2) Use only the transcripts provided in the keywords.
            If no transcript is provided, default to NM_004992.4."
            3) Confidence score must be between 0 and 1."
            4) Provide no extra commentary beyond the specified format."
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
            RawMutationPlugin(),
            plugin_name=RawMutationPlugin.PLUGIN_NAME,
        )

        return ChatCompletionAgent(
            kernel=kernel,
            name=self.name,
            description=self.description,
            instructions=self.instructions,
        )