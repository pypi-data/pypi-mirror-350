import asyncio
import argparse
from dotenv import load_dotenv
from semantic_kernel.contents.chat_message_content import ChatMessageContent
from semantic_kernel.functions import KernelFunctionFromPrompt
from semantic_kernel.agents import AgentGroupChat
from semantic_kernel.agents.strategies import (
    KernelFunctionSelectionStrategy,
    KernelFunctionTerminationStrategy,
)
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

    # Initialize the agent group chat
    group_chat = AgentGroupChat(
        agents=[
            my_validate_patient_agent,
            my_summarize_agent,
            my_keyword_agent,
#            my_normalize_mutation_agent,
            my_orchestrator_agent
        ],
        termination_strategy=ApprovalTerminationStrategy(
            agents=[my_orchestrator_agent],
            maximum_iterations=5,
        ),
    )

    # Give the group chat the task instructions
    user_message = """
        You are an expert in genetics.
        First validate the patient name and surname, and only if they are valid, proceed with the analysis.
        You must only extract MECP2 cDNA mutations explicitly mentioned in the provided text.
        Detect the MECP2 mutations in the text, returning a normalized list of mutations that includes:
        - genomic_coordinate
        - primary_transcript NM_004992.4
        - secondary_transcript NM_001110792.2
        """
    print("User message:", user_message)
    print("Content:", input_text)
    response.add_user_message(user_message)
    await group_chat.add_chat_message(
        ChatMessageContent(role="user", content=cleaned_text)
    )

    async for content in group_chat.invoke():
        response.add_group_agent_message(content.name, content.content)
        print(f"Assistant {content.name}:", content.content)

    print(f"Response: {content.content}")
    return content.content


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
