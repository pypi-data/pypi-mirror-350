from invoke import Context, task


@task
def tests(ctx: Context) -> None:
    """Test and coverage."""
    ctx.run("uv run coverage run -m pytest tests/ -v", echo=True, pty=True)
    ctx.run("uv run coverage report -i -m", echo=True, pty=True)


@task
def check(ctx: Context) -> None:
    """Check code with pre-commit."""
    ctx.run("uv run pre-commit run --all-files", echo=True, pty=True)


@task(pre=[check, tests])
def all(ctx: Context) -> None:
    """Run all tasks."""
    pass
