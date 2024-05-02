import pytest

from src.dungeongen.chat import send_prompt


@pytest.mark.asyncio
async def test_send_prompt(mock_chat_response_post):
    """Test that the send_prompt function returns the expected response."""
    prompt = "What is the meaning of life?"
    response = await send_prompt(prompt)
    assert response == "42"


@pytest.mark.asyncio
async def test_send_prompt_error(mock_chat_response_post_wrong_url):
    """Test that the send_prompt function returns an empty response when the URL is wrong."""
    prompt = "What is the meaning of life?"
    response = await send_prompt(prompt)
    assert response == {}
