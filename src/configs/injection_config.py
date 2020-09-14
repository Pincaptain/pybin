from dependency_injector import containers, providers

from src.repositories.file_repository import FileRepository
from src.services.file_service import FileService


class Container(containers.DeclarativeContainer):
    """
    Declarative container containing the instances of the
    singletons and their configuration.
    """

    config = providers.Configuration()
    file_repository = providers.Singleton(
        FileRepository,
        storage_dir_path=config.general.storage_dir_path,
        output_dir_path=config.general.output_dir_path)
    file_service = providers.Singleton(
        FileService,
        file_repository=file_repository)


class InjectionConfig(object):
    """
    Config class that initializes the container and uses the provided
    configurations to initialize the singletons.
    """

    def __init__(self, config_path: str):
        """
        Initialize the container and setup its configuration
        using the provided configuration file.

        :param config_path: Configuration file path
        """

        self.container = Container()
        self.container.config.from_ini(config_path)

    def get_file_repository(self) -> FileRepository:
        """
        Return the file repository singleton.

        :return: File repository singleton
        """

        return self.container.file_repository()

    def get_file_service(self) -> FileService:
        """
        Return the file service singleton.

        :return: File service singleton.
        """

        return self.container.file_service()
