import ply.yacc as yacc

from lex import tokens


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


wrong_in_while = 0

def p_program(p):
    '''program : progbody func'''
    p[0] = Node('program', [p[1], p[2]])


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
    '''assign : ID ASS expression LINEND'''
    p[0] = Node('assign', [p[1], p[3]])


def p_funcall(p):
    '''funcall : ID LBR args RBR LINEND'''
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
    '''while : WHILE LBR condition RBR LFBR funcbody RFBR'''
    global wrong_in_while
    if p[3] != 0 and wrong_in_while != 1:
        p[0] = Node('while', [p[3], p[6]])
    if wrong_in_while == 1:
        wrong_in_while = 0

# condition describe
def p_condition_plus(p):
    '''condition : condition PLUS con'''
    if isinstance(p[1], int) and isinstance(p[3], int):
        p[0] = p[1] + p[3]
    else:
        p[0] = Node(p[2], [p[1], p[3]])


def p_condition_minus(p):
    '''condition : condition MINUS con'''
    if isinstance(p[1], int) and isinstance(p[3], int):
        p[0] = p[1] - p[3]
    elif p[1] == p[3]:
        global wrong_in_while
        wrong_in_while = 1
    else:
        p[0] = Node(p[2], [p[1], p[3]])


def p_condition_compar(p):
    '''condition : condition MOREQ condition
                  | condition LESEQ condition
                  | condition LT condition
                  | condition GT condition
                  | condition EQ condition
                  | condition NE condition'''
    p[0] = Node(p[2], [p[1], p[3]])

    global wrong_in_while
    if p[2] == '==':  # if denial in expression
        wrong_in_while = 2  # then in while processing it

    if p[2] != '==':
        if p[1] == p[3]:
            wrong_in_while = 1


def p_condition_bin(p):
    '''condition : condition DIS con'''
    if p[1] == 0 and p[3] == 0:
        p[0] = 0
    else:
        p[0] = Node(p[2], [p[1], p[3]])


def p_condition_con(p):
    '''condition : con'''
    p[0] = p[1]


def p_con_times(p):
    'con : con MUL confactor'
    if isinstance(p[1], int) and isinstance(p[3], int):
        p[0] = p[1] * p[3]
    elif p[1] == 0 or p[3] == 0:
        global wrong_in_while
        wrong_in_while = 1
    else:
        p[0] = Node(p[2], [p[1], p[3]])


def p_con_bin(p):
    'con : con CON confactor'
    if p[1] == 0 or p[3] == 0:
        p[0] = 0
    else:
        p[0] = Node(p[2], [p[1], p[3]])

def p_con_div(p):
    'con : con DIVIDE confactor'
    if isinstance(p[1], int) and isinstance(p[3], int):
        p[0] = p[1] / p[3]
    elif p[1] == 0:
        global wrong_in_while
        wrong_in_while = 1
    else:
        p[0] = Node(p[2], [p[1], p[3]])


def p_con_confactor(p):
    '''con : confactor'''
    p[0] = p[1]


def p_confactor_num(p):
    '''confactor : NUM
              | funcvar
              | ID'''
    p[0] = p[1]


def p_confactor_bin(p):
    'confactor : DEN condition'
    p[0] = Node(p[1], [p[2]])
    global wrong_in_while
    if wrong_in_while == 2:
        wrong_in_while = 1

def p_confactor_deg(p):
    'confactor : confactor DEG condition'
    if isinstance(p[1], int) and isinstance(p[3], int):
        p[0] = p[1] ** p[3]
    else:
        p[0] = Node(p[2], [p[1], p[3]])


def p_confactor_expr(p):
    'confactor : LBR condition RBR'
    p[0] = p[2]


    # end condition describe
def p_return(p):
    '''return : RETURN expression LINEND'''
    p[0] = Node('return', [p[2]])


def p_expression_plus(p):
    '''expression : expression PLUS term'''
    p[0] = Node(p[2], [p[1], p[3]])


def p_expression_minus(p):
    '''expression : expression MINUS term'''
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
    'term : term MUL factor'
    p[0] = Node(p[2], [p[1], p[3]])


def p_term_bin(p):
    'term : term CON factor'
    p[0] = Node(p[2], [p[1], p[3]])


def p_term_div(p):
    'term : term DIVIDE factor'
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


def p_factor_deg(p):
    'factor : factor DEG expression'
    p[0] = Node(p[2], [p[1], p[3]])


def p_factor_expr(p):
    'factor : LBR expression RBR'
    p[0] = p[2]


def p_error(p):
    print("parser ")
    print("Unexpected token:", p)
    raise SystemExit(1)


parser = yacc.yacc()


def build_tree(text):
    return parser.parse(text)


def outputing(text):
    result = build_tree(text)
   # print('------res----------')
    #print(result)
    #print('------res----------')
    result = str(result)
    global wrong_in_while
    wrong_in_while = 0
    return result