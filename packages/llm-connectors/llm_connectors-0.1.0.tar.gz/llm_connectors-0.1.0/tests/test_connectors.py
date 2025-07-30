import pytest
from unittest.mock import patch, AsyncMock, MagicMock
from llm_connectors import ChatGPTConnector, GeminiConnector

def test_chatgpt_connector_initialization(mock_openai_api_key):
    """Test ChatGPT connector initialization."""
    connector = ChatGPTConnector(api_key=mock_openai_api_key)
    assert connector.api_key == mock_openai_api_key
    assert isinstance(connector.config, dict)

def test_gemini_connector_initialization(mock_google_api_key):
    """Test Gemini connector initialization."""
    connector = GeminiConnector(api_key=mock_google_api_key)
    assert connector.api_key == mock_google_api_key
    assert isinstance(connector.config, dict)

@pytest.mark.asyncio
async def test_chatgpt_chat_method(mock_openai_api_key):
    """Test ChatGPT chat method with mock response."""
    mock_completion = AsyncMock()
    mock_completion.model_dump = AsyncMock(return_value={
        "choices": [{"message": {"content": "Hi there!"}}]
    })
    
    mock_chat = AsyncMock()
    mock_chat.completions.create = AsyncMock(return_value=mock_completion)
    
    mock_client = AsyncMock()
    mock_client.chat = mock_chat

    with patch('openai.OpenAI', return_value=mock_client):
        connector = ChatGPTConnector(api_key=mock_openai_api_key)
        messages = [{"role": "user", "content": "Hello"}]
        response = await connector.chat(messages)
        assert isinstance(response, dict)
        assert "choices" in response

@pytest.mark.asyncio
async def test_gemini_chat_method(mock_google_api_key):
    """Test Gemini chat method with mock response."""
    mock_response = AsyncMock()
    mock_response.text = "Hi there!"
    
    mock_chat = AsyncMock()
    mock_chat.send_message = AsyncMock(return_value=mock_response)
    
    mock_model = AsyncMock()
    mock_model.start_chat = MagicMock(return_value=mock_chat)  # Use MagicMock instead of AsyncMock for start_chat

    with patch('google.generativeai.GenerativeModel', return_value=mock_model):
        connector = GeminiConnector(api_key=mock_google_api_key)
        messages = [{"role": "user", "content": "Hello"}]
        response = await connector.chat(messages)
        assert isinstance(response, dict)
        assert "content" in response

@pytest.mark.asyncio
async def test_chatgpt_generate_text(mock_openai_api_key):
    """Test ChatGPT text generation with mock response."""
    mock_completion = AsyncMock()
    mock_completion.choices = [AsyncMock()]
    mock_completion.choices[0].message.content = "This is a test response"
    
    mock_chat = AsyncMock()
    mock_chat.completions.create = AsyncMock(return_value=mock_completion)
    
    mock_client = AsyncMock()
    mock_client.chat = mock_chat

    with patch('openai.OpenAI', return_value=mock_client):
        connector = ChatGPTConnector(api_key=mock_openai_api_key)
        prompt = "Write a test"
        response = await connector.generate_text(prompt)
        assert isinstance(response, str)
        assert len(response) > 0

@pytest.mark.asyncio
async def test_gemini_generate_text(mock_google_api_key):
    """Test Gemini text generation with mock response."""
    mock_response = AsyncMock()
    mock_response.text = "This is a test response"
    
    mock_model = AsyncMock()
    mock_model.generate_content = AsyncMock(return_value=mock_response)

    with patch('google.generativeai.GenerativeModel', return_value=mock_model):
        connector = GeminiConnector(api_key=mock_google_api_key)
        prompt = "Write a test"
        response = await connector.generate_text(prompt)
        assert isinstance(response, str)
        assert len(response) > 0 