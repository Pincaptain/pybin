import sys
import os

from src.use_cases.store_file import StoreFile
from src.use_cases.load_file import LoadFile
from src.use_cases.destroy_file import DestroyFile
from src.configs.injection_config import InjectionConfig

INVALID_NUM_ARGUMENTS = 1
INVALID_ARGUMENTS = 2


def main(argv: list):
    """
    Based on the provided options and parameters instantiate the
    needed use case and store/load or destroy a file/s.

    :param argv: Command line arguments
    """

    injection_config = InjectionConfig('../resources/config.ini')

    if len(argv) < 2:
        exit(INVALID_NUM_ARGUMENTS)

    valid_options = ['-s', '-sm', '-l', '-lm', '-d', '-dm']
    option = argv[1]

    if option not in valid_options:
        exit(INVALID_ARGUMENTS)

    if option == '-s':
        # noinspection PyBroadException
        try:
            file_path = argv[2]
            file_id = argv[3]

            store_file = StoreFile(injection_config.get_file_service())
            store_file.store_file(file_path, file_id)
        except IndexError:
            exit(INVALID_NUM_ARGUMENTS)

    elif option == '-sm':
        # noinspection PyBroadException
        try:
            files = []
            for i in range(2, len(argv)):
                file_path = argv[i]

                if os.path.isdir(file_path):
                    files.extend(list_files(file_path))
                else:
                    files.append({
                        'path': file_path,
                        'id': os.path.basename(file_path)
                    })

            store_file = StoreFile(injection_config.get_file_service())
            store_file.store_files(files)
        except IndexError:
            exit(INVALID_NUM_ARGUMENTS)

    elif option == '-l':
        # noinspection PyBroadException
        try:
            file_id = argv[2]

            load_file = LoadFile(injection_config.get_file_service())
            load_file.load_file(file_id)
        except IndexError:
            exit(INVALID_NUM_ARGUMENTS)

    elif option == '-lm':
        # noinspection PyBroadException
        try:
            ids = []
            for i in range(2, len(argv)):
                ids.append(argv[i])

            load_file = LoadFile(injection_config.get_file_service())
            load_file.load_files(ids)
        except IndexError:
            exit(INVALID_NUM_ARGUMENTS)

    elif option == '-d':
        # noinspection PyBroadException
        try:
            file_id = argv[2]

            destroy_file = DestroyFile(injection_config.get_file_service())
            destroy_file.destroy_file(file_id)
        except IndexError:
            exit(INVALID_NUM_ARGUMENTS)

    elif option == '-dm':
        # noinspection PyBroadException
        try:
            ids = []
            for i in range(2, len(argv)):
                ids.append(argv[i])

            destroy_file = DestroyFile(injection_config.get_file_service())
            destroy_file.destroy_files(ids)
        except IndexError:
            exit(INVALID_NUM_ARGUMENTS)


def list_files(path: str):
    """
    Return a list of files in the initial directory and all the other directories
    inside of it recursively.

    :param path: Initial directory path
    :return: List of files
    """

    file_list = []
    files = os.listdir(path)

    for file in files:
        abs_file = os.path.join(path, file)
        if os.path.isdir(abs_file):
            file_list.extend(list_files(abs_file))
        else:
            file_list.append({
                'path': abs_file,
                'id': file
            })

    return file_list


if __name__ == '__main__':
    main(sys.argv)
