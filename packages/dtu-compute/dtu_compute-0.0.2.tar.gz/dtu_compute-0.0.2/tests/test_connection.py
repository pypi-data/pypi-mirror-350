import os
import tempfile
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

from dtu_compute.config import AuthConfig, Config, HPCSSHConfig, LogConfig, RepoConfig, TitansSSHConfig
from dtu_compute.connection import ClusterConnection, get_connection


@pytest.fixture
def mock_config():
    """Create a mock configuration for testing."""
    return Config(  # ty:ignore
        auth=AuthConfig(auth_method="ssh", dtu_username="testuser"),
        hpc=HPCSSHConfig(
            host="login.hpc.dtu.dk",
            key_filename="~/.ssh/id_rsa",
        ),
        titans=TitansSSHConfig(
            host="titans.compute.dtu.dk",
            key_filename="~/.ssh/id_rsa",
        ),
        repo=RepoConfig(
            git_user="testuser",
            repository="test_project",
            token="ghp_sample_token",
            default_branch="main",
        ),
        log=LogConfig(
            should_log=False,
            log_file=Path(""),
        ),
    )


@pytest.fixture
def temp_config_file():
    """Create a temporary file for config testing."""
    with tempfile.NamedTemporaryFile(suffix=".toml", delete=False) as tmp:
        temp_path = Path(tmp.name)
    try:
        yield temp_path
    finally:
        # Ensure the file is deleted after the test
        if temp_path.exists():
            os.unlink(temp_path)


@patch("dtu_compute.connection.Connection")
def test_cluster_connection_run(mock_connection_cls):
    """Test that the run method executes a command on the cluster."""
    mock_conn = MagicMock()
    mock_result = MagicMock()
    mock_result.stdout = "success"
    mock_conn.run.return_value = mock_result
    mock_connection_cls.return_value = mock_conn

    cc = ClusterConnection(user="user", host="host", password="pw", key_file="~/.ssh/id_rsa", hide=True)
    result = cc.run("echo hello")

    mock_conn.run.assert_called_once_with('bash -l -c "echo hello"', hide=True)
    assert result.stdout == "success"


@patch("dtu_compute.connection.Connection")
def test_cluster_connection_shell(mock_connection_cls):
    """Test that the shell method returns a shell object."""
    mock_conn = MagicMock()
    mock_connection_cls.return_value = mock_conn

    cc = ClusterConnection(user="user", host="host", password="pw", key_file="~/.ssh/id_rsa")
    cc.shell()
    mock_conn.shell.assert_called_once()


@patch("dtu_compute.connection.Connection")
def test_cluster_connection_close(mock_connection_cls):
    """Test that the connection closes properly."""
    mock_conn = MagicMock()
    mock_connection_cls.return_value = mock_conn

    cc = ClusterConnection(user="user", host="host", password="pw", key_file="~/.ssh/id_rsa")
    cc.close()
    mock_conn.close.assert_called_once()


@patch("dtu_compute.connection.logger")
@patch("dtu_compute.connection.Connection")
def test_cluster_connection_logging(mock_connection_cls, mock_logger):
    """Test that the connection logs the command when should_log is True."""
    mock_conn = MagicMock()
    mock_result = MagicMock()
    mock_result.stdout = "logged"
    mock_conn.run.return_value = mock_result
    mock_connection_cls.return_value = mock_conn

    cc = ClusterConnection(
        user="user",
        host="host",
        password="pw",
        key_file="~/.ssh/id_rsa",
        hide=False,
        should_log=True,
        log_file=Path("test.log"),
    )
    cc.run("echo test")

    mock_logger.info.assert_called_with("Running command: echo test")
    mock_conn.run.assert_called_once()


@patch("dtu_compute.connection.Connection")
@patch("dtu_compute.connection.Transfer")
def test_cluster_connection_get(mock_transfer_cls, mock_connection_cls):
    """Test that the get method transfers a file from the remote cluster."""
    mock_conn = MagicMock()
    mock_connection_cls.return_value = mock_conn

    mock_transfer = MagicMock()
    mock_transfer_cls.return_value = mock_transfer

    cc = ClusterConnection(user="user", host="host", password="pw", key_file="~/.ssh/id_rsa")
    cc.get("remote.txt", "local.txt")

    mock_transfer.get.assert_called_once_with("remote.txt", local="local.txt")


@patch("dtu_compute.connection.Connection")
@patch("dtu_compute.connection.Transfer")
def test_cluster_connection_put(mock_transfer_cls, mock_connection_cls):
    """Test that the put method transfers a file to the remote cluster."""
    mock_conn = MagicMock()
    mock_connection_cls.return_value = mock_conn

    mock_transfer = MagicMock()
    mock_transfer_cls.return_value = mock_transfer

    cc = ClusterConnection(user="user", host="host", password="pw", key_file="~/.ssh/id_rsa")
    cc.put("local.txt", "remote.txt")

    mock_transfer.put.assert_called_once_with("local.txt", remote="remote.txt")


@patch("dtu_compute.connection.Connection")
def test_clone_or_pull_repo_clone_new(mock_connection_cls):
    """Test that clone_or_pull_repo clones a repository if it doesn't exist."""
    mock_conn = MagicMock()
    mock_result = MagicMock()
    mock_result.stdout = ""  # Directory doesn't exist
    mock_conn.run.return_value = mock_result
    mock_connection_cls.return_value = mock_conn

    cc = ClusterConnection(user="user", host="host", password="pw", key_file="~/.ssh/id_rsa")
    result = cc.clone_or_pull_repo("https://github.com/username/repo.git", branch="dev")

    assert result == "repo"
    mock_conn.run.assert_any_call("bash -l -c \"if [ -d repo/.git ]; then echo 'exists'; fi\"", hide=False)
    mock_conn.run.assert_any_call(
        'bash -l -c "git clone --branch dev https://github.com/username/repo.git repo"', hide=False
    )


