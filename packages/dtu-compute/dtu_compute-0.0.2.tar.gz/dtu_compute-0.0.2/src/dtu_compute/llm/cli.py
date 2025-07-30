from pathlib import Path
from typing import Annotated

import openai
import typer

from dtu_compute.config import ConfigManager

app = typer.Typer(no_args_is_help=True)

chat_history = [{"role": "system", "content": "You are a helpful assistant."}]


@app.command()
def chat(
    config_file: Annotated[Path, typer.Option(help="Path for the configuration file")] = Path("dtu.toml"),
    model: Annotated[str, typer.Option(help="Model to use for the chat session")] = "CampusAI.gemma3:latest",
):
    """Start a chat session with the CampusAI model."""
    typer.echo("Welcome to the CampusAI Chat! Type 'exit' to quit.\n")

    # Load configuration
    config_manager = ConfigManager(config_file)
    config = config_manager.load_config()

    client = openai.OpenAI(
        api_key=config.campus_ai.api_key,
        base_url=config.campus_ai.base_url,
    )

    while True:
        try:
            user_input = typer.prompt("You")

            if user_input.lower() in ["exit", "quit"]:
                typer.echo("Exiting. Goodbye!")
                break

            chat_history.append({"role": "user", "content": user_input})

            typer.secho("\nAssistant: ", fg=typer.colors.GREEN, nl=False)

            stream = client.chat.completions.create(model=model, messages=chat_history, stream=True)

            assistant_reply = ""
            for chunk in stream:
                content = chunk.choices[0].delta.content
                if content:
                    print(content, end="", flush=True)
                    assistant_reply += content

            print("\n")  # for newline after full message
            chat_history.append({"role": "assistant", "content": assistant_reply})

        except KeyboardInterrupt:
            typer.echo("\nInterrupted. Exiting.")
            break
        except Exception as e:
            typer.secho(f"\nError: {e}", fg=typer.colors.RED)
