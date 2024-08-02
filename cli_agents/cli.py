import os
import click
from openai import OpenAI
from dotenv import load_dotenv
from .commands import chat, branch, commit, url

@click.group()
@click.pass_context
def cli(ctx):
    ctx.ensure_object(dict)
    load_dotenv()  # Load environment variables from .env file
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise click.ClickException("OPENAI_API_KEY not found in environment variables")
    ctx.obj["client"] = OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=api_key,
    )
    perp_api_key = os.getenv("PERPLEX_API_KEY")
    if not perp_api_key:
        raise click.ClickException("PERPLEX_API_KEY not found in environment variables")
    ctx.obj["perp_client"] = OpenAI(
        base_url="https://api.perplexity.ai",
        api_key=perp_api_key,
    )


cli.add_command(url.url)
cli.add_command(chat.chat)
cli.add_command(branch.branch)
cli.add_command(commit.commit)

if __name__ == "__main__":
    cli()
