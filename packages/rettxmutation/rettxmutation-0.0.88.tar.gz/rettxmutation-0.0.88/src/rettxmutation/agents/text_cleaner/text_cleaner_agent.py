from semantic_kernel.kernel import Kernel
from semantic_kernel.functions.kernel_arguments import KernelArguments
from .cleaner_plugin import TextCleanerPlugin

class text_cleaner_agent:

    def __init__(self):
        self.name = "text_cleaner_agent"
        self.description = "Agent that strictly cleans OCR-extracted text using regex-based rules."

    async def clean_text(self, raw_text: str) -> str:
        kernel = Kernel()
        cleaner_plugin = TextCleanerPlugin(raw_text=raw_text)
        kernel.add_plugin(cleaner_plugin, TextCleanerPlugin.PLUGIN_NAME)

        # Direct invocation—no LLM involved
        cleaned_text = await kernel.invoke(
            function_name="clean_ocr_text",
            plugin_name=TextCleanerPlugin.PLUGIN_NAME,
            arguments=KernelArguments()
        )
        return str(cleaned_text)
