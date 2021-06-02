import re

keywords = ['program', 'begin', 'end', 'var', 'boolean', 'integer', 'real', 'string', 'if', 'then', 'while', 'do',
            'print', 'read', 'true', 'false']

sigma = '[ ;a-zA-Z0-9_,:=!<>/*-+\n\t]'

buffer = [None]


def get_c():
    try:
        # noinspection PyUnresolvedReferences
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

        if not re.findall(sigma, c):
            tokens.append((c, 'NOT IN SIGMA', line_index))
            break

        if c == ' ':
            c = get_c()

        if c == '\n':
            line_index += 1
            c = get_c()

        if c == ';':
            tokens.append((';', 'PCOMMA', line_index))
            c = get_c()

        if c == ',':
            tokens.append((',', 'COMMA', line_index))
            c = get_c()

        if c == '+':
            tokens.append(('+', 'PLUS', line_index))
            c = get_c()

        if c == '-':
            tokens.append(('-', 'MINUS', line_index))
            c = get_c()

        if c == '*':
            tokens.append(('*', 'MULT', line_index))
            c = get_c()

        if c == '/':
            tokens.append(('/', 'DIV', line_index))
            c = get_c()

        if c == '(':
            tokens.append(('(', 'LBRACKET', line_index))
            c = get_c()

        if c == ')':
            tokens.append((')', 'RBRACKET', line_index))
            c = get_c()

        if c == '<':
            c = get_c()
            if c == '=':
                tokens.append(('<=', 'LE', line_index))
                c = get_c()
            else:
                tokens.append(('<', 'LT', line_index))

        if c == '>':
            c = get_c()
            if c == '=':
                tokens.append(('>=', 'GE', line_index))
                c = get_c()
            else:
                tokens.append(('>', 'GT', line_index))

        if c == ':':
            c = get_c()
            if c == '=':
                tokens.append((':=', 'ATTR', line_index))
                c = get_c()
            else:
                tokens.append((':', 'TWOP', line_index))

        if c == '=':
            c = get_c()
            if c == '=':
                tokens.append(('==', 'EQUAL', line_index))
                c = get_c()

        if c == '!':
            c = get_c()
            if c == '=':
                tokens.append(('==', 'NEQUAL', line_index))
                c = get_c()

        if re.findall('[a-zA-Z]', c):
            string = ''
            while re.findall('[a-zA-Z_]', c):
                string += c
                c = get_c()
            if string in keywords:
                tokens.append((string, string.upper(), line_index))
            else:
                tokens.append((string, 'ID', line_index))

        if c == '"':
            string = ''
            c = get_c()
            while c != '"':
                string += c
                c = get_c()
            tokens.append((string, 'STR_CONST', line_index))
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
                tokens.append((string.upper(), 'REAL_CONST', line_index))
            else:
                tokens.append((string.upper(), 'INT_CONST', line_index))

    return tokens