@patch("dtu_compute.connection.Connection")
def test_clone_or_pull_repo_pull_existing(mock_connection_cls):
    """Test that clone_or_pull_repo pulls a repository if it exists."""
    mock_conn = MagicMock()
    mock_result = MagicMock()
    mock_result.stdout = "exists"  # Directory exists
    mock_conn.run.return_value = mock_result
    mock_connection_cls.return_value = mock_conn

    cc = ClusterConnection(user="user", host="host", password="pw", key_file="~/.ssh/id_rsa")
    result = cc.clone_or_pull_repo("https://github.com/username/repo.git")

    assert result == "repo"
    mock_conn.run.assert_any_call("bash -l -c \"if [ -d repo/.git ]; then echo 'exists'; fi\"", hide=False)
    mock_conn.run.assert_any_call(
        'bash -l -c "cd repo && git fetch origin && git checkout main && git pull origin main"', hide=False
    )


@patch("dtu_compute.connection.Connection")
def test_clone_or_pull_repo_with_token(mock_connection_cls):
    """Test that clone_or_pull_repo properly adds the access token to the URL."""
    mock_conn = MagicMock()
    mock_result = MagicMock()
    mock_result.stdout = ""  # Directory doesn't exist
    mock_conn.run.return_value = mock_result
    mock_connection_cls.return_value = mock_conn

    cc = ClusterConnection(user="user", host="host", password="pw", key_file="~/.ssh/id_rsa")
    cc.clone_or_pull_repo("https://github.com/username/repo.git", access_token="abc123")

    # Check that the token was added to the URL in the clone command
    expected_url = "https://oauth2:abc123@github.com/username/repo.git"
    mock_conn.run.assert_any_call(f'bash -l -c "git clone --branch main {expected_url} repo"', hide=False)


@patch("dtu_compute.connection.logger")
@patch("dtu_compute.connection.Connection")
def test_clone_or_pull_repo_with_logging(mock_connection_cls, mock_logger):
    """Test that clone_or_pull_repo logs operations when logging is enabled."""
    mock_conn = MagicMock()
    mock_result = MagicMock()
    mock_result.stdout = ""  # Directory doesn't exist
    mock_conn.run.return_value = mock_result
    mock_connection_cls.return_value = mock_conn

    cc = ClusterConnection(
        user="user",
        host="host",
        password="pw",
        key_file="~/.ssh/id_rsa",
        should_log=True,
        log_file=Path("test.log"),
    )

    cc.clone_or_pull_repo("https://github.com/username/repo.git")

    # Verify logging occurred
    mock_logger.info.assert_any_call("Cloning repository https://github.com/username/repo.git into repo (branch: main)")


@patch("dtu_compute.connection.ConfigManager")
@patch("dtu_compute.connection.AuthManager")
def test_get_connection(mock_auth_manager_cls, mock_config_manager_cls):
    """Test that get_connection creates the correct connection object."""
    # Setup mocks
    mock_auth_manager = MagicMock()
    mock_auth_manager.get_auth.return_value = "password123"
    mock_auth_manager_cls.return_value = mock_auth_manager

    mock_config_manager = MagicMock()
    mock_config = MagicMock()
    mock_config.auth.auth_method = "ssh"
    mock_config.auth.dtu_username = "testuser"
    mock_config.hpc.host = "login.hpc.dtu.dk"
    mock_config.hpc.key_filename = "~/.ssh/id_rsa"
    mock_config.titans.host = "titans.compute.dtu.dk"
    mock_config.titans.key_filename = "~/.ssh/titans_key"
    mock_config.log.should_log = True
    mock_config.log.log_file = Path("test.log")
    mock_config_manager.load_config.return_value = mock_config
    mock_config_manager_cls.return_value = mock_config_manager

    # Patch ClusterConnection to check arguments
    with patch("dtu_compute.connection.ClusterConnection") as mock_cluster_connection_cls:
        mock_cluster_connection = MagicMock()
        mock_cluster_connection_cls.return_value = mock_cluster_connection

        # Test HPC connection
        get_connection(Path("config.toml"), "hpc", hide=True)

        # Verify correct arguments were passed
        mock_cluster_connection_cls.assert_called_with(
            user="testuser",
            host="login.hpc.dtu.dk",
            password="password123",
            key_file=str(Path("~/.ssh/id_rsa").expanduser()),
            hide=True,
            should_log=True,
            log_file=Path("test.log"),
        )

        # Reset mock to test Titans connection
        mock_cluster_connection_cls.reset_mock()

        # Test Titans connection
        get_connection(Path("config.toml"), "titans")

        # Verify correct arguments were passed
        mock_cluster_connection_cls.assert_called_with(
            user="testuser",
            host="titans.compute.dtu.dk",
            password="password123",
            key_file=str(Path("~/.ssh/titans_key").expanduser()),
            hide=False,
            should_log=True,
            log_file=Path("test.log"),
        )


def test_get_connection_invalid_cluster():
    """Test that get_connection raises a ValueError for invalid cluster names."""
    with pytest.raises(ValueError, match="Invalid cluster name: invalid. Expected 'hpc' or 'titans'."):
        get_connection(Path("config.yaml"), "invalid")
