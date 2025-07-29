import asyncio
import argparse
from dotenv import load_dotenv
from semantic_kernel.contents.chat_message_content import ChatMessageContent
from semantic_kernel.functions import KernelFunctionFromPrompt
from semantic_kernel.agents import AgentGroupChat, AgentChat, ChatHistoryAgentThread
from .services.agents_contracts import ResponseMessage, ApprovalTerminationStrategy
from .agents.summarize.summary_agent import summarize_agent
from .agents.keywords.keywords_agent import mutation_detector_agent
from .agents.normalize_mutation.normalize_agent import normalize_mutation_agent
from .agents.orchestrator import orchestrator_agent
from .agents.text_cleaner.text_cleaner_agent import text_cleaner_agent
from .agents.validate_patient.validate_patient_agent import validate_patient_agent
from rettxmutation.core.config_factory import get_config
from rettxmutation.services.ocr_extractor import OcrExtractor

# Define agent names
REVIEWER_NAME = "Reviewer"
SUMMARIZE_NAME = "Summarizer"


async def execution(name: str, surname: str, input_text: str) -> str:
    # Prepara the response message
    response = ResponseMessage()

    # Instantiate deterministic text cleaner
    #cleaner = text_cleaner_agent()
    #cleaned_text = await cleaner.clean_text(raw_text=input_text)
    cleaned_text = input_text

    # Initialize all the agents
    my_summarize_agent = summarize_agent().build_agent()
    my_keyword_agent = mutation_detector_agent().build_agent()
    my_normalize_mutation_agent = normalize_mutation_agent().build_agent()
    my_validate_patient_agent = validate_patient_agent(name, surname).build_agent()
    my_orchestrator_agent = orchestrator_agent().build_agent()

    thread = ChatHistoryAgentThread()
    input_messages = ChatMessageContent(
        content=cleaned_text,
        role="user",
        author=REVIEWER_NAME,
    )
    response = await my_validate_patient_agent.get_response(messages=input_messages, thread=thread)
    print("Response:", response.content)


if __name__ == "__main__":
    load_dotenv()
    myconfig = get_config()

    # Parse command line arguments
    parser = argparse.ArgumentParser(description='Process a file.')
    parser.add_argument('filename', metavar='F', type=str, nargs='+', help='a filename for the document analysis')
    parser.add_argument('name', metavar='N', type=str, nargs='+', help='a name for the patient')
    parser.add_argument('surname', metavar='S', type=str, nargs='+', help='a surname for the patient')
    filename = parser.parse_args().filename[0]
    name = parser.parse_args().name[0]
    surname = parser.parse_args().surname[0]

    ocr_extractor = OcrExtractor(
        myconfig.RETTX_DOCUMENT_ANALYSIS_ENDPOINT,
        myconfig.RETTX_DOCUMENT_ANALYSIS_KEY
    )

    file_stream = open(filename, "rb")
    document = ocr_extractor.extract_text(file_stream)
    input_text = document.raw_text

    asyncio.run(
        execution(
            input_text=input_text,
            name=name,
            surname=surname
        )
    )
