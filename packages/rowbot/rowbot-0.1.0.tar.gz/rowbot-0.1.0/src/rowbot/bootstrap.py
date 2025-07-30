from dependency_injector import containers, providers

from rowbot.configs.data import settings
from rowbot.controllers.menu import Menu
from rowbot.services.commands import Commands
from rowbot.services.storage import JSONStorage


class Container(containers.DeclarativeContainer):
    """
    Rowbot's dependency injection container, centralizing its configuration and
    instantiating components, ensuring modularity and facilitating testing.
    """

    storage = providers.Singleton(
        JSONStorage,
        file=providers.Callable(lambda: settings.ROWBOT_FILE),
    )

    commands = providers.Factory(
        Commands,
        storage=storage,
    )

    menu = providers.Factory(
        Menu,
        commands=commands,
    )
