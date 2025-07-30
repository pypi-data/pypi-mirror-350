import os
from pathlib import Path
from typing import Annotated

import typer

from dtu_compute.auth import AuthManager
from dtu_compute.config import ConfigManager
from dtu_compute.hpc.cli import app as hpc_cli
from dtu_compute.llm.cli import app as llm_cli
from dtu_compute.titans.cli import app as titans_cli
from dtu_compute.utils import add_to_gitignore, get_default_branch

cli = typer.Typer(no_args_is_help=True)
cli.add_typer(hpc_cli, name="hpc", help="Commands for managing the DTU Compute HPC cluster.")
cli.add_typer(titans_cli, name="titans", help="Commands for managing the DTU Compute Titans cluster.")
cli.add_typer(llm_cli, name="llm", help="Commands for managing the DTU campus LLM.")


@cli.callback()
def welcome():
    """Welcome to the DTU Compute CLI.

    This CLI provides commands for managing the DTU Compute cluster, LLM, and Titans cluster.
    """


@cli.command()
def auth(auth_method: str, clear: bool = False):
    """Store encrypted credentials for the DTU Compute cluster."""
    auth_manager = AuthManager(auth_method)

    username = typer.prompt("Enter your DTU Compute username", type=str)

    if clear:
        auth_manager.delete_auth(username)
        typer.echo(f"Deleted authentication for {username}.")
        return

    password = typer.prompt("Enter your DTU Compute password", type=str, hide_input=True)

    auth_manager.setup_auth(username, password)


@cli.command()
def init(
    config_file: Annotated[Path, typer.Option(help="Path for the configuration file")] = Path("dtu.toml"),
) -> None:
    """Initialize a new DTU Compute project configuration file."""
    config_manager = ConfigManager(config_file)

    # If a specific file is specified, check if it exists
    if config_file.exists():
        typer.echo(f"Configuration file already exists at {config_file}.")
        typer.confirm("Do you want to overwrite it?", abort=True)

    # Auth config
    typer.echo("====== Auth config ======")
    dtu_username = typer.prompt("DTU username", type=str, default=os.getenv("USER", ""))
    auth_method = typer.prompt("Authentication method (password or keyring)", type=str, default="keyring")
    if auth_method not in ["password", "keyring"]:
        typer.echo(f"Invalid authentication method: {auth_method}.")
        raise typer.Exit(code=1)
    if auth_method == "keyring":
        password = typer.prompt("Enter your DTU password", type=str, hide_input=True)
        auth_manager = AuthManager(auth_method)
        auth_manager.setup_auth(dtu_username, password)

    # HPC SSH config
    typer.echo("====== HPC config ======")
    hpc_ssh_host = typer.prompt("HPC SSH login host", type=str, default="login1.hpc.dtu.dk")
    hpc_ssh_key = typer.prompt("Path to HPC SSH key file", default="~/.ssh/dtu_hpc")

    # Titans SSH config
    typer.echo("====== Titans config ======")
    titans_ssh_host = typer.prompt("Titans SSH login host", type=str, default="titans")
    titans_ssh_key = typer.prompt("Path to Titans SSH key file", default="~/.ssh/dtu_hpc")

    # LLM config
    typer.echo("====== LLM config ======")
    base_url = typer.prompt("LLM host", type=str, default="https://campusai.compute.dtu.dk/api")
    api_key = typer.prompt("LLM API key", type=str, default="")

    # Repo config
    typer.echo("====== Repository config ======")
    git_user = typer.prompt("Git username", type=str, default="")
    repository = typer.prompt("Repository URL", type=str, default="")
    token = typer.prompt("Repository access token (leave empty if not needed)", type=str, default="")
    default_branch = typer.prompt("Default deployment branch", default=get_default_branch(Path(".")))

    # Log config
    typer.echo("====== Log config ======")
    should_log = typer.confirm("Should we log to a file?", default=True)
    log_file = ".dtu_compute.log"
    if should_log:
        log_file = typer.prompt("Path to log file", type=str, default=".dtu_compute.log")

    # Create the configuration data
    config_data = {
        "auth": {
            "dtu_username": dtu_username,
            "auth_method": auth_method,
        },
        "hpc": {
            "host": hpc_ssh_host,
            "key_filename": hpc_ssh_key,
        },
        "titans": {
            "host": titans_ssh_host,
            "key_filename": titans_ssh_key,
        },
        "campus_ai": {
            "base_url": base_url,
            "api_key": api_key,
        },
        "repo": {
            "git_user": git_user,
            "repository": repository,
            "token": token,
            "default_branch": default_branch,
        },
        "log": {
            "should_log": should_log,
            "log_file": log_file,
        },
    }

    # Set up the configuration
    config_manager.setup_config(config_data)
    typer.echo(f"Configuration file created at {config_file}. Adding to .gitignore.")
    add_to_gitignore(config_file)
