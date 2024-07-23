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
                "--staged",
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
def commit(ctx, model):
    """Send a message to the chat model and get a response."""
    client = ctx.obj["client"]
    diff_output = get_git_diff()
    message = f"""
You will be provided with the output from the `git diff --staged` command.
Your task is to craft a concise and descriptive commit message that accurately reflects the code and documentation changes.

Please adhere to the Conventional Commits specification, formatting the message as follows:
<type>(<scope>): <description>
<blank line>
<body>

- `type`: Choose one of the following based on the nature of the changes:
* feat: A new feature
* fix: A bug fix
* docs: Documentation changes
* style: Changes that do not affect the meaning of the code (formatting, whitespace, etc.)
* refactor: A code change that neither fixes a bug nor adds a feature
* perf: A code change that improves performance
* test: Adding missing tests or correcting existing tests
* build: Changes that affect the build system or external dependencies
* ci: Changes to the CI configuration files and scripts
* chore: Other changes that don't modify src or test files

- `scope` (optional): A specific area or module of the codebase that the changes affect, enclosed in parentheses (e.g., `feat(parser):`)
- `description`: A concise summary of the changes in a single, lowercase sentence without ending punctuation
- `blank line`: Add a blank line between the commit message and the body
- `body` (optional): A couple of paragraphs that provide additional contextual information about the changes.

Please provide only the commit message in your response, as it will be used directly in a git commit command.
    
{diff_output}
"""
    response = client.chat.completions.create(
        model=model, messages=[{"role": "system", "content": message}]
    )
    click.echo(f"{response.choices[0].message.content}")
