import subprocess
import click

def get_git_root():
    try:
        return (
            subprocess.check_output(
                ["git", "rev-parse", "--show-toplevel"], stderr=subprocess.DEVNULL
            )
            .decode("utf-8")
            .strip()
        )
    except subprocess.CalledProcessError:
        raise click.ClickException("Not in a git repository.")


def get_git_diff():
    git_root = get_git_root()
    try:
        return subprocess.check_output(
            [
                "git",
                "--no-pager",
                "diff",
                "--minimal",
                "--no-color",
                "--function-context",
                "--no-ext-diff",
                "--",
                ":(exclude)*.lock*",
                ":(exclude)*-lock.*",
            ],
            cwd=git_root,
        ).decode("utf-8")
    except subprocess.CalledProcessError:
        raise click.ClickException("Not a git repository or no changes")


@click.command()
@click.option(
    "--model", default="openai/gpt-4o-mini", help="Model to use for chat completion"
)
@click.pass_context
def branch(ctx, model):
    """Send a message to the chat model and get a response."""
    client = ctx.obj["client"]
    diff_output = get_git_diff()
    message = f'''
    You will be provided with the output from the `git diff` command.
    Your task is to suggest three to five branch names from the output.
    Please provide only the branch name in your response, as it will be used directly in a `git checkout -b` command.
    
    {diff_output}
    '''
    response = client.chat.completions.create(
    model=model, messages=[{"role": "system", 
                            "content": message}]
    )
    click.echo(f"{response.choices[0].message.content}")
