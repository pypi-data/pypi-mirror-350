from typing import Final, ClassVar

import json
import subprocess
import sys
from datetime import datetime
from importlib.metadata import distributions
from importlib.resources import files
from pathlib import Path

from git import Repo
from pydantic import BaseModel

from .exc import (
    PluginAlreadyInstalledException,
    PluginDoesNotExistException,
    PluginNotInstalledException,
    PluginTemplateCloneDirectoryIsNotEmpty,
    PluginTemplateClonePathIsNotDirectory,
)


class PluginMetadata(BaseModel):
    name: str
    pypi_package: str
    date_added: datetime
    official: bool
    description: str
    url: str
    tool_url: str
    license: str


class PackageManager(BaseModel):
    @classmethod
    def _run_pip(cls, subcommand, *args):
        command = [sys.executable, "-m", "pip", subcommand, *args, "--quiet"]
        subprocess.check_call(command)

    @classmethod
    def install_package(cls, *package_names) -> None:
        cls._run_pip("install", *package_names)

    @classmethod
    def uninstall_package(cls, *package_names) -> None:
        cls._run_pip("uninstall", *package_names, "--yes")

    @classmethod
    def list_installed_packages(cls) -> list[str]:
        installed_packages = []
        for package in distributions():
            installed_packages.append(package.metadata["Name"])
        return installed_packages


class PluginManager(BaseModel):
    available_plugin_index: dict[str, PluginMetadata] = {}
    installed_plugin_index: dict[str, PluginMetadata] = {}

    def __init__(self, **data) -> None:
        super().__init__(**data)
        self.load_plugins_metadata()

    def load_plugins_metadata(self):
        package_dir = str(files("parsomics_cli"))
        plugins_json = (
            Path(package_dir) / Path("parsomics-registry") / Path("plugins.json")
        )
        with open(plugins_json, "r") as file:
            data = json.load(file)
            for d in data["plugins"]:
                plugin_metadata = PluginMetadata.model_validate(d)
                self.available_plugin_index[plugin_metadata.name] = plugin_metadata

    def is_plugin_installed(self, plugin_name: str):
        installed_packages = PackageManager.list_installed_packages()
        plugin_metadata = self.available_plugin_index[plugin_name]

        # Check if the plugin package is installed
        plugin_installed = False
        if plugin_metadata.pypi_package in installed_packages:
            plugin_installed = True

        return plugin_installed

    def list_plugins(self):
        installed_plugins = []
        for plugin_name in self.available_plugin_index:
            if self.is_plugin_installed(plugin_name):
                installed_plugins.append(
                    {
                        "name": plugin_name,
                        "installed": True,
                    }
                )
            else:
                installed_plugins.append(
                    {
                        "name": plugin_name,
                        "installed": False,
                    }
                )
        return installed_plugins

    def check_plugin_installable(self, plugin_name: str):
        # Raise exception if plugin does not exist
        if not plugin_name in self.available_plugin_index:
            raise PluginDoesNotExistException(plugin_name)

        # Raise exception if the plugin is already installed
        if self.is_plugin_installed(plugin_name):
            raise PluginAlreadyInstalledException(plugin_name)

    def install_plugin(self, plugin_name: str):
        # Raise exception if the plugin is not installable
        self.check_plugin_installable(plugin_name)

        plugin_metadata: PluginMetadata = self.available_plugin_index[plugin_name]
        PackageManager.install_package(plugin_metadata.pypi_package)

    def check_plugin_uninstallable(self, plugin_name: str):
        # Raise exception if plugin does not exist
        if not plugin_name in self.available_plugin_index:
            raise PluginDoesNotExistException(plugin_name)

        # Raise exception if the plugin is not installed
        if not self.is_plugin_installed(plugin_name):
            raise PluginNotInstalledException(plugin_name)

    def uninstall_plugin(self, plugin_name: str):
        # Raise exception if the plugin is not uninstallable
        self.check_plugin_uninstallable(plugin_name)

        plugin_metadata: PluginMetadata = self.available_plugin_index[plugin_name]
        PackageManager.uninstall_package(plugin_metadata.pypi_package)


