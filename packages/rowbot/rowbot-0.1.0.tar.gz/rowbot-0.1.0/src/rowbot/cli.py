import io
import sys

import click

from rowbot import __version__
from rowbot.bootstrap import Container

# Configuring stdout/stderr for Windows Operative Systems:
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8")


@click.command()
@click.option("-m", "--menu", is_flag=True, help="Open the interactive menu.")
@click.version_option(version=__version__, message="Rowbot 🤖, v%(version)s")
def rowbot(menu: bool) -> None:
    """
    🤖 Rowbot - An interactive command manager for your terminal.

    Manage and execute frequently used commands through an interactive interface
    (allowing searching and navigation), displaying all your commands and their
    descriptions, stored within a `~/.rowbot/commands.json` file.

    Basic usage:

    \b
        rowbot              Display interactive commands table
        rowbot -m/--menu    Manage commands (add/remove/edit)
    """
    if menu:
        container = Container()
        menu_handler = container.menu()
        menu_handler.display()

        return

    # TODO: Add custom logic for the "rowbot" command, to manage the interactive
    # command"s table.
    click.echo("Rowbot: Command-line assistant for commands management.")
    click.echo("Basic functionality coming soon! Use --help for more info.")
