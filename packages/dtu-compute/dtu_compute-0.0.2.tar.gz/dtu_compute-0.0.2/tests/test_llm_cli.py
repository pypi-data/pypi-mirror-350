from unittest.mock import MagicMock, patch

import pytest
from typer.testing import CliRunner

from dtu_compute.llm.cli import app

runner = CliRunner()


@pytest.fixture
def mock_config():
    """Fixture to create a mock configuration for testing."""
    mock_config = MagicMock()
    mock_config.campus_ai.api_key = "fake-key"
    mock_config.campus_ai.base_url = "https://fake.api"
    return mock_config


def mock_stream_response():
    """Mock function to simulate OpenAI streaming response."""

    class FakeDelta:
        def __init__(self, content):
            self.content = content

    class FakeChoice:
        def __init__(self, delta):
            self.delta = delta

    class FakeChunk:
        def __init__(self, content):
            self.choices = [FakeChoice(FakeDelta(content))]

    # simulate a stream of 3 tokens
    yield FakeChunk("Hello")
    yield FakeChunk(", ")
    yield FakeChunk("world!")


@patch("dtu_compute.llm.cli.ConfigManager")
@patch("dtu_compute.llm.cli.openai.OpenAI")
@patch("dtu_compute.llm.cli.typer.prompt")
def test_chat_command_happy_path(mock_prompt, mock_openai, MockConfigManager, mock_config):
    """Test the happy path of the chat command."""
    # Mock prompt input
    mock_prompt.side_effect = ["Hi", "exit"]

    # Mock config manager
    MockConfigManager.return_value.load_config.return_value = mock_config

    # Mock OpenAI streaming chat response
    mock_client = MagicMock()
    mock_client.chat.completions.create.return_value = mock_stream_response()
    mock_openai.return_value = mock_client

    result = runner.invoke(app)

    assert result.exit_code == 0
    assert "Welcome to the CampusAI Chat!" in result.output
    assert "Hello, world!" in result.output or "Hello" in result.output  # Output depends on print stream
    assert "Exiting. Goodbye!" in result.output


@patch("dtu_compute.llm.cli.ConfigManager")
@patch("dtu_compute.llm.cli.openai.OpenAI")
@patch("dtu_compute.llm.cli.typer.prompt")
def test_chat_command_keyboard_interrupt(mock_prompt, mock_openai, MockConfigManager, mock_config):
    """Test handling of keyboard interrupt during chat command."""
    mock_prompt.side_effect = KeyboardInterrupt

    MockConfigManager.return_value.load_config.return_value = mock_config
    mock_openai.return_value = MagicMock()

    result = runner.invoke(app)

    assert result.exit_code == 0
    assert "Interrupted. Exiting." in result.output
