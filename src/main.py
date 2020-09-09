import sys

from src.repositories.file_repository import FileRepository


# noinspection PyUnusedLocal
def main(argv):
    fr = FileRepository('C:\\Users\\Borjan Gjorovski\\Projects\\Python\\pybin\\storage\\storage',
                        'C:\\Users\\Borjan Gjorovski\\Projects\\Python\\pybin\\output')
    fr.store_file('C:\\Users\\Borjan Gjorovski\\Downloads\\The Burning Crusade\\Data\\common.MPQ', 'Big Boi')


if __name__ == '__main__':
    main(sys.argv)
