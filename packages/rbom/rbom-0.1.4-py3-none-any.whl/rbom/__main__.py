import click

from . import commands

@click.group()
def xcli():
    pass

xcli.add_command(commands.welcome)
xcli.add_command(commands.load)
xcli.add_command(commands.set_attribute)
xcli.add_command(commands.sign)
