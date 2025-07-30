import click

from .alias import alias
from .plugin import plugin


@click.group()
def cli():
    pass


cli.add_command(plugin)
cli.add_command(alias)
