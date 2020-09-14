import os
import json
from abc import ABC, abstractmethod


class IFileRepository(ABC):
    """
    Abstract class for a file repository containing the required
    methods and their signatures.

    This class is the bread and butter of the whole program and
    as a result of that coding a custom implementation might
    cause some serious pain and suffering.
    """

    @abstractmethod
    def store_file(self, file_path: str, file_id: str):
        pass

    @abstractmethod
    def load_file(self, file_id: str):
        pass

    @abstractmethod
    def destroy_file(self, file_id: str):
        pass


class FileRepository(IFileRepository):
    """
    File repository class used to store, load and destroy files from
    and to the storage.

    Initialize it by providing the directory of the storage.bin and
    storage.json files and additionally the output directory.
    """

    def __init__(self, storage_dir_path: str, output_dir_path: str):
        """
        Initialize the file repository by specifying the storage path
        and the output path.

        :param storage_dir_path: Storage directory path
        :param output_dir_path: Output directory path
        """

        self.storage_path = f'{storage_dir_path}.bin'
        self.id_storage_path = f'{storage_dir_path}.json'
        self.output_dir_path = output_dir_path

    def store_file(self, file_path: str, file_id: str):
        """
        Store the file by appending the file bytes to the end of the storage file
        and update the id storage with the position, size, name and extension of the new file.

        :param file_path: File path
        :param file_id: File identity
        """

        if not os.path.exists(file_path):
            raise FileNotFoundException(file_path)

        with open(file_path, 'rb') as r_file:
            file_size = os.path.getsize(file_path)
            file_name = os.path.basename(file_path)
            file_extension = os.path.splitext(file_path)[1]

            with open(self.storage_path, 'r+b') as w_file:
                w_file.seek(0, os.SEEK_END)

                file_position = w_file.tell()
                self.__store_id(file_id, file_position, file_size, file_name, file_extension)

                for file_bytes in r_file:
                    w_file.write(file_bytes)

    def __store_id(self, file_id: str, file_position: int, file_size: int, file_name: str, file_extension: str):
        """
        Store the file id and stats by loading the json id storage file,
        appending the key value pair and saving the file once the process
        is done.

        For an example of this key-value pair you can check the storage.json
        file though playing around with it is strictly forbidden if
        you have no idea what it does for it may cause errors and data loss.

        :param file_id: File identity
        :param file_position: File storage position
        :param file_size: File size
        :param file_name: File name and extension
        :param file_extension: File extension
        """

        with open(self.id_storage_path, 'r') as r_file:
            content = r_file.read()

            if len(content) == 0:
                ids = {}
            else:
                ids = json.loads(content)

            if file_id in ids:
                raise IdentityAlreadyExistsException(file_id)

            ids[file_id] = {
                'position': file_position,
                'size': file_size,
                'name': file_name,
                'extension': file_extension,
            }

        with open(self.id_storage_path, 'w') as w_file:
            w_file.write(json.dumps(ids))

    def load_file(self, file_id: str):
        """
        Load the file from the storage using the provided file_id and save
        it to the output directory using the file stats dictionary.

        Buffered writing is used to prevent memory issues with files too large
        to be stored in memory.

        :param file_id: File identity
        """

        file_stats = self.__load_id(file_id)
        file_name = file_stats['name']
        file_position = file_stats['position']
        file_path = f'{self.output_dir_path}\\{file_name}'

        with open(self.storage_path, 'r+b') as r_file:
            r_file.seek(file_position, os.SEEK_SET)

            buffer_size = 65536
            file_size = file_stats['size']

            with open(file_path, 'wb') as w_file:
                while file_size != 0:
                    if buffer_size > file_size:
                        w_file.write(r_file.read(file_size))
                        file_size -= file_size
                    else:
                        w_file.write(r_file.read(buffer_size))
                        file_size -= buffer_size

    def __load_id(self, file_id: str):
        """
        Load the id storage and look for the specified file stats.
        If they exists return them otherwise a raise an error.

        :param file_id: File identity
        :return: Dict of the file stats
        """

        with open(self.id_storage_path, 'r') as r_file:
            content = r_file.read()

            if len(content) == 0:
                raise IdentityNotStoredException(file_id)

            ids = json.loads(content)

            if file_id in ids:
                return ids[file_id]
            else:
                raise IdentityNotStoredException(file_id)

    def destroy_file(self, file_id: str):
        """
        Destroy the file from the storage by replacing all of its bytes to null bytes and
        finalize the process by deleting its id from the id storage.

        :param file_id: File identity
        """

        file_stats = self.__load_id(file_id)
        file_position = file_stats['position']
        file_size = file_stats['size']
        buffer_size = 65536

        with open(self.storage_path, 'r+b') as w_file:
            w_file.seek(file_position, os.SEEK_SET)

            while file_size != 0:
                if buffer_size > file_size:
                    w_file.write(bytearray(file_size))
                    file_size -= file_size
                else:
                    w_file.write(bytearray(buffer_size))
                    file_size -= buffer_size

        self.__destroy_id(file_id)

    def __destroy_id(self, file_id: str):
        """
        Remove the file id from the id storage if it exists.

        :param file_id: File identity
        :return: Boolean based on the success of the operation
        """

        with open(self.id_storage_path, 'r') as r_file:
            content = r_file.read()

            if len(content) == 0:
                return False

            ids = json.loads(content)

            if ids.pop(file_id, None) is None:
                return False

        with open(self.id_storage_path, 'w') as w_file:
            w_file.write(json.dumps(ids))

        return True


class FileNotFoundException(Exception):
    """
    Exception class that raises an exception when the file provided
    is invalid or cannot be found.
    """

    def __init__(self, file_path: str):
        """
        Initialize the exception class by storing the path of the file
        that does not exist or is invalid.

        :param file_path: Unknown file path
        """
        self.file_path = file_path

    def __str__(self):
        return f'File {self.file_path} not found'


class IdentityAlreadyExistsException(Exception):
    """
    Exception class that raises an exception when the program tries to
    store an id that already exists inside the id storage.
    """

    def __init__(self, file_id: str):
        """
        Initialize the exception class by storing the id that already exists
        in the id storage.

        :param file_id: File identity
        """

        self.file_id = file_id

    def __str__(self):
        return f'Id "{self.file_id}" already exists'


class IdentityNotStoredException(Exception):
    """
    Exception class that raises an exception when the id provided does not
    exist inside the id storage.
    """

    def __init__(self, file_id: str):
        """
        Initialize the exception class by storing the id that was not
        yet stored.

        :param file_id: File identity
        """
        self.file_id = file_id

    def __str__(self):
        return f'Id {self.file_id} not stored'


class DirectoryNotSpecifiedException(Exception):
    """
    Exception class that raises an exception when the directory provided
    is either not a directory or does not exist.
    """

    def __init__(self, file_path: str):
        """
        Initialize the exception class by storing the invalid directory
        path provided.

        :param file_path: Invalid directory path
        """
        self.file_path = file_path

    def __str__(self):
        return f'File {self.file_path} is not a directory'
