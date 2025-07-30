from pathlib import Path
from urllib.parse import urlparse, urlunparse

import typer
from fabric import Connection, Result
from fabric.transfer import Transfer
from loguru import logger

from dtu_compute.auth import AuthManager
from dtu_compute.config import ConfigManager


class ClusterConnection:
    """Class to manage the connection to the DTU Compute cluster.

    Args:
        user (str): The username for the connection.
        host (str): The hostname of the cluster.
        password (str): The password for the connection.
        key_file (str): Path to the SSH key file.
        hide (bool): Whether to hide the output of the command. Defaults to False.

    """

    def __init__(
        self,
        user: str,
        host: str,
        password: str,
        key_file: str,
        hide: bool = False,
        should_log: bool = False,
        log_file: Path | None = None,
    ) -> None:
        self.hide = hide
        self.conn = Connection(
            user=user,
            host=host,
            connect_kwargs={"key_filename": key_file, "password": password},
        )
        self.transfer = Transfer(self.conn)
        self.should_log = should_log
        if should_log:
            self.logger = logger
            self.logger.add(log_file)

    def run(self, command: str) -> Result:
        """Run a command on the remote cluster.

        Args:
            command: The command to run.

        Returns:
            Result: The result of the command execution.

        """
        if self.should_log:
            self.logger.info(f"Running command: {command}")
        return self.conn.run(f'bash -l -c "{command}"', hide=self.hide)

    def shell(self) -> None:
        """Start an interactive shell session on the remote cluster."""
        if self.should_log:
            self.logger.info("Starting interactive shell session.")
        self.conn.shell()

    def close(self) -> None:
        """Close the connection to the remote cluster."""
        self.conn.close()

    def get(self, remote_path: str, local_path: str | None = None) -> None:
        """Get a file from the remote cluster."""
        if self.should_log:
            self.logger.info(f"Getting file from {remote_path} to {local_path}")
        self.transfer.get(remote_path, local=local_path)

    def put(self, local_path: str, remote_path: str | None = None) -> None:
        """Put a file to the remote cluster."""
        if self.should_log:
            self.logger.info(f"Putting file from {local_path} to {remote_path}")
        self.transfer.put(local_path, remote=remote_path)

    def clone_or_pull_repo(
        self,
        repo_url: str,
        access_token: str | None = None,
        branch: str = "main",
    ) -> str:
        """Clone or pull a Git repository on the remote cluster and check out the desired branch.

        Args:
            repo_url (str): HTTPS URL of the repository.
            access_token (str | None): Personal access token if needed.
            branch (str): The branch to check out after cloning or pulling.

        """
        parsed_url = urlparse(repo_url)

        if access_token:
            # GitHub/GitLab token in HTTPS URL
            netloc = f"oauth2:{access_token}@{parsed_url.netloc}"
            repo_url = urlunparse(parsed_url._replace(netloc=netloc))  # type: ignore

        target_dir = parsed_url.path.rstrip("/").split("/")[-1].removesuffix(".git")

        # Check if directory already contains a Git repo
        result = self.run(f"if [ -d {target_dir}/.git ]; then echo 'exists'; fi")
        if "exists" in result.stdout.strip():
            if self.should_log:
                self.logger.info(f"Repository exists. Pulling latest changes in {target_dir}")
            self.run(f"cd {target_dir} && git fetch origin && git checkout {branch} && git pull origin {branch}")
        else:
            if self.should_log:
                self.logger.info(f"Cloning repository {repo_url} into {target_dir} (branch: {branch})")
            self.run(f"git clone --branch {branch} {repo_url} {target_dir}")

        return target_dir


def get_connection(config_file: Path, cluster: str, hide: bool = False) -> ClusterConnection:
    """Get a connection to the DTU Compute cluster.

    Args:
        config_file: Path to the configuration file
        cluster: The name of the cluster
        hide: Whether to hide the output of the command

    """
    if cluster not in ["hpc", "titans"]:
        raise ValueError(f"Invalid cluster name: {cluster}. Expected 'hpc' or 'titans'.")

    config_manager = ConfigManager(config_file)
    config = config_manager.load_config()

    auth_manager = AuthManager(config.auth.auth_method)
    user = config.auth.dtu_username
    password = auth_manager.get_auth(user)
    if password is None:
        typer.echo("No password found. Please set up authentication.")
        raise typer.Exit(code=1)

    if cluster == "hpc":
        host = config.hpc.host
        key_file = config.hpc.key_filename
    else:
        host = config.titans.host
        key_file = config.titans.key_filename

    key_file = str(Path(key_file).expanduser())

    return ClusterConnection(
        user=user,
        host=host,
        password=password,
        key_file=key_file,
        hide=hide,
        should_log=config.log.should_log,
        log_file=config.log.log_file,
    )
