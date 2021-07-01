from datetime import datetime

i = 0
tok_vetor = []
SymbolTable = []
varSymbol = []
variavel = None

log_file = './logs/syntatic.log'
log = None
errors = 0

follow = {}
follow['PROGRAM'] = ['ID']
follow['BEGIN'] = ['ID', 'EOF', 'PRINT', 'READ', 'END']
follow['VAR'] = ['ID']
follow['TWOP'] = ['BOOLEAN', 'INTEGER', 'REAL', 'STRING']
follow['COMMA'] = ['ID']
follow['LBRACKET'] = ['ID', 'REAL_CONST', 'INT_CONST', 'STRING_LITERAL']
follow['REAL_CONST'] = ['PCOMMA', 'PLUS', 'MULT', 'DIV', 'MINUS', 'EQUAL', 'ATTR', 'NEQUAL', 'GT', 'GE', 'LT', 'LE']
follow['PLUS'] = follow['REAL_CONST']
follow['MULT'] = follow['REAL_CONST']
follow['DIV'] = follow['REAL_CONST']
follow['MINUS'] = follow['REAL_CONST']
follow['EQUAL'] = follow['REAL_CONST']
follow['NEQUAL'] = follow['REAL_CONST']
follow['ATTR'] = follow['REAL_CONST']
follow['GT'] = follow['REAL_CONST']
follow['GE'] = follow['REAL_CONST']
follow['LT'] = follow['REAL_CONST']
follow['LE'] = follow['REAL_CONST']
follow['INT_CONST'] = follow['REAL_CONST']
follow['STRING_LITERAL'] = ['ID', 'PCOMMA']
follow['IF'] = ['LBRACKET', 'TRUE', 'FALSE'] + follow['LBRACKET'] + ['RBRACKET']
follow['THEN'] = ['ID', 'END', 'PRINT', 'READ']
follow['WHILE'] = ['LBRACKET', 'TRUE', 'FALSE'] + follow['LBRACKET'] + ['RBRACKET']
follow['DO'] = ['LBRACKET', 'ID', 'END', 'RBRACKET'] + follow['LBRACKET']
follow['PRINT'] = follow['LBRACKET'] + ['RBRACKET']
follow['READ'] = follow['LBRACKET'] + ['RBRACKET']
follow['ID'] = ['COMMA'] + follow['REAL_CONST']


def match(tok):
    global token, i
    if(token[1] == tok):
        print("match " + token[1])
        i = i + 1
        if(i < len(tok_vetor)):
            token = tok_vetor[i]
    else:
        Error()

def Error():
    global token, i, errors, log
    erro = tok_vetor[i - 1]
    log.write(f'[{datetime.now().strftime("%X")}] '
                          f'Syntatic Error. line {token[2]} - Token {token[1]} unexpected. Some down:\n{follow[erro[1]]} expected\n')
    errors += 1

def Programa():
    match('PROGRAM')
    match('ID')
    match('PCOMMA')
    Bloco()

def Bloco():
    DeclaracaoSeq()
    match('BEGIN')
    ComandoSeq()
    match('END')
    match('EOF')

def DeclaracaoSeq():
    Declaracao()
    if(token[1] == 'VAR'):
        DeclaracaoSeq()

def Declaracao():
    match('VAR')
    VarList()
    match('TWOP')
    Type()
    match('PCOMMA')

def VarList():
    global errors, log
    if(token[1] == 'ID'):
        flag = False
        for i in range(0, len(SymbolTable)):
            if(token[0] in SymbolTable[i][0]):
                flag = True
        if(not flag):
            varSymbol.append(token)
        else:
            log.write(f'[{datetime.now().strftime("%X")}] '
                          f'Semantic Error. {token[0]} already declared: line c\n')
            errors += 1
        Fator()
        VarList2()
    else:
        Error()

def VarList2():
    global errors,log
    if(token[1] == 'COMMA'):
        match('COMMA')
        flag = False
        for i in range(0, len(SymbolTable)):
            if(token[0] in SymbolTable[i][0]):
                flag = True
        if(not flag):
            varSymbol.append(token)
        else:
            log.write(f'[{datetime.now().strftime("%X")}] '
                          f'Semantic Error. {token[0]} already declared: line {token[2]}\n')
            errors += 1
        Fator()
        VarList2()

def Type():
    if(token[1] == 'BOOLEAN'):
        for i in varSymbol:
            SymbolTable.append((i[0], token[1]))
        varSymbol.clear()
        match('BOOLEAN')
    elif(token[1] == 'INTEGER'):
        for i in varSymbol:
            SymbolTable.append((i[0], token[1]))
        varSymbol.clear()
        match('INTEGER')
    elif(token[1] == 'REAL'):
        for i in varSymbol:
            SymbolTable.append((i[0], token[1]))
        varSymbol.clear()
        match('REAL')
    elif(token[1] == 'STRING'):
        for i in varSymbol:
            SymbolTable.append((i[0], token[1]))
        varSymbol.clear()
        match('STRING')
    else:
        Error()

