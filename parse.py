import ply.yacc as yacc 

from lex import tokens 

def p_expression_plus(p): 
    'expression : expression PLUS term'
    p[0] = p[1] + p[3]

def p_expression_minus(p):
    'expression : expression SUB term'
    p[0] = p[1] - p[3]

def p_expression_term(p): 
    'expression : term' 
    p[0] = p[1]

def p_term_times(p): 
    'term : term MULT factor'
    p[0] = p[1] * p[3]

def p_term_div(p):
    'term : term DIV factor'
    p[0] = p[1] / p[3]

def p_term_factor(p): 
    'term : factor' 
    p[0] = p[1] 

def p_factor_num(p): 
    'factor : NUM'
    p[0] = p[1]

def p_term_pow(p):
    'term : term POW factor'
    p[0] = pow(p[1], p[3])

def p_factor_expr(p): 
    'factor : LBR expression RBR'
    p[0] = p[2]

def p_error(p): 
    print("Syntax error")

parser = yacc.yacc()
read_file = open('input.txt.out', 'r')
text = read_file.read()

while True: 
    try: 
        s = text
    except EOFError: 
        break
    if not s: 
        continue
    result=parser.parse(s)
    write_file = open('input.txt.out', 'w')
    write_file.write("result = " + text + " = " + str(result))
    print(result)
    break