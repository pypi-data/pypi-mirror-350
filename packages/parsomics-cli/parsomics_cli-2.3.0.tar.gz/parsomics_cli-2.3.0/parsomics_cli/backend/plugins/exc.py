from pathlib import Path


class PluginManagerException(Exception):
    pass


class PluginDoesNotExistException(PluginManagerException):
    def __init__(self, plugin_name: str):
        message = f'plugin "{plugin_name}" does not exist'
        super().__init__(message)


class PluginAlreadyInstalledException(PluginManagerException):
    def __init__(self, plugin_name: str):
        message = f'plugin "{plugin_name}" is already installed'
        super().__init__(message)


class PluginNotInstalledException(PluginManagerException):
    def __init__(self, plugin_name: str):
        message = f"plugin {plugin_name} is not installed"
        super().__init__(message)


class PluginMakerException(Exception):
    pass


class PluginTemplateClonePathIsNotDirectory(PluginMakerException):
    def __init__(self, directory_path: Path):
        message = f'the path "{directory_path}" exists but is not a directory'
        super().__init__(message)


class PluginTemplateCloneDirectoryIsNotEmpty(PluginMakerException):
    def __init__(self, directory_path: Path):
        message = f'the directory "{directory_path}" exists but is not a directory'
        super().__init__(message)
