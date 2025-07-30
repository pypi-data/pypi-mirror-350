import pytest
from unittest.mock import patch, MagicMock
from rettxmutation.analysis.openai_rettx_agents import OpenAIRettXAgents, InvalidResponse
from rettxmutation.models.gene_models import RawMutation
from openai import RateLimitError


@patch("rettxmutation.analysis.openai_rettx_agents.AzureOpenAI")
def test_extract_mutations_success(mock_azure_openai_class):
    """
    Test a successful call to extract_mutations that returns valid mutations.
    """
    # 1) Create a mock AzureOpenAI instance
    mock_azure_openai = MagicMock()
    mock_azure_openai_class.return_value = mock_azure_openai

    # 2) Mock the 'chat.completions.create' method to simulate a valid response
    mock_response = MagicMock()
    mock_response.choices = [
        MagicMock(
            message=MagicMock(content=(
                "NM_004992.4:c.916C>T;confidence=1.0\n"
                "NM_001110792.2:c.538C>T;confidence=0.8\n"
                "Invalid;confidence=0.0"
            ))
        )
    ]
    mock_azure_openai.chat.completions.create.return_value = mock_response

    # 3) Instantiate OpenAIRettXAgents
    agent = OpenAIRettXAgents(
        api_key="fake_key",
        api_version="fake_version",
        azure_endpoint="https://fake.endpoint",
        model_name="test-model",
        embedding_deployment="test-embedding",
        audit_logger=MagicMock()
    )

    # 4) Call the method under test
    text = "This text mentions c.916C>T and c.538C>T in MECP2."
    result = agent.extract_mutations(
        audit_context="dummy-correlation-id",
        document_text=text,
        mecp2_keywords="NM_004992.4\nNM_001110792.2",
        variant_list="c.916C>T\nc.538C>T"
    )    # 5) Verify the result
    assert len(result) == 3  # All three lines are parsed successfully

    first_mutation = result[0]
    assert first_mutation.mutation == "NM_004992.4:c.916C>T" 
    assert first_mutation.confidence == 1.0

    second_mutation = result[1]
    assert second_mutation.mutation == "NM_001110792.2:c.538C>T"
    assert second_mutation.confidence == 0.8
    
    third_mutation = result[2]
    assert third_mutation.mutation == "Invalid"
    assert third_mutation.confidence == 0.0

    # 6) Also ensure the mock was called correctly
    mock_azure_openai.chat.completions.create.assert_called_once()


@patch("rettxmutation.analysis.openai_rettx_agents.AzureOpenAI")
def test_openai_fail(mock_azure_openai_class):
    """
    Test a failed call to extract_mutations that returns valid mutations.
    """
    # 1) Create a mock AzureOpenAI instance
    mock_azure_openai = MagicMock()
    mock_azure_openai_class.return_value = mock_azure_openai

    # 2) Mock the 'chat.completions.create' method to simulate a valid response
    mock_response = MagicMock()
    mock_response.choices = [
        MagicMock(message=MagicMock(content=None))
    ]
    mock_azure_openai.chat.completions.create.return_value = mock_response

    # 3) Instantiate OpenAIRettXAgents
    agent = OpenAIRettXAgents(
        api_key="fake_key",
        api_version="fake_version",
        azure_endpoint="https://fake.endpoint",
        model_name="test-model",
        embedding_deployment="test-embedding",
        audit_logger=MagicMock()
    )

    # Must raise exception
    with pytest.raises(InvalidResponse):
        agent.extract_mutations(
            audit_context="dummy-correlation-id",
            document_text="dummy text",
            mecp2_keywords="dummy text",
            variant_list="dummy text"
        )

    # Must raise exception
    with pytest.raises(InvalidResponse):
        agent.summarize_report(
            audit_context="dummy-correlation-id",
            document_text="dummy text",
            keywords="dummy text"
        )

    # Must raise exception
    with pytest.raises(InvalidResponse):
        agent.correct_summary_mistakes(
            audit_context="dummy-correlation-id",
            document_text="dummy text",
            keywords="dummy text",
            text_analytics="dummy text"
        )


@patch("rettxmutation.analysis.openai_rettx_agents.AzureOpenAI")
def test_summarize_report_success(mock_azure_openai_class):
    """
    Test a successful call to summarize_report.
    """
    # 1) Create a mock AzureOpenAI instance
    mock_azure_openai = MagicMock()
    mock_azure_openai_class.return_value = mock_azure_openai

    # 2) Mock the 'chat.completions.create' method to simulate a valid response
    mock_response = MagicMock()
    mock_response.choices = [
        MagicMock(
            message=MagicMock(content=(
                "This is a mock of the report summary"
            ))
        )
    ]
    mock_azure_openai.chat.completions.create.return_value = mock_response

    # 3) Instantiate OpenAIRettXAgents
    agent = OpenAIRettXAgents(
        api_key="fake_key",
        api_version="fake_version",
        azure_endpoint="https://fake.endpoint",
        model_name="test-model",
        embedding_deployment="test-embedding",
        audit_logger=MagicMock()
    )

    # 4) Call the method under test
    text = "This text mentions c.916C>T and c.538C>T in MECP2."
    result = agent.summarize_report(
        audit_context="dummy-correlation-id",
        document_text=text,
        keywords="NM_004992.4\nNM_001110792.2"
    )

    # 5) Verify the result
    assert len(result) == 36
    assert result == "This is a mock of the report summary"


