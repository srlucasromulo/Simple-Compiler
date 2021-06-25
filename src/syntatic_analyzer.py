i = 0
tok_vetor = []

def match(tok):
    global token, i
    if(token == tok):
        print("match " + token)
        i = i + 1
        if(i < len(tok_vetor)):
            token = tok_vetor[i]
    else:
        Error()

def Error():
    global token, i
    print("Erro sintático. Token " + token + " não esperado")

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
    if(token == 'VAR'):
        DeclaracaoSeq()

def Declaracao():
    match('VAR')
    VarList()
    match('TWOP')
    Type()
    match('PCOMMA')

def VarList():
    if(token == 'ID'):
        Fator()
        VarList2()
    else:
        Error()

def VarList2():
    if(token == 'COMMA'):
        match('COMMA')
        Fator()
        VarList2()

def Type():
    if(token == 'BOOLEAN'):
        match('BOOLEAN')
    elif(token == 'INTEGER'):
        match('INTEGER')
    elif(token == 'REAL'):
        match('REAL')
    elif(token == 'STRING'):
        match('STRING')
    else:
        Error()

def ComandoSeq():
    Comando()
    if(token == 'ID' or token == 'IF' or token == 'WHILE' or token == 'PRINT' or token == 'READ'):
        ComandoSeq()

def Comando():
    if(token == 'ID'):
        Fator()
        match('ATTR')
        Expr()
        match('PCOMMA')
    elif(token == 'IF'):
        match('IF')
        Expr()
        match('THEN')
        ComandoSeq()
        match('END')
    elif(token == 'WHILE'):
        match('WHILE')
        Expr()
        match('DO')
        ComandoSeq()
        match('END')
    elif(token == 'PRINT'):
        match('PRINT')
        Expr()
        match('PCOMMA')
    elif(token == 'READ'):
        match('READ')
        Fator()
        match('PCOMMA')

def Expr():
    Rel()
    ExprOpc()

def ExprOpc():
    OpIgual()
    Rel()
    if(token == 'EQUAL' or token == 'NEQUAL' or token == 'ID' or token == 'INT_CONST' or token == 'REAL_CONST'):
        ExprOpc()

def OpIgual():
    if(token == 'EQUAL'):
        match('EQUAL')
    elif(token == 'NEQUAL'):
        match('NEQUAL')

def Rel():
    Adicao()
    RelOpc()

def RelOpc():
    OpRel()
    Adicao()
    if(token == 'LT' or token == 'GT' or token == 'LE' or token == 'GE' or token == 'ID' or token == 'INT_CONST' or token == 'REAL_CONST'):
        RelOpc()

def OpRel():
    if(token == 'LT'):
        match('LT')
    elif(token == 'GE'):
        match('GE')
    elif(token == 'LE'):
        match('LE')
    elif(token == 'GT'):
        match('GT')

def Adicao():
    Termo()
    AdicaoOpc()

def AdicaoOpc():
    OpAdicao()
    Termo()
    if(token == 'PLUS' or token == 'MINUS' or token == 'ID' or token == 'INT_CONST' or token == 'REAL_CONST'):
        AdicaoOpc()

def OpAdicao():
    if(token == 'PLUS'):
        match('PLUS')
    elif(token == 'MINUS'):
        match('MINUS')

def Termo():
    Fator()
    TermoOpc()

def TermoOpc():
    OpMult()
    Fator()
    if(token == 'MULT' or token == 'DIV' or token == 'ID' or token == 'INT_CONST' or token == 'REAL_CONST'):
        TermoOpc()

def OpMult():
    if(token == 'MULT'):
        match('MULT')
    elif(token == 'DIV'):
        match('DIV')

def Fator():
    if(token == 'ID'):
        match('ID')
    elif(token == 'INT_CONST'):
        match('INT_CONST')
    elif(token == 'REAL_CONST'):
        match('REAL_CONST')
    elif(token == 'TRUE'):
        match('TRUE')
    elif(token == 'FALSE'):
        match('FALSE')
    elif(token == 'STRING_LITERAL'):
        match('STRING_LITERAL')
    elif(token == 'LBRACKET'):
        match('LBRACKET')
        Expr()
        match('RBRACKET')

def syntatic_analyzer(toke):
    global token, i
    for j in range(0, len(toke)):
        tok_vetor.append(toke[j][1])
    token = tok_vetor[i]
    Programa()
