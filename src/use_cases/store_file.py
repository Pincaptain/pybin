from src.services.file_service import IFileService


class StoreFile(object):
    """
    Use case scenario class for storing files in the storage.

    Contains use cases for storing one or multiple files
    into the storage.
    """

    def __init__(self, file_service: IFileService):
        """
        Initialize the use case by obtaining an instance of file service
        using the dependency container.

        :param file_service: File service
        """

        self.file_service = file_service

    def store_file(self, file_path: str, file_id: str):
        """
        Store a single file inside the storage.

        :param file_path: File path
        :param file_id: File identity
        """

        self.file_service.store_file(file_path, file_id)

    def store_files(self, files: list):
        """
        Store multiple files inside the storage.

        :param files: List of dicts containing a file path and a file id
        """

        self.file_service.store_files(files)
