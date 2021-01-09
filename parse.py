import ply.yacc as yacc
from collections import deque
import sys as sys
import re

from lex import tokens

class Node:
    def parts_str(self):
        st = []
        for part in self.parts:
            st.append(str(part))
        return "\n".join(st)

    def __repr__(self):
        return self.type + ":\n\t" + self.parts_str().replace("\n", "\n\t")

    def add_parts(self, parts):
        self.parts += parts
        return self

    def __init__(self, type, parts):
        self.type = type
        self.parts = parts

def p_program(p):
    '''program : progbody func'''
    p[0] = Node('def', [p[1], p[2]])


def p_progbody(p):
    '''progbody :
                | progbody func'''
    if len(p) > 1:
        if p[1] is None:
            p[1] = Node('body', [])
        p[0] = p[1].add_parts([p[2]])


def p_func(p):
    '''func : DEF ID LBR args RBR LFBR funcbody RFBR'''
    p[0] = Node(p[2], [p[4], p[7]])


def p_args(p):
    '''args :
            | ID
            | args COMMA ID'''
    if len(p) == 1:
        p[0] = Node('args', [])
    elif len(p) == 2:
        p[0] = Node('args', [p[1]])
    else:
        p[0] = p[1].add_parts([p[3]])


def p_funcbody(p):
    '''funcbody :
                | funcbody if
                | funcbody funcall
                | funcbody assign
                | funcbody while
                | funcbody return'''
    if len(p) == 1:
        p[0] = Node('funcbody', [])
    else:
        p[0] = p[1].add_parts([p[2]])


def p_assign(p):
    '''assign : ID ASSIGN expression SEMICOLON
              | ID ASSIGN funcall'''
    p[0] = Node('assign', [p[1], p[3]])


def p_funcall(p):
    '''funcall : ID LBR args RBR SEMICOLON'''
    p[0] = Node('call func '+p[1], [p[3]])


def p_if(p):
    '''if : IF LBR expression RBR LFBR funcbody RFBR elsebranch'''
    if p[8] is None:
        p[0] = Node('if', [p[3], p[6]])
    else:
        p[0] = Node('if', [p[3], p[6], p[8]])


def p_elsebranch(p):
    '''elsebranch :
                  | ELSE LFBR funcbody RFBR'''
    if len(p) == 5:
        p[0] = Node('else', [p[3]])


def p_while(p):
    '''while : WHILE LBR expression RBR LFBR funcbody RFBR'''
    if p[3] != 0:
        p[0] = Node('while', [p[3], p[6]])


def p_return(p):
    '''return : RETURN expression SEMICOLON
              | RETURN ID SEMICOLON '''
    p[0] = Node('return', p[2])

def p_expression_plus(p):
    '''expression : expression PLUS term
                  | ID PLUS term'''
    p[0] = Node(p[2], [p[1], p[3]])


def p_expression_sub(p):
    '''expression : expression SUB term
                  | ID SUB term'''
    p[0] = Node(p[2], [p[1], p[3]])


def p_expression_compar(p):
    '''expression : expression COMPAR expression'''
    p[0] = Node(p[2], [p[1], p[3]])

def p_expression_term(p):
    '''expression : term
                  | ID'''
    p[0] = p[1]


def p_term_times(p):
    'term : term MULT factor'
    p[0] = Node(p[2], [p[1], p[3]])


def p_term_div(p):
    'term : term DIV factor'
    p[0] = Node(p[2], [p[1], p[3]])


def p_term_factor(p):
    '''term : factor
            | ID'''
    p[0] = p[1]

def p_factor_bin(p):
    'factor : DEN expression'
    p[0] = Node(p[1], [p[2]])

def p_factor_num(p):
    'factor : NUM'
    p[0] = p[1]

def p_factor_pow(p):
    'factor : factor POW expression'
    p[0] = Node(p[2], [p[1], p[3]])

def p_factor_expr(p):
    'factor : LBR expression RBR'
    p[0] = p[2]


def p_error(p):
    print("Unexpected token:", p)
    sys.exit()


parser = yacc.yacc()

def build_tree(text):
    return parser.parse(text)


mass1 = []
countTab = deque()
resultList = []
currentTab = 0
assinc = False

def ifWhile(mass):
    return "a > b"


def counterTab(type):
    r = re.compile(".*" + type)
    stingList = list(filter(r.match, resultList)) if list(filter(r.match, resultList)) is not None else None
    if len(stingList) == 0:
        return
    count = 0
    sting = stingList[0]
    if sting is not None:
        for char in sting:
            if char == '\t':
                count = count + 1
    return count, sting


