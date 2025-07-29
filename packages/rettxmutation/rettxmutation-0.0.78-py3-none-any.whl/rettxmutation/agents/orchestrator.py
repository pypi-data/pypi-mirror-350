from semantic_kernel.connectors.ai.open_ai.services.azure_chat_completion import (
    AzureChatCompletion,
)
from semantic_kernel.agents.chat_completion.chat_completion_agent import (
    ChatCompletionAgent,
)
from semantic_kernel.functions.kernel_arguments import KernelArguments
from semantic_kernel.kernel import Kernel
from rettxmutation.core.config_factory import get_config

class orchestrator_agent:
    def __init__(self):
        self.name = "orchestrator"
        self.description = "A chat that reviews the conversation and decides which agent to call."
        self.instructions = """
        You are a chat agent tasked to identify a MECP2 mutation from an input message.
        You will be helped by other agents that you can call if you need more information.
        If any of the agents helping you uses the word TERMINATE in their message, you should stop the conversation.
        Once the mutation is identified you can close the conversation and add the word TERMINATE to the message.
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