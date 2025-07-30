import pytest

from dtu_compute.auth import AuthManager


def test_init_valid_methods():
    """Test that AuthManager can be initialized with valid methods."""
    auth_manager_password = AuthManager("password")
    assert auth_manager_password.auth_method == "password"

    auth_manager_keyring = AuthManager("keyring")
    assert auth_manager_keyring.auth_method == "keyring"


def test_init_invalid_method():
    """Test that AuthManager raises ValueError with invalid method."""
    with pytest.raises(ValueError):
        AuthManager("invalid_method")


def test_setup_auth_keyring(monkeypatch):
    """Test setup_auth with keyring method."""
    # Create a mock for keyring.set_password
    mock_calls = []

    def mock_set_password(service, username, password):
        mock_calls.append((service, username, password))

    monkeypatch.setattr("keyring.set_password", mock_set_password)

    auth_manager = AuthManager("keyring")
    auth_manager.setup_auth("test_user", "test_password")

    assert mock_calls == [("dtu_compute", "test_user", "test_password")]


def test_setup_auth_password(monkeypatch):
    """Test setup_auth with password method."""
    # Create a mock for keyring.set_password to ensure it's not called
    mock_calls = []

    def mock_set_password(service, username, password):
        mock_calls.append((service, username, password))

    monkeypatch.setattr("keyring.set_password", mock_set_password)

    auth_manager = AuthManager("password")
    auth_manager.setup_auth("test_user", "test_password")

    assert mock_calls == []  # No calls should be made


def test_get_auth_keyring(monkeypatch):
    """Test get_auth with keyring method."""

    # Mock keyring.get_password to return a test password
    def mock_get_password(service, username):
        assert service == "dtu_compute"
        assert username == "test_user"
        return "test_password"

    monkeypatch.setattr("keyring.get_password", mock_get_password)

    auth_manager = AuthManager("keyring")
    password = auth_manager.get_auth("test_user")

    assert password == "test_password"


def test_get_auth_password(monkeypatch):
    """Test get_auth with password method."""

    # Mock typer.prompt to return a test password
    def mock_prompt(prompt_text, type, hide_input):
        assert prompt_text == "Enter your DTU Compute password"
        assert type is str
        assert hide_input is True
        return "test_password"

    monkeypatch.setattr("typer.prompt", mock_prompt)

    auth_manager = AuthManager("password")
    password = auth_manager.get_auth("test_user")

    assert password == "test_password"


def test_delete_auth_keyring(monkeypatch):
    """Test delete_auth with keyring method."""
    # Create a mock for keyring.delete_password
    mock_calls = []

    def mock_delete_password(service, username):
        mock_calls.append((service, username))

    monkeypatch.setattr("keyring.delete_password", mock_delete_password)

    auth_manager = AuthManager("keyring")
    auth_manager.delete_auth("test_user")

    assert mock_calls == [("dtu_compute", "test_user")]


def test_delete_auth_password(monkeypatch):
    """Test delete_auth with password method - should not call keyring."""
    # Create a mock for keyring.delete_password to ensure it's not called
    mock_calls = []

    def mock_delete_password(service, username):
        mock_calls.append((service, username))

    monkeypatch.setattr("keyring.delete_password", mock_delete_password)

    auth_manager = AuthManager("password")
    auth_manager.delete_auth("test_user")

    assert mock_calls == []  # No calls should be made
