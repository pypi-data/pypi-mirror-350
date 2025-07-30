import click
from click import secho
from adxp_cli.agent.cli import agent
from adxp_cli.auth.cli import auth


@click.group()
def cli():
    """Command-line interface for AIP server management."""
    pass


cli.add_command(auth)
cli.add_command(agent)


if __name__ == "__main__":
    cli()
