import sys
from src.lexical_analyzer import lexical_analyzer


def main():
    args = sys.argv[1:]
    src_codes = './source_codes/'

    for filename in args:
        try:
            file = open(src_codes + filename, 'r')
            file_buffer = iter(file.read().replace('\t', ''))
            file.close()

            lexical_analyzer(file_buffer)   # talvez tem q fazer surround
            # syntactic analyzer
        except IOError:
            print(f'{filename}: file not found!!')


if __name__ == '__main__':
    main()
