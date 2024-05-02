import asyncio

import pytest

from src.dungeongen.main import (
    display_encounter,
    display_menu,
    parse_boolean,
    send_prompt_with_spinner,
    spinner_function,
)


def test_display_menu(capsys):
    """Test that the display_menu function prints the expected output."""
    display_menu(chat_narration=True)
    captured = capsys.readouterr()
    assert "E Rank Gate" in captured.out
    assert "D Rank Gate" in captured.out
    assert "C Rank Gate" in captured.out
    assert "B Rank Gate" in captured.out
    assert "A Rank Gate" in captured.out
    assert "S Rank Gate" in captured.out
    assert "SS Rank Gate" in captured.out
    assert "Random Gate" in captured.out
    assert "Toggle chat narration" in captured.out
    assert "Display these options again" in captured.out
    assert "Quit the Dungeon Generator" in captured.out


def test_narration_toggle(capsys):
    display_menu(chat_narration=True)
    captured = capsys.readouterr()
    assert "currently enabled" in captured.out

    display_menu(chat_narration=False)
    captured = capsys.readouterr()
    assert "currently disabled" in captured.out


def test_display_encounter(capsys):
    """Test that the display_encounter function prints the expected output."""
    encounter = {
        "rank": "A",
        "monsters": [
            {"wave": 1, "monster": "Goblin", "wave_size": 3},
            {"wave": 2, "monster": "Orc", "wave_size": 2},
        ],
        "boss": "Troll",
    }

    display_encounter(encounter)
    captured = capsys.readouterr()

    assert "Rank: A" in captured.out
    assert "Monsters: Total: 5, Waves: 2" in captured.out
    assert "Wave 1 Goblin x3" in captured.out
    assert "Wave 2 Orc x2" in captured.out
    assert "Boss: Troll" in captured.out


@pytest.mark.asyncio
async def test_spinner_function(capsys):
    """Test that the spinner function prints the expected output."""
    task = asyncio.create_task(spinner_function("Testing"))

    await asyncio.sleep(0.5)
    task.cancel()

    # Wait for the task to be cancelled
    try:
        await task
    except asyncio.CancelledError:
        pass

    captured = capsys.readouterr()

    assert captured.out.startswith("\rTesting: |")
    assert "\rTesting: /" in captured.out
    assert "\rTesting: -" in captured.out
    assert "\rTesting: \\" in captured.out


@pytest.mark.asyncio
async def test_send_prompt_with_spinner(monkeypatch, capsys):
    """Test that the send_prompt_with_spinner function returns the expected response."""

    async def mock_send_prompt(prompt):
        assert prompt == "prompt"
        return "response"

    monkeypatch.setattr("src.dungeongen.main.send_prompt", mock_send_prompt)

    # Mock spinner_function to do nothing
    async def mock_spinner_function(prompt):
        pass

    monkeypatch.setattr("src.dungeongen.main.spinner_function", mock_spinner_function)

    result = await send_prompt_with_spinner("prompt")
    assert result == "response"

    captured = capsys.readouterr()
    assert captured.out == " Done!\n"


@pytest.mark.parametrize(
    "input_value,expected",
    [
        (True, True),
        ("True", True),
        ("true", True),
        ("1", True),
        (1, True),
        ("yes", True),
        ("YES", True),
        (False, False),
        ("False", False),
        ("false", False),
        ("0", False),
        (0, False),
        ("no", False),
        ("NO", False),
    ],
)
def test_parse_boolean(input_value, expected):
    """Test that the parse_boolean function returns the expected results."""
    assert parse_boolean(input_value) is expected
