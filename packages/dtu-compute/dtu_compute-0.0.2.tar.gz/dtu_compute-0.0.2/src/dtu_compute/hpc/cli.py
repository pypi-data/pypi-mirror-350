from pathlib import Path
from typing import Annotated

import typer

from dtu_compute.config import ConfigManager
from dtu_compute.connection import get_connection
from dtu_compute.hpc.submit import LSFJob
from dtu_compute.run_config import ConfigProcessor
from dtu_compute.sweep import SweepProcessor

app = typer.Typer(no_args_is_help=True)


@app.command()
def ssh(
    config_file: Annotated[Path, typer.Option(help="Path for the configuration file")] = Path("dtu.toml"),
):
    """SSH into the DTU Compute cluster."""
    connection = get_connection(config_file, cluster="hpc")
    connection.shell()
    connection.close()


@app.command()
def run(
    command: Annotated[str, typer.Argument(help="Command to run on the cluster")],
    config_file: Annotated[Path, typer.Option(help="Path for the configuration file")] = Path("dtu.toml"),
):
    """Run a command on the DTU Compute cluster."""
    connection = get_connection(config_file, cluster="hpc")
    result = connection.run(command)
    if result.exited != 0:
        typer.echo(f"Command failed with exit code {result.exited}")
        raise typer.Exit(code=result.exited)
    raise typer.Exit(code=0)


@app.command()
def get(
    remote_path: Annotated[Path, typer.Argument(help="Remote path to get")],
    local_path: Annotated[Path | None, typer.Argument(help="Local path to save the file")] = None,
    config_file: Annotated[Path, typer.Option(help="Path for the configuration file")] = Path("dtu.toml"),
):
    """Get a file from the DTU Compute cluster."""
    connection = get_connection(config_file, cluster="hpc")
    connection.get(str(remote_path), str(local_path) if local_path else None)


@app.command()
def put(
    local_path: Annotated[Path, typer.Argument(help="Local path to put")],
    remote_path: Annotated[Path | None, typer.Argument(help="Remote path to save the file")] = None,
    config_file: Annotated[Path, typer.Option(help="Path for the configuration file")] = Path("dtu.toml"),
):
    """Put a file to the DTU Compute cluster."""
    connection = get_connection(config_file, cluster="hpc")
    connection.put(str(local_path), str(remote_path) if remote_path else None)


@app.command()
def submit(
    run_config: Annotated[Path, typer.Argument(help="Path to the run configuration file")],
    config_file: Annotated[Path, typer.Option(help="Path for the configuration file")] = Path("dtu.toml"),
):
    """Submit a job to the DTU Compute cluster."""
    processor = ConfigProcessor(run_config)
    job = processor.get_job_config()

    config_manager = ConfigManager(config_file)
    config = config_manager.load_config()

    connection = get_connection(config_file, cluster="hpc")
    target_dir = connection.clone_or_pull_repo(
        repo_url=config.repo.repository,
        access_token=config.repo.token,
        branch=config.repo.default_branch,
    )
    lfsjob = LSFJob(job, target_dir=target_dir)
    lfsjob.submit(connection)


@app.command()
def sweep(
    run_config: Annotated[Path, typer.Argument(help="Path to the run configuration file")],
    config_file: Annotated[Path, typer.Option(help="Path for the configuration file")] = Path("dtu.toml"),
):
    """Submit a sweep job to the DTU Compute cluster."""
    processor = SweepProcessor(run_config)
    jobs = processor.get_job_config()

    config_manager = ConfigManager(config_file)
    config = config_manager.load_config()

    connection = get_connection(config_file, cluster="hpc")
    target_dir = connection.clone_or_pull_repo(
        repo_url=config.repo.repository,
        access_token=config.repo.token,
        branch=config.repo.default_branch,
    )
    for job in jobs:
        # Submit each job in the sweep
        lsfjob = LSFJob(job, target_dir=target_dir)
        lsfjob.submit(connection)