class PluginMaker(BaseModel):
    TOOL_NAME_CANONICAL_PLACEHOLDER: ClassVar[str] = "<Tool Name>"
    TOOL_NAME_PASCAL_CASE_PLACEHOLDER: ClassVar[str] = "<ToolName>"
    TOOL_NAME_KEBAB_CASE_PLACEHOLDER: ClassVar[str] = "<tool-name>"
    TOOL_NAME_SNAKE_CASE_PLACEHOLDER: ClassVar[str] = "<tool_name>"

    REPO_URL: ClassVar[str] = (
        "https://gitlab.com/parsomics/parsomics-plugin-template.git"
    )

    @classmethod
    def _to_pascal_case(cls, string: str) -> str:
        words = [word.title() for word in string.lower().split()]
        return "".join(words)

    @classmethod
    def _to_kebab_case(cls, string: str) -> str:
        words = string.lower().split()
        return "-".join(words)

    @classmethod
    def _to_snake_case(cls, string: str) -> str:
        words = string.lower().split()
        return "_".join(words)

    @classmethod
    def _replace_in_file(cls, file_path: Path, replace: dict) -> None:
        if file_path.is_file():
            content = file_path.read_text(encoding="utf-8")

            # Replace strings
            for old_string, new_string in replace.items():
                content = content.replace(old_string, new_string)

            file_path.write_text(content, encoding="utf-8")

    @classmethod
    def _replace_in_directory(cls, directory_path: Path, replace) -> None:
        for file_path in directory_path.iterdir():
            cls._replace_in_file(file_path, replace)

    @classmethod
    def _create_replace_dict(cls, name_canonical: str) -> dict:
        name_pascal_case = cls._to_pascal_case(name_canonical)
        name_kebab_case = cls._to_kebab_case(name_canonical)
        name_snake_case = cls._to_snake_case(name_canonical)

        replace = {
            cls.TOOL_NAME_CANONICAL_PLACEHOLDER: name_canonical,
            cls.TOOL_NAME_PASCAL_CASE_PLACEHOLDER: name_pascal_case,
            cls.TOOL_NAME_KEBAB_CASE_PLACEHOLDER: name_kebab_case,
            cls.TOOL_NAME_SNAKE_CASE_PLACEHOLDER: name_snake_case,
        }
        return replace

    @classmethod
    def _replace_placeholders(cls, name_canonical: str, template_path: Path):
        replace = cls._create_replace_dict(name_canonical)

        python_module_path = template_path / Path("parsomics_plugin_template")
        cls._replace_in_directory(python_module_path, replace)

        readme_file_path = template_path / Path("README.md")
        cls._replace_in_file(readme_file_path, replace)

        # Rename source directory
        python_module_path_new = template_path / Path(
            f"parsomics_plugin_{cls._to_snake_case(name_canonical)}"
        )
        python_module_path.rename(python_module_path_new)

    @classmethod
    def _clone_template_repository(cls, directory_path: Path):
        if directory_path.exists():
            if not directory_path.is_dir():
                raise PluginTemplateClonePathIsNotDirectory(directory_path)
            if any(directory_path.iterdir()):
                raise PluginTemplateCloneDirectoryIsNotEmpty(directory_path)
        else:
            directory_path.mkdir(parents=True)

        # Clone the repository
        Repo.clone_from(PluginMaker.REPO_URL, directory_path)

    @classmethod
    def make_plugin(cls, name_canonical: str, directory_path: Path):
        # Name the cloning directory uniquely
        name_kebab_case = cls._to_kebab_case(name_canonical)
        clone_path = directory_path / Path(f"parsomics-plugin-{name_kebab_case}")

        # Clone the template repository
        cls._clone_template_repository(clone_path)

        # Make necessary replacements
        cls._replace_placeholders(name_canonical, clone_path)