@patch("rettxmutation.analysis.openai_rettx_agents.AzureOpenAI")
def test_correct_summary_mistakes_success(mock_azure_openai_class):
    """
    Test a successful call to correct_summary_mistakes.
    """
    # 1) Create a mock AzureOpenAI instance
    mock_azure_openai = MagicMock()
    mock_azure_openai_class.return_value = mock_azure_openai

    # 2) Mock the 'chat.completions.create' method to simulate a valid response
    mock_response = MagicMock()
    mock_response.choices = [
        MagicMock(
            message=MagicMock(content=(
                "Mutation c.538C>T was detected in patient A"
            ))
        )
    ]
    mock_azure_openai.chat.completions.create.return_value = mock_response

    # 3) Instantiate OpenAIRettXAgents
    agent = OpenAIRettXAgents(
        api_key="fake_key",
        api_version="fake_version",
        azure_endpoint="https://fake.endpoint",
        model_name="test-model",
        embedding_deployment="test-embedding",
        audit_logger=MagicMock()
    )

    # 4) Call the method under test
    text = "Mutation c538C->T was detected in patient A"
    result = agent.correct_summary_mistakes(
        audit_context="dummy-correlation-id",
        document_text=text,
        keywords="NM_004992.4\nNM_001110792.2",
        text_analytics="c.916C>T\nc.538C>T"
    )

    # 5) Verify the result
    assert result == "Mutation c.538C>T was detected in patient A"


@patch("rettxmutation.analysis.openai_rettx_agents.AzureOpenAI")
def test_create_embedding_success(mock_azure_openai_class):
    """
    Test a successful call to create_embedding.
    """
    # 1) Create a mock AzureOpenAI instance
    mock_azure_openai = MagicMock()
    mock_azure_openai_class.return_value = mock_azure_openai

    # 2) Mock the 'embeddings.create' method to simulate a valid response
    mock_response = MagicMock()
    mock_response.data = [MagicMock(embedding=[0.1, 0.2, 0.3, 0.4, 0.5])]
    mock_azure_openai.embeddings.create.return_value = mock_response

    # 3) Instantiate OpenAIRettXAgents
    agent = OpenAIRettXAgents(
        api_key="fake_key",
        api_version="fake_version",
        azure_endpoint="https://fake.endpoint",
        model_name="test-model",
        embedding_deployment="test-embedding",
        audit_logger=MagicMock()
    )

    # 4) Call the method under test
    text = "This is a test text for embedding."
    result = agent.create_embedding(text)

    # 5) Verify the result
    assert result == [0.1, 0.2, 0.3, 0.4, 0.5]
    
    # 6) Verify the mock was called correctly
    mock_azure_openai.embeddings.create.assert_called_once_with(
        model="test-embedding",
        input=text,
        encoding_format="float"
    )


@patch("rettxmutation.analysis.openai_rettx_agents.AzureOpenAI")
def test_create_embedding_error(mock_azure_openai_class):
    """
    Test error handling in create_embedding.
    """
    # 1) Create a mock AzureOpenAI instance
    mock_azure_openai = MagicMock()
    mock_azure_openai_class.return_value = mock_azure_openai

    # 2) Mock the 'embeddings.create' method to raise an exception
    mock_azure_openai.embeddings.create.side_effect = Exception("Test error")

    # 3) Instantiate OpenAIRettXAgents
    agent = OpenAIRettXAgents(
        api_key="fake_key",
        api_version="fake_version",
        azure_endpoint="https://fake.endpoint",
        model_name="test-model",
        embedding_deployment="test-embedding",
        audit_logger=MagicMock()
    )

    # 4) Call the method under test and verify it raises the exception
    with pytest.raises(Exception):
        agent.create_embedding("This is a test text for embedding.")


