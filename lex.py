import ply.lex as lex
import re

reserved = {
    'def': 'DEF',
    'while': 'WHILE',
    'if': 'IF',
    'else': 'ELSE',
    'return': 'RETURN',
}

tokens = [
    'NUM',          #число                  number
    'PLUS',         #сложение               +          
    'MULT',         #умножение              *
    'DIV',          #деление                /
    'SUB',          #вычитание              -
    'ID',           #идентификатор          listNat_123
    'DIS',          #дизъюнкция             ||
    'CON',          #конъюнкция             &&
    'DEN',          #логическое отрицание   --
    'POW',          #возведение в степень   **
    'COMPAR',       #сравнение              >, >=, <, <=, /=, ==
    'LBR',          #левая скобка           (
    'LFBR',         #левая фигурная скобка  {
    'RFBR',         #правая фигурная скобка {
    'RBR',          #правая скобка          )
    'ASSIGN',       #приравнивание          =
    'SEMICOLON',    #точка с запятой        ;       
    'COMMA'        #запятая                ,
] + list(reserved.values())


def t_ID(t):
    r'[a-z_][a-z_0-9]*'
    t.type = reserved.get(t.value, 'ID')
    return t


def t_NUM(t):
    r'[0-9]+'
    t.value = int(t.value)
    return t


t_PLUS = r'\+'
t_MULT = r'\*'
t_LBR = r'\('
t_RBR = r'\)'
t_LFBR = r'\{'
t_RFBR = r'\}'
t_SUB = r'\-'
t_POW = r'\*\*'  # **S
t_DIV = r'/'
t_DIS = r'\|\|'  # ||
t_CON = r'\&\&'
t_DEN = r'\-\-'  # --
t_COMPAR = r'(\<|\<=|==|\>|\>=|/=)'  # <, <=, ==, /=, >, >=
t_ASSIGN = r'='
t_SEMICOLON = r';'
t_COMMA = r','

t_ignore = ' \t\n'

def t_error(t):
    print("Illegal character ", t.value[0])

lexer = lex.lex()

file = open('input.txt', 'r')
text = file.read()
file.close()
lexer.input(text)


while True:
    tok = lexer.token()
    if not tok:
        break
    print(tok)