def printCurrentTab():
    string = ''
    for i in range(currentTab):
        string = string + '\t'
    return string


def saveTab(type, cur):
    count, string = counterTab(type)
    resultList.remove(string)
    countTab.append((type, cur, count))


def printBracket(type):
    count = counterTab(type)[0]
    tabs = ''
    global currentTab
    global assinc
    if len(countTab) > 0:
        elm = countTab.pop()
        if count <= elm[2]:
            if type == "assign" and count == elm[2]:
                countTab.append(elm)
                return tabs
            for i in range(elm[1]):
                tabs = tabs + '\t'
            tabs = tabs + '}'
            tabs = tabs + '\n'
            currentTab = int(elm[1])
            assinc = False
        else:
            countTab.append(elm)
            if type == 'assign' and assinc:
                currentTab = currentTab - 1
            elif type == 'assign':
                assinc = True
    elif type == 'assign' and not assinc:
        assinc = True
    elif type == 'assign' and assinc:
        currentTab = currentTab - 1
    return tabs


def assign(mass):
    global currentTab
    mass[0] = None
    mass[1] = None
    string = '\n'
    string = string + printBracket("assign")
    currentTab = currentTab if string != '\n' else currentTab + 1
    string = string + printCurrentTab()
    string = string + 'a=(b+1)*c'
    return string


def argg(mass):
    string = ["("]
    for arg in mass:
        string.append(arg)
        string.append(', ')
    string.pop()
    string.append(') {')
    # mass = None

    return ''.join(string)


def insertType(type, parts):
    string = None
    global currentTab
    if str(type) == 'while' or type == 'WHILE':
        string = '\n'
        string = string + printBracket(type)
        currentTab = currentTab if string != '\n' else currentTab + 1
        string = string + printCurrentTab()
        string = string + "while ( " + ifWhile(parts[0]) + ' ) {'
        saveTab(type, currentTab)
        parts[0] = None
    if str(type) == 'if' or str(type) == 'IF':
        string = '\n'
        string = string + printBracket(type)
        currentTab = currentTab if string != '\n' else currentTab + 1
        string = string + printCurrentTab()
        string = string + "if ( " + ifWhile(parts[0]) + ' ) {'
        saveTab(type, currentTab)
        parts[0] = None
    if str(type) == 'else' or str(type) == 'ELSE':
        string = '\n'
        string = string + printBracket(type)
        currentTab = currentTab if string != '\n' else currentTab + 1
        string = string + printCurrentTab()
        string = string + "else {"
        saveTab(type, currentTab)
        parts[0] = None
    return string


def insertReturn(node):
    bracket = printBracket(node.type)
    string = '\n' + printCurrentTab()
    string = string + 'return ' + node.parts
    string = string + "\n" + bracket
    return string


def recurs(result):
    if result.parts is not None and result.type is not None:
        res = insertType(result.type, result.parts)
        type = None if res is None else res
        if (str(result.type) == 'assign' or str(result.type) == 'ASSIGN') and type is None:
            type = assign(result.parts)

        if (str(result.type) == 'args' or str(result.type) == 'ARGS') and type is None:
            type = argg(result.parts)

        if (str(result.type) == 'return' or str(result.type) == 'RETURN') and type is None:
            type = insertReturn(result)
        if (str(result.type) == 'def' or str(result.type) == 'DEF') and type is None:
            global countTab
            global currentTab
            global assinc
            endProg()
            currentTab = 0
            assinc = False

        mass1.append(type if type is not None else result.type)

        for i in result.parts:
            if i is not None and isinstance(i, Node):
                recurs(i)

def endProg():
    if len(countTab) > 0:
        tabs = "\n"
        for rl in range(countTab.pop()[1]):
            tabs = tabs + '\t'
        tabs = tabs + "}"
        print(tabs)
    print('}')

def outputing(text):
    result = build_tree(text)
    write_file = open('input.txt.out', 'w')
    write_file.write(str(result))
    return result

def outputing_tests(text):
    result = build_tree(text)
    result = str(result)
    return result

def pretty_printing(result):
    global resultList
    resultList = str(result).split('\n')
    recurs(result)

    for out in mass1:
        if str(out) != 'None' and str(out) != 'args' and str(out) != 'funcbody' and str(out) != 'body':
            print(out, end=' ')

    endProg()

read_file = open('input.txt', 'r')
text = read_file.read()

pretty_printing(outputing(text))

#----------------------------

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
string1 = "((2+((2+2)*3)-1))"

print(remove_brackets(string1))
