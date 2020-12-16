import ply.lex as lex 
import sys
import re

reserved = {
    'False':    'FALSE',
    'True':     'TRUE',
    'None':     'NONE',
    'and':      'AND',
    'with':     'WITH',
    'as':       'AS',
    'assert':   'ASSERT',
    'break':    'BREAK',
    'class':    'CLASS',
    'continue': 'CONTINUE',
    'def':      'DEF',
    'del':      'DEL',
    'elif':     'ELIF',
    'else':     'ELSE',
    'except':   'EXCEPT',
    'finally':  'FINALLY',
    'for':      'FOR',
    'from':     'FROM',
    'global':   'GLOBAL',
    'if':       'IF',
    'import':   'IMPORT',
    'in':       'IN',
    'is':       'IS',
    'lambda':   'LAMBDA',
    'nonlocal': 'NONLOCAL',
    'not':      'NOT',
    'or':       'OR',
    'pass':     'PASS',
    'raise':    'RAISE',
    'return':   'RETURN',
    'try':      'TRY',
    'while':    'WHILE',
    'yield':    'YIELD'
}

tokens = [
    'NUM',    #число                  number
    'PLUS',   #сложение               +
    'MULT',   #умножение              *
    'DIV',    #деление                /
    'SUB',    #вычитание              -
    'POW',    #возведение в степень   **
    'CON',    #конъюнкция             &&
    'DIS',    #дизъюнкция             ||
    'NEG',    #логическое отрицание   --
    'LESS',   #меньше                 <
    'LOE',    #меньше или равно       <=
    'EQL',    #равно                  ==
    'MORE',   #больше                 >
    'MOE',    #больше или равно       >=
    'ID',     #идентификатор          listNat_123
    'LBR',    #левая скобка           (
    'RBR'     #правая скобка          )
] + list(reserved.values())

def t_ID(t):
    r'[a-z_][a-z_0-9]*'
    t.type = reserved.get(t.value, 'ID')
    return t

def t_NUM(t): 
    r'[0-9]+' #число может быть отрицательным, поэтому может быть либо один минус перед числом, либо ни одного: 50, -50
    t.value = int(t.value)
    return t

t_PLUS = r'\+'
t_SUB = r'\-'
t_MULT = r'\*'
t_LBR = r'\('
t_RBR = r'\)'
t_POW = r'\*\*'
t_DIV = r'\/'
t_CON = r'\&\&'
t_DIS = r'\|\|'
t_NEG = r'\-\-'
t_LESS = r'\<'
t_LOE = r'\<\='
t_EQL = r'\=\='
t_MORE = r'\>'
t_MOE = r'\>\='

t_ignore = ' \t\r\n\v\f\a\b'

def t_newline(t): 
  r'\n+'
  t.lexer.lineno += len(t.value)

def t_error(t): 
  print("Illegal character '%s'" % t.value[0])
  t.lexer.skip(1)

lexer = lex.lex() 

read_file = open('input.txt', 'r')
text = read_file.read()
read_file.close()
lexer.input(text) 

while True: 
  tok = lexer.token() 
  if not tok: 
    break
  print(tok)

def remove_brackets(term): #удаление лишних скобок
    a = 0
    while True:
        try:
            a = term.index("(", a)
        except ValueError:
            break
        b = a
        while True:
            b = term.index(")", b + 1)
            if term[a + 1:b].count("(") == term[a + 1:b].count(")"):
                break
        new_term = term[:a] + term[a + 1:b] + term[b + 1:]
        if eval(term) != eval(new_term):
            a += 1
            continue
        term = new_term
    return term

write_file = open('input.txt.out', 'w')
write_file.write(remove_brackets(text))
write_file.close()