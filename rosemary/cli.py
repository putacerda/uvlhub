import click
from rosemary.commands.update import update
from rosemary.commands.info import info
from rosemary.commands.make_module import make_module
from rosemary.commands.env import env
from rosemary.commands.test import test


class RosemaryCLI(click.Group):
    def get_command(self, ctx, cmd_name):
        rv = super().get_command(ctx, cmd_name)
        if rv is not None:
            return rv
        click.echo(f"No such command '{cmd_name}'.")
        click.echo("Try 'rosemary --help' for a list of available commands.")
        return None


@click.group(cls=RosemaryCLI)
def cli():
    """A CLI tool to help with project management."""
    pass


cli.add_command(update)
cli.add_command(info)
cli.add_command(make_module)
cli.add_command(env)
cli.add_command(test)

if __name__ == '__main__':
    cli()
