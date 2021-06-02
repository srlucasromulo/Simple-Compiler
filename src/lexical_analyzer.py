import re

keywords = ['program', 'begin', 'end', 'var', 'boolean', 'integer', 'real', 'string', 'if', 'then', 'while', 'do',
            'print', 'read', 'true', 'false']

sigma = '[ ;a-zA-Z0-9_,:=!<>/*+-?#\n\t]'  # alfabeto, falta coisa

buffer = [None]


def get_c():
    try:
        c = buffer[0].__next__()
    except StopIteration:
        c = ''
    return c


def lexical_analyzer(file: iter):
    buffer[0] = file
    line_index = 1
    tokens = []

    c = get_c()
    while True:
        if c == '':
            break

        if c == '\n':
            line_index += 1
            c = get_c()

        if re.findall('[a-zA-Z]', c):
            string = ''
            while re.findall('[a-zA-Z_]', c):
                string += c
                c = get_c()
            print(string)   # salvar id

        if c == '\"':
            string = ''
            c = get_c()
            while c != '\"':
                string += c
                c = get_c()
            print(string)   # salvar string
            c = get_c()

        if re.findall('[0-9]', c):
            string = ''
            while re.findall('[0-9]', c):
                string += c
                c = get_c()
            if c == '.':
                string += c
                c = get_c()
                while re.findall('[0-9]', c):
                    string += c
                    c = get_c()
                print(string)   # salva float
            else:
                print(string)   # salvar int

        c = get_c() # vai sair

        # if c == '\t':
        #     c = get_c(buffer)