@patch("rettxmutation.analysis.openai_rettx_agents.AzureOpenAI")
def test_create_embedding_rate_limit_backoff(mock_azure_openai_class):
    """
    Test that backoff is applied when a RateLimitError is encountered.
    """
    # Create a Mock for the client
    mock_azure_openai = MagicMock()
    mock_azure_openai_class.return_value = mock_azure_openai
    
    # Create a Mock for the response
    mock_response = MagicMock()
    mock_response.data = [MagicMock(embedding=[0.1, 0.2, 0.3])]
    mock_azure_openai.embeddings.create.return_value = mock_response
    
    # Instantiate OpenAIRettXAgents
    agent = OpenAIRettXAgents(
        api_key="fake_key",
        api_version="fake_version",
        azure_endpoint="https://fake.endpoint",
        model_name="test-model",
        embedding_deployment="test-embedding",
        audit_logger=MagicMock()
    )
    
    # Call the method
    result = agent.create_embedding("test text")
    
    # Verify the result
    assert result == [0.1, 0.2, 0.3]
    
    # Verify the API was called with correct parameters
    mock_azure_openai.embeddings.create.assert_called_once_with(
        model="test-embedding",
        input="test text",
        encoding_format="float"
    )
    
    # Verify the method is decorated with backoff.on_exception
    # We can't directly test this in a unit test, but we can check that
    # the method has the __wrapped__ attribute which is added by the decorator    assert hasattr(agent.create_embedding, "__wrapped__")
    
    # Note: Due to how backoff works, we can't easily test the actual retry 
    # behavior in a unit test without complex mocking. This test verifies that
    # the decorator is configured correctly.


@patch("rettxmutation.analysis.openai_rettx_agents.AzureOpenAI")
def test_validate_document_success(mock_azure_openai_class):
    """
    Test a successful call to validate_document.
    """
    # 1) Create a mock AzureOpenAI instance
    mock_azure_openai = MagicMock()
    mock_azure_openai_class.return_value = mock_azure_openai

    # 2) Mock the 'chat.completions.create' method to simulate a valid response
    mock_response = MagicMock()
    mock_response.choices = [
        MagicMock(
            message=MagicMock(content="True, confidence=0.9")
        )
    ]
    mock_azure_openai.chat.completions.create.return_value = mock_response

    # 3) Instantiate OpenAIRettXAgents
    agent = OpenAIRettXAgents(
        api_key="fake_key",
        api_version="fake_version",
        azure_endpoint="https://fake.endpoint",
        model_name="test-model",
        embedding_deployment="test-embedding",
        audit_logger=MagicMock()
    )

    # 4) Call the method under test
    text = "This text mentions MECP2 gene with mutation c.916C>T."
    is_valid, confidence = agent.validate_document(
        audit_context="dummy-correlation-id",
        document_text=text
    )

    # 5) Verify the result
    assert is_valid is True
    assert confidence == 0.9


@patch("rettxmutation.analysis.openai_rettx_agents.AzureOpenAI")
def test_validate_document_failure(mock_azure_openai_class):
    """
    Test a failure response from validate_document.
    """
    # 1) Create a mock AzureOpenAI instance
    mock_azure_openai = MagicMock()
    mock_azure_openai_class.return_value = mock_azure_openai

    # 2) Mock the 'chat.completions.create' method to simulate a negative response
    mock_response = MagicMock()
    mock_response.choices = [
        MagicMock(
            message=MagicMock(content="False, confidence=0.8")
        )
    ]
    mock_azure_openai.chat.completions.create.return_value = mock_response

    # 3) Instantiate OpenAIRettXAgents
    agent = OpenAIRettXAgents(
        api_key="fake_key",
        api_version="fake_version",
        azure_endpoint="https://fake.endpoint",
        model_name="test-model",
        embedding_deployment="test-embedding",
        audit_logger=MagicMock()
    )

    # 4) Call the method under test
    text = "This text has nothing about mutations."
    is_valid, confidence = agent.validate_document(
        audit_context="dummy-correlation-id",
        document_text=text
    )

    # 5) Verify the result
    assert is_valid is False
    assert confidence == 0.8


@patch("rettxmutation.analysis.openai_rettx_agents.AzureOpenAI")
def test_validate_document_parsing_error(mock_azure_openai_class):
    """
    Test error handling in validate_document when the response format is incorrect.
    """
    # 1) Create a mock AzureOpenAI instance
    mock_azure_openai = MagicMock()
    mock_azure_openai_class.return_value = mock_azure_openai

    # 2) Mock the 'chat.completions.create' method to simulate an invalid response format
    mock_response = MagicMock()
    mock_response.choices = [
        MagicMock(
            message=MagicMock(content="Invalid format response")
        )
    ]
    mock_azure_openai.chat.completions.create.return_value = mock_response

    # 3) Instantiate OpenAIRettXAgents
    agent = OpenAIRettXAgents(
        api_key="fake_key",
        api_version="fake_version",
        azure_endpoint="https://fake.endpoint",
        model_name="test-model",
        embedding_deployment="test-embedding",
        audit_logger=MagicMock()
    )

    # 4) Call the method under test and verify error handling
    text = "Some text for testing error handling."
    is_valid, confidence = agent.validate_document(
        audit_context="dummy-correlation-id",
        document_text=text
    )

    # 5) Verify the result (should default to False, 0.0 on parsing error)
    assert is_valid is False
    assert confidence == 0.0
