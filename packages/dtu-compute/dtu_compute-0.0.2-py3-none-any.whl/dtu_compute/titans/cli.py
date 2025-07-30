from pathlib import Path
from typing import Annotated

import typer

from dtu_compute.connection import get_connection

app = typer.Typer(no_args_is_help=True)


@app.command()
def ssh(
    config_file: Annotated[Path, typer.Option(help="Path for the configuration file")] = Path("dtu.toml"),
):
    """SSH into the DTU Compute Titans cluster."""
    connection = get_connection(config_file, cluster="titans")
    connection.shell()
    connection.close()


@app.command()
def run(
    command: Annotated[str, typer.Argument(help="Command to run on the cluster")],
    config_file: Annotated[Path, typer.Option(help="Path for the configuration file")] = Path("dtu.toml"),
):
    """Run a command on the DTU Compute cluster."""
    connection = get_connection(config_file, cluster="titans")
    result = connection.run(command)
    if result.exited != 0:
        typer.echo(f"Command failed with exit code {result.exited}")
        raise typer.Exit(code=result.exited)
    raise typer.Exit(code=0)