def ComandoSeq():
    Comando()
    if(token[1] == 'ID' or token[1] == 'IF' or token[1] == 'WHILE' or token[1] == 'PRINT' or token[1] == 'READ'):
        ComandoSeq()

def Comando():
    global variavel, errors,log
    if(token[1] == 'ID'):
        variavel = None
        for i in range(0, len(SymbolTable)):
            if(token[0] in SymbolTable[i][0]):
                variavel = SymbolTable[i]
        if(not variavel):
            log.write(f'[{datetime.now().strftime("%X")}] '
                          f'Semantic Error. {token[0]} not declared: line {token[2]}\n')
            errors += 1
        Fator()
        match('ATTR')
        Expr()
        match('PCOMMA')
    elif(token[1] == 'IF'):
        match('IF')
        Expr()
        match('THEN')
        ComandoSeq()
        match('END')
    elif(token[1] == 'WHILE'):
        match('WHILE')
        Expr()
        match('DO')
        ComandoSeq()
        match('END')
    elif(token[1] == 'PRINT'):
        match('PRINT')
        Expr()
        match('PCOMMA')
    elif(token[1] == 'READ'):
        match('READ')
        Fator()
        match('PCOMMA')

def Expr():
    Rel()
    ExprOpc()

def ExprOpc():
    OpIgual()
    Rel()
    if(token[1] == 'EQUAL' or token[1] == 'NEQUAL' or token[1] == 'ID' or token[1] == 'INT_CONST' or token[1] == 'REAL_CONST'):
        ExprOpc()

def OpIgual():
    if(token[1] == 'EQUAL'):
        match('EQUAL')
    elif(token[1] == 'NEQUAL'):
        match('NEQUAL')

def Rel():
    Adicao()
    RelOpc()

def RelOpc():
    OpRel()
    Adicao()
    if(token[1] == 'LT' or token[1] == 'GT' or token[1] == 'LE' or token[1] == 'GE' or token[1] == 'ID' or token[1] == 'INT_CONST' or token[1] == 'REAL_CONST'):
        RelOpc()

def OpRel():
    if(token[1] == 'LT'):
        match('LT')
    elif(token[1] == 'GE'):
        match('GE')
    elif(token[1] == 'LE'):
        match('LE')
    elif(token[1] == 'GT'):
        match('GT')

def Adicao():
    Termo()
    AdicaoOpc()

def AdicaoOpc():
    OpAdicao()
    Termo()
    if(token[1] == 'PLUS' or token[1] == 'MINUS' or token[1] == 'ID' or token[1] == 'INT_CONST' or token[1] == 'REAL_CONST'):
        AdicaoOpc()

def OpAdicao():
    if(token[1] == 'PLUS'):
        match('PLUS')
    elif(token[1] == 'MINUS'):
        match('MINUS')

def Termo():
    Fator()
    TermoOpc()

def TermoOpc():
    OpMult()
    Fator()
    if(token[1] == 'MULT' or token[1] == 'DIV' or token[1] == 'ID' or token[1] == 'INT_CONST' or token[1] == 'REAL_CONST'):
        TermoOpc()

def OpMult():
    if(token[1] == 'MULT'):
        match('MULT')
    elif(token[1] == 'DIV'):
        match('DIV')

def Fator():
    if(token[1] == 'ID'):
        match('ID')
    elif(token[1] == 'INT_CONST'):
        match('INT_CONST')
    elif(token[1] == 'REAL_CONST'):
        match('REAL_CONST')
    elif(token[1] == 'TRUE'):
        match('TRUE')
    elif(token[1] == 'FALSE'):
        match('FALSE')
    elif(token[1] == 'STRING_LITERAL'):
        match('STRING_LITERAL')
    elif(token[1] == 'LBRACKET'):
        match('LBRACKET')
        Expr()
        match('RBRACKET')

def syntatic_analyzer(toke, filename):
    global token, i, tok_vetor,log
    
    log = open(log_file, 'a')
    log.write('\n--------------------------------------------------------\n')
    log.write(f'Error log from code {filename}\n')
    log.write(f'Syntatic analyzer started at: {datetime.now().strftime("%A %x %X")}\n')
    log.write('--------------------------------------------------------\n')
    tok_vetor = toke
    token = tok_vetor[i]
    Programa()
    log.write('--------------------------------------------------------\n')
    log.write(f'Errors found in code {filename}: {errors}\n')
    log.write(f'Syntatic analyzer finished at: {datetime.now().strftime("%A %x %X")}\n')
    log.write('--------------------------------------------------------\n\n')
    log.close()
    i = 0
