from pathlib import Path

from parsomics_cli.backend.config.types import Scope


class ConfigurationManagerException(Exception):
    pass


class ConfigurationPathAlreadyExists(ConfigurationManagerException):
    def __init__(self, scope: Scope, path: Path):
        message = f"{scope.value} configuration file at {path} already exists"
        super().__init__(message)


class ConfigurationPathDoesNotExist(ConfigurationManagerException):
    def __init__(self, scope: Scope, path: Path):
        message = f"{scope.value} configuration file at {path} does not exist"
        super().__init__(message)


class ConfigurationFileNotTOML(ConfigurationManagerException):
    def __init__(self, scope: Scope, path: Path):
        message = f"{scope.value} configuration file at {path} is not TOML"
        super().__init__(message)


class ConfigurationCannotBeLocated(ConfigurationManagerException):
    def __init__(self):
        message = f"{Scope.CUSTOM.value} configuration cannot be automatically located"
        super().__init__(message)
