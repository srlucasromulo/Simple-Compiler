import re
from datetime import datetime

keywords = ['program', 'begin', 'end', 'var', 'boolean', 'integer', 'real', 'string', 'if', 'then', 'while', 'do',
            'print', 'read', 'true', 'false']

sigma = '[ ;a-zA-Z0-9_,:=!<>/*-+\n\t]'

buffer = [None]

log_file = './logs/lexical.log'

def get_c():
    try:
        # noinspection PyUnresolvedReferences
        c = buffer[0].__next__()
    except StopIteration:
        c = ''
    return c


def lexical_analyzer(file: iter, filename):
    buffer[0] = file
    line_index = 1
    tokens = []
    errors = 0

    log = open(log_file, 'a')
    log.write('\n--------------------------------------------------------\n')
    log.write(f'Error log from code {filename}\n')
    log.write(f'Lexical analyzer started at: {datetime.now().strftime("%A %x %X")}\n')
    log.write('--------------------------------------------------------\n')

    c = get_c()
    while True:
        if c == '':
            break

        if not re.findall(sigma, c):
            log.write(f'- Char {c} found in line {line_index} doesnt belong to Sigma\n')
            c = get_c()
            errors += 1

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
                tokens.append(('!=', 'NEQUAL', line_index))
                c = get_c()

        # id tokens
        if re.findall('[a-zA-Z]', c):
            string = ''
            while re.findall('[a-zA-Z_0-9]', c):
                string += c
                c = get_c()
            if string in keywords:
                tokens.append((string, string.upper(), line_index))
            else:
                tokens.append((string, 'ID', line_index))

        # string tokens
        if c == '"':
            string = ''
            c = get_c()
            while c != '"':
                string += c
                c = get_c()
            tokens.append((string, 'STRING_LITERAL', line_index))
            c = get_c()

        # int and float tokens
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
                tokens.append((float(string), 'REAL_CONST', line_index))
            else:
                tokens.append((int(string), 'INT_CONST', line_index))

    tokens.append(('EOF', 'EOF', line_index))

    log.write('--------------------------------------------------------\n')
    log.write(f'Erros found in code {filename}: {errors}\n')
    log.write(f'Lexical analyzer fineshed at: {datetime.now().strftime("%A %x %X")}\n')
    log.write('--------------------------------------------------------\n\n')
    log.close()

    return tokens
