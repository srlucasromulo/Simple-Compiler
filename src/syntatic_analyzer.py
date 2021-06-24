i = 0
tok_vetor = ['PROGRAM', 'ID', 'PCOMA','VAR', 'ID', 'DPO', 'INTEGER', 'PCOMA', 'VAR', 'ID', 'DPO', 'INTEGER', 'PCOMA']
token = tok_vetor[i]

def match(tok):
    global token, i
    if(token == tok):
        print("match " + token)
        i = i + 1
        if(i < len(tok_vetor)):
            token = tok_vetor[i]
    else:
        print("Error")

def Programa():
    match('PROGRAM')
    match('ID')
    match('PCOMA')
    Bloco()

def Bloco():
    DeclaracaoSeq()
    match('BEGIN')
    ComandoSeq()
    match('END')

def DeclaracaoSeq():
    Declaracao()
    if(token == 'VAR'):
        DeclaracaoSeq()

def Declaracao():
    match('VAR')
    VarList()
    match('DPO')
    Type()
    match('PCOMA')

def VarList():
    if(token == 'ID'):
        Fator()
        VarList2()
    else:
        print("Error")

def VarList2():
    if(token == 'COMA'):
        match('COMA')
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

def ComandoSeq():
    Comando()
    if(token == 'ID' or token == 'IF' or token == 'WHILE' or token == 'PRINT' or token == 'READ'):
        ComandoSeq()

def Comando():
    if(token == 'ID'):
        Fator()
        match('RECE')
        Expr()
        match('PCOMA')
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
        match('PCOMA')
    elif(token == 'READ'):
        match('READ')
        Fator()
        match('PCOMA')
    else:
        print("Error")

def Expr():
    Rel()
    ExprOpc()

def ExprOpc():
    OpIgual()
    Rel()
#     ExprOpc()

def OpIgual():
    if(token == 'IGUAL'):
        match('IGUAL')
    elif(token == 'DIF'):
        match('DIF')

def Rel():
    Adicao()
    RelOpc()

def RelOpc():
    OpRel()
    Adicao()
#     RelOpc()

def OpRel():
    if(token == 'MENOR'):
        match('MENOR')
    elif(token == 'MAIORE'):
        match('MAIORE')
    elif(token == 'MENORE'):
        match('MENORE')
    elif(token == 'MAIOR'):
        match('MAIOR')

def Adicao():
    Termo()
    AdicaoOpc()

def AdicaoOpc():
    OpAdicao()
    Termo()
#     AdicaoOpc()

def OpAdicao():
    if(token == 'PLUS'):
        match('PLUS')
    elif(token == 'SUB'):
        match('SUB')

def Termo():
    Fator()
    TermoOpc()

def TermoOpc():
    OpMult()
    Fator()
#     TermoOpc()

def OpMult():
    if(token == 'MULT'):
        match('MULT')
    elif(token == 'DIV'):
        match('DIV')

def Fator():
    if(token == 'ID'):
        match('ID')
    elif(token == 'integer_const'):
        match('integer_const')
    elif(token == 'real_const'):
        match('real_const')
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

Programa()
