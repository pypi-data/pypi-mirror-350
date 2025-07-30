from collections.abc import Callable
from importlib import import_module

from cleo.application import Application
from cleo.commands.command import Command
from cleo.exceptions import CleoLogicError
from cleo.loaders.factory_command_loader import FactoryCommandLoader

from expanse_cli import __version__


def load_command(name: str) -> Callable[[], Command]:
    def _load() -> Command:
        words = name.split(" ")
        module = import_module("expanse_cli.commands." + ".".join(words))
        command_class = getattr(module, "".join(c.title() for c in words) + "Command")
        command: Command = command_class()
        return command

    return _load


COMMANDS: list[str] = [
    "new",
]


class CommandLoader(FactoryCommandLoader):
    def register_factory(
        self, command_name: str, factory: Callable[[], Command]
    ) -> None:
        if command_name in self._factories:
            raise CleoLogicError(f'The command "{command_name}" already exists.')

        self._factories[command_name] = factory


app = Application("Expanse", __version__)
app.set_command_loader(CommandLoader({name: load_command(name) for name in COMMANDS}))


def run() -> int:
    return app.run()
