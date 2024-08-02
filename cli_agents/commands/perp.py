import click

@click.command()
@click.option(
    "--model", default="llama-3.1-sonar-small-128k-online", help="Model to use for chat completion"
)
@click.option(
    "--message", prompt="Enter your message", help="Message to send to the chat model"
)
@click.pass_context
def perp(ctx, model, message):
    """Send a message to the chat model and get a response."""
    client = ctx.obj["perp_client"]
    response = client.chat.completions.create(
        model=model, messages=[{"role": "user", "content": message}]
    )
    click.echo(f"Response: {response.choices[0].message.content}")
