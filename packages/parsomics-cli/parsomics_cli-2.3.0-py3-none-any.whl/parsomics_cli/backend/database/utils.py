import os
import shutil
import psutil

import keyring
from parsomics_core.globals.database import DATABASE_NAME, USERNAME
from podman import PodmanClient
from podman.errors.exceptions import APIError, NotFound
from pydantic import BaseModel

from parsomics_cli.backend.database.exc import (
    ContainerAlreadyExists,
    ContainerDoesNotExist,
    ContainerEngineNotInstalled,
    ContainerEngineSocketNotAvailable,
    ContainerIsNotRunning,
    ContainerIsRunning,
    ContainerProcessNotYours,
)
from parsomics_cli.backend.database.types import DatabaseStatus

CONTAINER_NAME = "parsomics-postgres"
POSTGRES_IMAGE_NAME = "postgres"
POSTGRES_IMAGE_TAG = "latest"
POSTGRES_IMAGE_URI = f"docker.io/library/{POSTGRES_IMAGE_NAME}:{POSTGRES_IMAGE_TAG}"


class ContainerManager(BaseModel):
    def check_container_exists(self) -> None:
        with PodmanClient() as client:
            try:
                client.containers.get(CONTAINER_NAME)
            except NotFound:
                raise ContainerDoesNotExist(CONTAINER_NAME)

    def check_container_does_not_exist(self) -> None:
        with PodmanClient() as client:
            try:
                client.containers.get(CONTAINER_NAME)
                raise ContainerAlreadyExists(CONTAINER_NAME)
            except NotFound:
                pass

    def _is_database_connected(self) -> bool:
        DATABASE_PORT = 5432
        database_connections: list[bool] = [
            # NOTE: pyright doesn't seem to support namedtuples (like
            #       conn.laddr), so ignore typing in the next line
            conn.laddr.port == DATABASE_PORT and conn.status == psutil.CONN_LISTEN  # type: ignore
            for conn in psutil.net_connections(kind="inet")
        ]
        return any(database_connections)

    def check_container_is_running(self) -> None:
        with PodmanClient() as client:
            container = client.containers.get(CONTAINER_NAME)
            if container.status != "running" and not self._is_database_connected():
                raise ContainerIsNotRunning(CONTAINER_NAME)
            if container.status != "running" and self._is_database_connected():
                raise ContainerProcessNotYours()

    def check_container_is_not_running(self) -> None:
        with PodmanClient() as client:
            container = client.containers.get(CONTAINER_NAME)
            if container.status == "running" or self._is_database_connected():
                raise ContainerIsRunning(CONTAINER_NAME)

    def check_podman_executable(self) -> None:
        if not shutil.which("podman"):
            raise ContainerEngineNotInstalled()
        pass

    def check_podman_socket(self) -> None:
        with PodmanClient() as client:
            try:
                client.ping()
            except APIError:
                raise ContainerEngineSocketNotAvailable()

    def check_status_retrievable(self) -> None:
        self.check_podman_executable()
        self.check_podman_socket()

    def get_status(self) -> DatabaseStatus:
        result = DatabaseStatus.UNKNOWN
        with PodmanClient() as client:
            try:
                container = client.containers.get(CONTAINER_NAME)
                status = container.status
                if status == "running" or self._is_database_connected():
                    result = DatabaseStatus.RUNNING
                else:
                    result = DatabaseStatus.NOT_RUNNING
            except NotFound:
                result = DatabaseStatus.NOT_CREATED
        return result

    def check_container_creatable(self) -> None:
        self.check_podman_executable()
        self.check_podman_socket()
        self.check_container_does_not_exist()

    def create_container(self):
        self.check_container_creatable()
        with PodmanClient() as client:
            # Pull an image
            client.images.pull(POSTGRES_IMAGE_URI)

            # Get password
            password = keyring.get_password(DATABASE_NAME, USERNAME)

            # Create and start parsomics container
            client.containers.create(
                f"{POSTGRES_IMAGE_NAME}:{POSTGRES_IMAGE_TAG}",
                name=CONTAINER_NAME,
                environment={
                    "POSTGRES_DB": DATABASE_NAME,
                    "POSTGRES_USER": USERNAME,
                    "POSTGRES_PASSWORD": password,
                },
                ports={"5432/tcp": "5432"},
            )

    def check_container_deletable(self) -> None:
        self.check_podman_executable()
        self.check_podman_socket()
        self.check_container_exists()
        self.check_container_is_not_running()

    def delete_container(self):
        self.check_container_deletable()
        with PodmanClient() as client:
            container = client.containers.get(CONTAINER_NAME)
            container.remove()

    def check_container_startable(self) -> None:
        self.check_podman_executable()
        self.check_podman_socket()
        self.check_container_exists()
        self.check_container_is_not_running()

    def start_container(self):
        self.check_container_startable()
        with PodmanClient() as client:
            container = client.containers.get(CONTAINER_NAME)
            container.start()

    def check_container_stoppable(self) -> None:
        self.check_podman_executable()
        self.check_podman_socket()
        self.check_container_exists()
        self.check_container_is_running()

    def stop_container(self):
        self.check_container_stoppable()
        with PodmanClient() as client:
            container = client.containers.get(CONTAINER_NAME)
            container.stop()

    def set_password(self, password: str):
        keyring.set_password(DATABASE_NAME, USERNAME, password)

    def get_password(self) -> str | None:
        return keyring.get_password(DATABASE_NAME, USERNAME)
