from src.services.file_service import IFileService


class DestroyFile(object):
    """
    Use case scenario class for destroying files in the storage.

    Contains methods for destroying one or multiple files
    from the storage.
    """

    def __init__(self, file_service: IFileService):
        """
        Initialize the use case by obtaining an instance of file service
        using the dependency container.

        :param file_service: File service
        """

        self.file_service = file_service

    def destroy_file(self, file_id: str):
        """
        Destroy a single file from the storage.

        :param file_id: File identity
        """

        self.file_service.destroy_file(file_id)

    def destroy_files(self, ids: list):
        """
        Destroy multiple files from the storage.

        :param ids: List of file ids
        """

        self.file_service.destroy_files(ids)
