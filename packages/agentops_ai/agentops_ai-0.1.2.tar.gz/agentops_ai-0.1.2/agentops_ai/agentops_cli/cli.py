import click
from .analyze import analyze
from .config import Config

@click.group()
def cli():
    """AgentOps CLI: Manage your testing and code confidence workflow."""
    pass

@cli.command()
def init():
    """Initialize an AgentOps project."""
    Config().initialize()

@cli.command()
def generate_tests():
    """Generate tests for your codebase."""
    click.echo("[AgentOps] Test generation started (stub)")

@cli.command()
def run_tests():
    """Run tests and show coverage."""
    click.echo("[AgentOps] Running tests and showing coverage (stub)")

cli.add_command(analyze)

if __name__ == "__main__":
    cli() 