from abc import ABC, abstractmethod

from src.repositories.file_repository import IFileRepository


class IFileService(ABC):
    """
    Abstract class for a file service containing the required
    methods and their signatures.

    If required this class can be extended to support a custom
    implementation of the file service.
    """

    @abstractmethod
    def store_file(self, file_path: str, file_id: str):
        pass

    @abstractmethod
    def store_files(self, files: list):
        pass

    @abstractmethod
    def load_file(self, file_id: str):
        pass

    @abstractmethod
    def load_files(self, ids: list):
        pass

    @abstractmethod
    def destroy_file(self, file_id: str):
        pass

    @abstractmethod
    def destroy_files(self, ids: str):
        pass


class FileService(IFileService):
    """
    Service class that handles the business logic between the
    file repository and the file use cases.

    Provides methods that can be used to store/load/destroy one
    or multiple files at once.
    """

    def __init__(self, file_repository: IFileRepository):
        """
        Initialize the file service by specifying the file repository
        from the dependency container.

        :param file_repository: File repository
        """

        self.file_repository = file_repository

    def store_file(self, file_path: str, file_id: str):
        """
        Store a single file inside the storage by providing a file
        path and a file id.

        :param file_path: File path
        :param file_id: File identity
        """

        self.file_repository.store_file(file_path, file_id)

    def store_files(self, files: list):
        """
        Store multiple files inside the storage by providing a list of
        dictionary objects containing a file path and a file id.

        :param files: List of dicts containing a file path and a file id
        """

        for file in files:
            self.file_repository.store_file(file['path'], file['id'])

    def load_file(self, file_id: str):
        """
        Load a single file inside the output directory by providing
        a file id stored in the id storage.

        :param file_id: File identity
        """

        self.file_repository.load_file(file_id)

    def load_files(self, ids: list):
        """
        Load multiple files inside the output directory by providing a list
        of file ids stored in the id storage.

        :param ids: List of file ids
        """

        for file_id in ids:
            self.file_repository.load_file(file_id)

    def destroy_file(self, file_id: str):
        """
        Destroy a single file from the storage by providing
        a file id stored in the id storage.

        :param file_id: File identity
        """

        self.file_repository.destroy_file(file_id)

    def destroy_files(self, ids: list):
        """
        Destroy multiple files from the storage by providing a list
        of file ids stored in the id storage.

        :param ids: List of file ids
        """

        for file_id in ids:
            self.file_repository.destroy_file(file_id)
