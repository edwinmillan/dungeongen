import pytest

from src.chat import coverage_test, send_prompt


@pytest.mark.asyncio
async def test_send_prompt(mock_chat_response_post):
    prompt = "What is the meaning of life?"
    response = await send_prompt(prompt)
    assert response == "42"


@pytest.mark.asyncio
async def test_send_prompt_error(mock_chat_response_post_wrong_url):
    prompt = "What is the meaning of life?"
    response = await send_prompt(prompt)
    assert response == {}


def test_coverage():
    assert coverage_test() is True
