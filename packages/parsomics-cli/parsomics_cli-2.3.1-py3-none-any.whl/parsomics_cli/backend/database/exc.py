class ContainerManagerException(Exception):
    pass


class ContainerEngineNotInstalled(ContainerManagerException):
    def __init__(self):
        message = f"podman is not installed. Follow installation instructions at https://podman.io/docs/installation#installing-on-linux"
        super().__init__(message)


class ContainerEngineSocketNotAvailable(ContainerManagerException):
    def __init__(self):
        message = f"podman socket is not available"
        super().__init__(message)


class ContainerProcessNotYours(ContainerManagerException):
    def __init__(self):
        message = f"cannot stop a container process that was started by another user"
        super().__init__(message)


class ContainerAlreadyExists(ContainerManagerException):
    def __init__(self, container_name: str):
        message = f'database container "{container_name}" already exists'
        super().__init__(message)


class ContainerDoesNotExist(ContainerManagerException):
    def __init__(self, container_name: str):
        message = f'database container "{container_name}" does not exist'
        super().__init__(message)


class ContainerIsNotRunning(ContainerManagerException):
    def __init__(self, container_name: str):
        message = f'database container "{container_name}" is not running'
        super().__init__(message)


class ContainerIsRunning(ContainerManagerException):
    def __init__(self, container_name: str):
        message = f'database container "{container_name}" is running'
        super().__init__(message)
