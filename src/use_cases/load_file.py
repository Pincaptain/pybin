from src.services.file_service import IFileService


class LoadFile(object):
    """
    Use case scenario class for loading files from the storage.

    Contains methods for loading one or multiple files
    from the storage.
    """

    def __init__(self, file_service: IFileService):
        """
        Initialize the use case by obtaining an instance of file service
        using the dependency container.

        :param file_service: File service
        """

        self.file_service = file_service

    def load_file(self, file_id: str):
        """
        Load a single file inside the output directory.

        :param file_id: File identity
        """

        self.file_service.load_file(file_id)

    def load_files(self, ids: list):
        """
        Load multiple files inside the output directory.

        :param ids: List of file ids
        """

        self.file_service.load_files(ids)
