from semantic_kernel.connectors.ai.open_ai.services.azure_chat_completion import (
    AzureChatCompletion,
)
from semantic_kernel.agents.chat_completion.chat_completion_agent import (
    ChatCompletionAgent,
)
from semantic_kernel.functions.kernel_arguments import KernelArguments
from semantic_kernel.kernel import Kernel
from rettxmutation.core.config_factory import get_config

class summarize_agent():

    def __init__(self, input_keywords: str = None):
        self.name = "summarize_agent"
        self.description = "A chat that can summarize genetic clinical reports."
        self.input_keywords = input_keywords
        self.instructions = """
        You are an expert at summarizing genetic clinical reports.
        Output a concise summary focusing on any mention of the MECP2 gene, transcripts.
        (e.g., NM_004992, NM_001110792), and variants (e.g., c.538C>T).
        Ignore unrelated text.
        The output must be always generated in English.
        You will be provided with a list of keywords to guide your summary.
        Focus on: "
        - Mentions of MECP2 gene "
        - Mentions of transcripts (NM_...) "
        - Mentions of variants (c.XXX...>XXX...) "
        - Key statements that connect them "
            "Return 1-3 paragraphs, no more than 300 words total."
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
#        kernel.add_plugin(
#            IssuesPlugin(
#                repo=self.repo,
#                gh_token=self.config.GH_TOKEN,
#            ),
#            plugin_name=WebPlugin.PLUGIN_NAME,
#        )

        return ChatCompletionAgent(
            kernel=kernel,
            name=self.name,
            description=self.description,
            instructions=self.instructions,
        )