import os
import json


class FileRepository(object):
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
        with open(path, 'rb') as file:
            # Get the file stats
            file_size = os.path.getsize(path)
            file_extension = os.path.splitext(path)[1]
            file_name = os.path.basename(path)

            # Begin reading the file
            file_bytes = file.read()

            # Position the cursor at the end of the file
            # Store the file stats (id, position, size, name and extension)
            with open(self.storage, 'r+b') as storage:
                storage.seek(0, os.SEEK_END)
                self.__store_id(id, storage.tell(), file_size, file_name, file_extension)

                storage.write(file_bytes)

    # noinspection PyShadowingBuiltins
    def __store_id(self, id: str, position: int, size: int, name: str, extension: str):
        with open(self.id_storage, 'r') as file:
            content = file.read()

            if len(content) == 0:
                ids = {}
            else:
                ids = json.loads(content)

            if id in ids:
                raise IdentityAlreadyExistsException(id)

            ids[id] = {
                'position': position,
                'size': size,
                'name': name,
                'extension': extension,
            }

        with open(self.id_storage, 'w') as file:
            file.write(json.dumps(ids))

    # noinspection PyShadowingBuiltins
    def load_file(self, id: str):
        stats = self.__load_id(id)
        path = f'{self.output}\\{stats["name"]}'

        with open(self.storage, 'r+b') as file:
            file.seek(stats['position'], os.SEEK_SET)
            file_bytes = file.read(stats['size'])

        with open(path, 'wb') as file:
            file.write(file_bytes)

    # noinspection PyShadowingBuiltins
    def __load_id(self, id: str):
        with open(self.id_storage, 'r') as file:
            content = file.read()

            if len(content) == 0:
                raise IdentityNotStoredException(id)

            ids = json.loads(content)

            if id in ids:
                return ids[id]
            else:
                raise IdentityNotStoredException(id)

    def destroy_file(self):
        pass


class FileNotFoundException(Exception):
    def __init__(self, path: str):
        self.path = path

    def __str__(self):
        return f'File {self.path} not found'


class IdentityAlreadyExistsException(Exception):
    # noinspection PyShadowingBuiltins
    def __init__(self, id: str):
        self.id = id

    def __str__(self):
        return f'Id "{self.id}" already exists'


class IdentityNotStoredException(Exception):
    # noinspection PyShadowingBuiltins
    def __init__(self, id: str):
        self.id = id

    def __str__(self):
        return f'Id {self.id} not stored'


class DirectoryNotSpecifiedException(Exception):
    def __init__(self, path: str):
        self.path = path

    def __str__(self):
        return f'File {self.path} is not a directory'
