import os
import json


# Repository class used to handle
# file storing, loading and destroying
class FileRepository(object):
    # Initialize the file repository by specifying the
    # storage path and the output path
    def __init__(self, storage: str, output: str):
        self.storage = f'{storage}.bin'
        self.id_storage = f'{storage}.json'
        self.output = output

    # noinspection PyShadowingBuiltins
    def store_file(self, path: str, id: str):
        # Check if the file exists
        if not os.path.exists(path):
            raise FileNotFoundException(path)

        # Open the file for reading
        with open(path, 'rb') as r_file:
            # Get the file stats
            file_size = os.path.getsize(path)
            file_extension = os.path.splitext(path)[1]
            file_name = os.path.basename(path)

            # Position the cursor at the end of the file
            # Store the file stats (id, position, size, name and extension)
            with open(self.storage, 'r+b') as w_file:
                w_file.seek(0, os.SEEK_END)
                self.__store_id(id, w_file.tell(), file_size, file_name, file_extension)

                # Begin reading the file line by line
                # To evade memory errors
                for bytes in r_file:
                    w_file.write(bytes)

    # noinspection PyShadowingBuiltins
    def __store_id(self, id: str, position: int, size: int, name: str, extension: str):
        # Open the id_storage file for reading
        with open(self.id_storage, 'r') as r_file:
            # Read the content of the file
            content = r_file.read()

            # Initialize the ids based on the contents
            # of the file (if empty new dictionary else load the existing one)
            if len(content) == 0:
                ids = {}
            else:
                ids = json.loads(content)

            # Check if the id provided already exists in the storage
            # If it does raise an exception
            if id in ids:
                raise IdentityAlreadyExistsException(id)

            # Store the new id in the dictionary
            # along with its stats
            ids[id] = {
                'position': position,
                'size': size,
                'name': name,
                'extension': extension,
            }

        # Store the new dictionary to a file
        with open(self.id_storage, 'w') as w_file:
            w_file.write(json.dumps(ids))

    # noinspection PyShadowingBuiltins
    def load_file(self, id: str):
        # Load the stats of the file
        # and deduce the filename and extension
        # based on them
        stats = self.__load_id(id)
        path = f'{self.output}\\{stats["name"]}'

        # Open the storage file for reading
        # Set the cursor at the specified position
        # and read the file line by line to evade
        # memory leaks
        with open(self.storage, 'r+b') as r_file:
            r_file.seek(stats['position'], os.SEEK_SET)

            buffer_size = 65536
            file_size = stats['size']

            with open(path, 'wb') as w_file:
                while True:
                    if buffer_size > file_size:
                        w_file.write(r_file.read(file_size))
                        break

                    w_file.write(r_file.read(buffer_size))
                    file_size -= buffer_size

    # noinspection PyShadowingBuiltins
    def __load_id(self, id: str):
        # Open the id storage file
        # with reading permissions
        with open(self.id_storage, 'r') as r_file:
            # Read and store the file content
            content = r_file.read()

            # If the file is empty then the id
            # is not stored
            if len(content) == 0:
                raise IdentityNotStoredException(id)

            # Load the content into ids dictionary
            ids = json.loads(content)

            # Check if the id is contained
            # within the ids dictionary and return it
            if id in ids:
                return ids[id]
            else:
                raise IdentityNotStoredException(id)

    def destroy_file(self):
        # TODO - Replace or destroy the file bytes
        pass


# Raise this exception when the file provided
# is invalid or cannot be found
class FileNotFoundException(Exception):
    def __init__(self, path: str):
        self.path = path

    def __str__(self):
        return f'File {self.path} not found'


# Raise this exception when the program tries to store
# an id that already exists inside the id storage
class IdentityAlreadyExistsException(Exception):
    # noinspection PyShadowingBuiltins
    def __init__(self, id: str):
        self.id = id

    def __str__(self):
        return f'Id "{self.id}" already exists'


# Raise this exception when the id provided does not
# exist inside the id storage
class IdentityNotStoredException(Exception):
    # noinspection PyShadowingBuiltins
    def __init__(self, id: str):
        self.id = id

    def __str__(self):
        return f'Id {self.id} not stored'


# Raise this exception when an invalid directory is specified
# Also if no directory is specified
class DirectoryNotSpecifiedException(Exception):
    def __init__(self, path: str):
        self.path = path

    def __str__(self):
        return f'File {self.path} is not a directory'
