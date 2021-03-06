import re
import sys as sys
from collections import deque
from lex import tokens

import ply.yacc as yacc


class Node:
    def parts_str(self):
        st = []
        for part in self.parts:
            if part != None:
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
            | expression
            | args COMMA expression'''
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
    '''assign : ID ASSIGN expression SEMICOLON'''
    p[0] = Node('assign', [p[1], p[3]])


def p_funcall(p):
    '''funcall : ID LBR args RBR SEMICOLON'''
    p[0] = Node('call func ' + p[1], [p[3]])

def p_funcvar(p):
    '''funcvar : ID LBR args RBR'''
    p[0] = Node('variable func ' + p[1], [p[3]])

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
    p[0] = Node('return', [p[2]])


def p_expression_plus(p):
    '''expression : expression PLUS term'''
    p[0] = Node(p[2], [p[1], p[3]])


def p_expression_sub(p):
    '''expression : expression SUB term'''
    p[0] = Node(p[2], [p[1], p[3]])


def p_expression_compar(p):
    '''expression : expression MOREQ expression
                  | expression LESEQ expression
                  | expression LT expression
                  | expression GT expression
                  | expression EQ expression
                  | expression NE expression'''
    p[0] = Node(p[2], [p[1], p[3]])


def p_expression_bin(p):
    '''expression : expression DIS term'''
    p[0] = Node(p[2], [p[1], p[3]])


def p_expression_term(p):
    '''expression : term'''
    p[0] = p[1]


def p_term_times(p):
    'term : term MULT factor'
    p[0] = Node(p[2], [p[1], p[3]])


def p_term_bin(p):
    'term : term CON factor'
    p[0] = Node(p[2], [p[1], p[3]])


def p_term_div(p):
    'term : term DIV factor'
    p[0] = Node(p[2], [p[1], p[3]])


def p_term_factor(p):
    '''term : factor'''
    p[0] = p[1]


def p_factor_num(p):
    '''factor : NUM
              | funcvar
              | ID'''
    p[0] = p[1]


def p_factor_bin(p):
    'factor : DEN expression'
    p[0] = Node(p[1], [p[2]])


def p_factor_pow(p):
    'factor : factor POW expression'
    p[0] = Node(p[2], [p[1], p[3]])


def p_factor_expr(p):
    '''factor : LBR expression RBR'''
    if len(p) == 2:
        p[0] = p[1]
    else:
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
tabs = ''
currentTab = 0
assinc = False
prettyPrint = ""
flag = 0;


def ifWhile(mass):
    global flag
    flag = 1;
    if len(str(mass)) == 1:
        return "(" + str(mass) + ")"
    return expression_processing(mass)


def counterTab(type):
    r = re.compile(".*" + type)
    stringList = list(filter(r.match, resultList)) if list(filter(r.match, resultList)) is not None else None
    if len(stringList) == 0:
        return
    count = 0
    string = stringList[0]
    if string is not None:
        for char in string:
            if char == '\t':
                count = count + 1
    return count, string


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
    global tabs
    global currentTab
    global assinc
    global resultList
    global prettyPrint
    if len(countTab) > 0:
        elm = countTab.pop()
        if count <= elm[2] or (type == 'else' and elm[0] == 'if' and count == elm[2] + 1):

            tabs = tabs if tabs == '' and elm[1] > 0 else tabs + '\n'
            for i in range(elm[1]):
                tabs = tabs + '\t'
            tabs = tabs + '}'
            tabs = tabs + '\n' if type != 'else' and type != 'return' else tabs
            currentTab = int(elm[1])
            assinc = False
            printBracket(type)
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
    global resultList
    global tabs
    string = '\n'
    string = string + printBracket("assign")
    tabs = ''
    currentTab = currentTab if string != '\n' else currentTab + 1
    string = string + printCurrentTab()
    string = string + mass[0] + "=" + expression_processing(mass[1]) + ";"
    mass[0] = None
    mass[1] = None
    string123 = counterTab("assign")[1]
    resultList.remove(string123)
    return string


def argg(mass):
    string = ["("]

    for arg in mass:
        string.append(expression_processing(arg))
        string.append(', ')
    if len(string) > 1:
        string.pop()
    string.append(') {')
    mass = None

    return ''.join(string)


def callFunc(mass):
    string = mass.type.split()[2]
    string = string + argg(mass.parts[0].parts)
    mass.parts[0] = None
    string = string[:-2]
    return string


def insertType(type, parts):
    string = None
    global currentTab
    global assinc
    global flag
    global mass1
    global tabs
    if str(type) == 'while' or type == 'WHILE':
        string = '\n'
        string = string + printBracket(type)
        tabs = ''
        currentTab = currentTab if mass1[len(mass1) - 1] != 'funcbody' else currentTab + 1
        string = string + printCurrentTab()
        string = string + "while " + ifWhile(parts[0]) + " {"
        flag = 0
        saveTab(type, currentTab)
        assinc = False
        parts[0] = None
    if str(type) == 'if' or str(type) == 'IF':
        string = '\n'
        string = string + printBracket(type)
        tabs = ''
        currentTab = currentTab if mass1[len(mass1) - 1] != 'funcbody' else currentTab + 1
        string = string + printCurrentTab()
        string = string + "if " + ifWhile(parts[0]) + " {"
        flag = 0
        saveTab(type, currentTab)
        assinc = False
        parts[0] = None
    if str(type) == 'else' or str(type) == 'ELSE':
        string = '\n'
        string = string + printBracket(type)
        tabs = ''
        string = string + ' '
        string = string + "else {"
        saveTab(type, currentTab)
        assinc = False
    return string


def insertReturn(mass):
    global flag
    global currentTab
    global resultList
    global tabs
    string = '\n'
    string = string + printBracket("return")
    tabs = ''
    currentTab = currentTab if mass1[len(mass1) - 1] != 'funcbody' else currentTab + 1
    string = string if string != '\n' else ''
    string = string + '\n' + printCurrentTab()
    flag = 0
    string = string + 'return ' + expression_processing(mass[0]) + ";"
    mass[0] = None
    string123 = counterTab("return")[1]
    resultList.remove(string123)
    return string

def func(result):
    string = None
    global countTab
    global currentTab
    global assinc
    global flag
    global mass1
    global tabs
    string = '\n'
    string = string + printBracket(result.type)
    tabs = ''
    currentTab = currentTab if mass1[len(mass1) - 1] != 'funcbody' else currentTab + 1
    string = string + printCurrentTab()
    string = string + callFunc(result) + ";"
    flag = 0
    count, string123 = counterTab(result.type)
    resultList.remove(string123)
    assinc = False
    return string


def recurs(result):
    global countTab
    global currentTab
    global assinc
    if result.parts is not None and result.type is not None:
        res = insertType(result.type, result.parts)
        type = None if res is None else res
        if (str(result.type) == 'assign' or str(result.type) == 'ASSIGN') and type is None:
            type = assign(result.parts)

        if (str(result.type) == 'args' or str(result.type) == 'ARGS') and type is None:
            type = argg(result.parts)

        if ('call func' in str(result.type) or 'variable func' in str(result.type)) and type is None:
            type = func(result)

        if (str(result.type) == 'return' or str(result.type) == 'RETURN') and type is None:
            type = insertReturn(result.parts)
        if (str(result.type) == 'def' or str(result.type) == 'DEF') and type is None:
            endProg()
            currentTab = 0
            assinc = False

        mass1.append(type if type is not None else result.type)

        for i in result.parts:
            if i is not None and isinstance(i, Node):
                recurs(i)


def endProg():
    global prettyPrint
    while len(countTab) > 0:
        tabs = "\n"
        size = countTab.pop()[1]
        for rl in range(size):
            tabs = tabs + '\t'
        tabs = tabs + "}"
        prettyPrint += str(tabs)
        prettyPrint += ' '



def outputing(text):
    return build_tree(text)


def pretty_printing(result):
    global resultList
    global prettyPrint
    resultList = str(result).split('\n')
    mass1.clear()
    prettyPrint = ""
    recurs(result)
    for out in mass1:
        if str(out) != 'None' and str(out) != 'args' and str(out) != 'funcbody' and str(out) != 'body':
            prettyPrint += out
            prettyPrint += ' '

    endProg()
    return prettyPrint + '\n}'


# ----------------------------
def remove_brackets(term):  # удаление лишних скобок
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


def expression_processing(mass):
    global flag
    string = str(mass)
    if string.isdigit():
        return string
    string = '\n' + string + '\n'
    tabs = []
    symbols = []
    operations = deque()
    variables = deque()
    oper = deque()
    tmpOper = []
    number = 2
    functionTabs = 0
    func = ""
    fl = 0
    while string.count('\n') >= 2:
        match = re.search(r'\n(.*)\n', string)
        count = len(match.group(1)) - len(match.group(1).replace("\t", ""))
        symbol = match.group(1).replace("\t", "")
        if symbol.find(':') != -1:
            symbol = symbol.replace(":", "")
        if (count - functionTabs) != 2 and fl and not "args" in str(match):
            fl = 0;
            if "," in func:
                func = func[:-2]
            func += ")"
            symbols.append(str(number))
            tmpOper.append(str(number))
            variables.append(func)
            number += 1
        if "args" in str(match):
            fl = 1
        if (count - functionTabs) == 2 and fl == 1:
            func += symbol
            func += ", "
        tabs.append(str(count))
        if "call func" in str(match):
            functionTabs = count
            func = symbol.replace("call func ", "")
            func += "("
        if "variable func" in str(match):
            functionTabs = count
            func = symbol.replace("variable func ", "")
            func += "("
        if not fl and not "call func" in str(match) and not "variable func" in str(match):
            if symbol.isalnum():
                symbols.append(str(number))
                tmpOper.append(str(number))
                variables.append(symbol)
                number += 1
            else:
                if symbol == "&&":
                    symbols.append('*')
                    tmpOper.append('*')
                    oper.append('&&')
                elif symbol == "||":
                    symbols.append('+')
                    tmpOper.append('+')
                    oper.append('||')
                else:
                    symbols.append(symbol)
                    tmpOper.append(symbol)
                    oper.append(symbol)
        string = string[string.index(symbol) + 1:]
    if len(func) >=2:
        if func[-2] == ",":
            func = func[:-2]
            func += ")"
            symbols.append(str(number))
            tmpOper.append(str(number))
            variables.append(func)
            number += 1
    fl = 0
    brackets = 0
    result = ""
    for index in range(len(symbols)):
        if index == 0:
            if not symbols[index].isdigit():
                tabs[index] = str(int(tabs[index + 1]) - 1)
            else:
                if len(tabs) >= 2:
                    tabs[index] = tabs[index + 1]
        if not symbols[index].isdigit():
            if (int(tabs[index - 1]) - int(tabs[index])) > 1 and index != len(tabs) - 1 and index != 0:
                result += ")" * (int(tabs[index - 1]) - int(tabs[index]) - 1)
                brackets -= (int(tabs[index - 1]) - int(tabs[index]) - 1)
            if fl == 0:
                result += "("
                if symbols[index] == '--':
                    result += '--'
                brackets += 1
                operations.append(symbols[index])
            else:
                result += operations.pop()
                operations.append(symbols[index])
                result += "("
                if symbols[index] == '--':
                    result += '--'
                brackets += 1
                fl = 0
        else:
            if (int(tabs[index - 1]) - int(tabs[index])) > 1 and index != len(tabs) - 1 and index != 0:
                result += ")" * (int(tabs[index - 1]) - int(tabs[index]) - 1)
                brackets -= (int(tabs[index - 1]) - int(tabs[index]) - 1)
            if fl == 0:
                result += symbols[index]
                fl = 1
            else:
                result += operations.pop()
                result += symbols[index]
                result += ")"
                brackets -= 1
        if index == len(tabs) - 1 and index != 0:
            result += ")" * (int(tabs[index]) - int(tabs[0]) - 1)
            brackets -= (int(tabs[index]) - int(tabs[0]) - 1)
    while brackets > 0:
        result += ")"
        brackets -= 1
    for index in range(len(symbols)):
        if not symbols[index].isalnum():
            symbols[index] = oper.popleft()
    if flag == 0:
        expression = remove_brackets(result)
    else:
        expression = result
    while 1:
        if len(tmpOper) == 0:
            break
        expression = expression.replace(tmpOper.pop(0), symbols.pop(0), 1)
    for index in range(number - 1, 1, -1):
        tmp = variables.pop()
        if tmp == "--":
            expression = tmp + expression
        else:
            expression = expression.replace(str(index), tmp, 1)
    if variables:
        expression = variables.pop() + expression
    return expression


if __name__ == '__main__':
    if len(sys.argv) == 2:
        f = sys.argv[1]
        read_file = open(f, 'r')
        text = read_file.read()
        tree = outputing(text)

        write_file = open(f + '.out', 'w')
        write_file.write(str(tree))

        write_file = open(f + '.pp', 'w')
        write_file.write(pretty_printing(tree))
    else:
        print("No input file")
