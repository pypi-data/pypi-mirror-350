import click
from click import secho
from adxp_cli.agent_cli import agent


@click.group()
def cli():
    """Command-line interface for AIP server management."""
    pass


cli.add_command(agent)


if __name__ == "__main__":
    cli()
