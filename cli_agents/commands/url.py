import click

@click.command()
@click.option(
    "--model", default="llama-3.1-sonar-small-128k-online", help="Model to use for chat completion"
)
@click.option(
    "--uri", prompt="Enter URL", help="URL to summarize"
)
@click.pass_context
def url(ctx, model, uri):
    """Send a message to the chat model and get a response."""
    client = ctx.obj["perp_client"]
    response = client.chat.completions.create(
        model=model, messages=[{"role": "user", "content": f"summarize: {uri}"}]
    )
    click.echo(f"Response: {response.choices[0].message.content}")
