import os
import click
from openai import OpenAI
from dotenv import load_dotenv
from .commands import chat, branch, commit


@click.group()
@click.pass_context
def cli(ctx):
    """OpenAI CLI tool for chat completions and text completions."""
    load_dotenv()  # Load environment variables from .env file
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise click.ClickException("OPENAI_API_KEY not found in environment variables")
    ctx.ensure_object(dict)
    ctx.obj["client"] = OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=api_key,
    )


cli.add_command(chat.chat)
cli.add_command(branch.branch)
cli.add_command(commit.commit)

if __name__ == "__main__":
    cli()
