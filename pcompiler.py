import sys
from src.lexical_analyzer import lexical_analyzer
from src.syntatic_analyzer import syntatic_analyzer


def clear_logs():
    log = open('./logs/lexical.log', 'w')
    log.close()
    log = open('./logs/syntatic.log', 'w')
    log.close()

def main():
    args = sys.argv[1:]
    src_codes = './source_codes/'
    clear_logs()

    for filename in args:
        try:
            file = open(src_codes + filename, 'r')
            file_buffer = iter(file.read().replace('\t', ''))
            file.close()

            tokens = lexical_analyzer(file_buffer, filename)
            print(tokens)
            syntatic_analyzer(tokens)
        except IOError:
            print(f'{filename}: file not found!!')


if __name__ == '__main__':
    main()
