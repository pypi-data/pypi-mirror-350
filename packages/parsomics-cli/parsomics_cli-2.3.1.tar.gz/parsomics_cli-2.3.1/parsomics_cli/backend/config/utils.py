import os
import subprocess
from pathlib import Path

from parsomics_core.configuration import (
    SYSTEM_DEFAULT_CONFIG_FILE_PATH,
    USER_DEFAULT_CONFIG_FILE_PATH,
)
from pydantic import BaseModel
from pygments import highlight
from pygments.formatters import TerminalFormatter
from pygments.lexers import TOMLLexer

from rich.console import Console
from rich.rule import Rule

from parsomics_cli.backend.config.exc import (
    ConfigurationCannotBeLocated,
    ConfigurationFileNotTOML,
    ConfigurationPathAlreadyExists,
    ConfigurationPathDoesNotExist,
)
from parsomics_cli.backend.config.types import Scope

console = Console()


class ConfigurationManager(BaseModel):
    system_config: Path = SYSTEM_DEFAULT_CONFIG_FILE_PATH
    user_config: Path = USER_DEFAULT_CONFIG_FILE_PATH

    def check_file_readable(self, scope: Scope, path: Path):
        if not path.is_file():
            raise ConfigurationPathDoesNotExist(scope, path)
        if not path.suffix == ".toml":
            raise ConfigurationFileNotTOML(scope, path)

    def check_file_editable(self, scope: Scope, path: Path):
        self.check_file_readable(scope, path)

    def check_file_viewable(self, scope: Scope, path: Path):
        self.check_file_readable(scope, path)

    def check_file_creatable(self, scope: Scope, path: Path):
        if not path.suffix == ".toml":
            raise ConfigurationFileNotTOML(scope, path)
        if path.is_file():
            raise ConfigurationPathAlreadyExists(scope, path)

    def _edit_file(self, scope: Scope, path: Path):
        self.check_file_editable(scope, path)
        editor = os.getenv("EDITOR", "vi")
        subprocess.run([editor, path])

    def edit_user_config(self):
        path: Path = self.user_config
        scope: Scope = Scope.USER
        self._edit_file(scope, path)

    def edit_system_config(self):
        path: Path = self.system_config
        scope: Scope = Scope.SYSTEM
        self._edit_file(scope, path)

    def edit_custom_config(self, path: Path):
        scope: Scope = Scope.CUSTOM
        self._edit_file(scope, path)

    def _create_config(self, scope: Scope, path: Path):
        # If the path is a directory
        if path.is_dir() or path.suffix == "":
            path = path / Path("config.toml")

        self.check_file_creatable(scope, path)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.touch()

    def create_user_config(self):
        scope: Scope = Scope.USER
        path: Path = USER_DEFAULT_CONFIG_FILE_PATH
        self._create_config(scope, path)

    def create_system_config(self):
        scope: Scope = Scope.SYSTEM
        path: Path = SYSTEM_DEFAULT_CONFIG_FILE_PATH
        self._create_config(scope, path)

    def create_custom_config(self, path):
        scope: Scope = Scope.CUSTOM
        self._create_config(scope, path)

    def _view_config(self, scope: Scope, path: Path):
        self.check_file_viewable(scope, path)
        content = path.read_text()

        rule = Rule(f"{path} (scope={scope.value})")
        console.print(rule)
        print(highlight(content, TOMLLexer(), TerminalFormatter()))
        rule = Rule()
        console.print(rule)

    def view_user_config(self):
        scope: Scope = Scope.USER
        path = self.user_config
        self._view_config(scope, path)

    def view_system_config(self):
        scope: Scope = Scope.SYSTEM
        path = self.system_config
        self._view_config(scope, path)

    def view_custom_config(self, path: Path):
        scope: Scope = Scope.CUSTOM
        self._view_config(scope, path)

    def locate_config(self, scope: Scope):
        match scope:
            case Scope.USER:
                return self.user_config
            case Scope.SYSTEM:
                return self.system_config
            case Scope.CUSTOM:
                raise ConfigurationCannotBeLocated
