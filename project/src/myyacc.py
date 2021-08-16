from mylexer import MyLexer
from ply import yacc

####################################################################

start = 'declaration_function'

####################################################################

def p_declaration_function(p):
	"""declaration_function : function
							| declaration_function function"""
	if len(p) == 3:
		p[0] = p[1] + [p[2]]
	else:
		p[0] = [p[1]]

####################################################################

def p_func(p):
	"""function : type ID LPAR paramlist RPAR LBRA stmtlist RBRA
				| type ID LPAR RPAR LBRA stmtlist RBRA"""
	if len(p) == 9:
		params = p[4]
		stmts = p[7]
		end = 8
	else:
		params = ['void']
		stmts = p[6]
		end = 7

	p[0] = {
		'identity': 'function',
		'return type': p[1],
		'symbol': p[2],
		'params': params,
		'stmts': stmts,
		'line info': (p.lineno(1), p.lineno(end))
	}

####################################################################

def p_type(p):
	"""type : INT
			| FLOAT
			| type STAR"""
	if len(p) == 2:
		p[0] = p[1]
	else:
		p[0] = p[1] + p[2]

def p_paramlist(p):
	"""paramlist : param
				 | param COMMA paramlist"""
	if len(p) == 4:
		if p[1] == "void":
			p_error(p)
		else:
			p[0] = [p[1]] + p[3]
	else:
		p[0] = [p[1]]


def p_param(p):
	"""param : VOID
			 | type ID"""
	if len(p) == 3:
		p[0] = { 'identity': 'param',
				 'param type': p[1],
				 'symbol': p[2]
		}
	elif len(p) == 2:
		p[0] = { 'identity': 'param',
				 'param type': p[1]
		}
	else:
		p_error(p)

####################################################################

def p_stmtlist(p):
	"""stmtlist : stmt
				| stmt stmtlist"""
	if len(p) == 3:
		p[0] = [p[1]] + p[2]
	else:
		p[0] = [p[1]]

def p_stmt(p):
	"""stmt : return SEMICOLON
			| var_declaration SEMICOLON
			| var_assign SEMICOLON
			| incre
			| if
			| forloop
			| funccall SEMICOLON"""
	p[0] = { 'identity': 'stmt',
			 'content': p[1]
	}

####################################################################

def p_return(p):
	"""return : RETURN
			  | RETURN arithexp"""
	if len(p) == 2:
		p[0] = { 'identity': 'return',
				 'line info': (p.lineno(1), p.lineno(1))
		}
	else:
		p[0] = { 'identity': 'return',
				 'return value': p[2],
				 'line info': (p.lineno(1), p.lineno(2))
		}


def p_forloop(p):
	'forloop : FOR LPAR id ASSIGN arithexp SEMICOLON id cmp arithexp SEMICOLON incre RPAR LBRA stmtlist RBRA'
	p[0] = { 'identity': 'forloop',
			 'assign': (p[3], p[5]),
			 'condition': (p[7], p[8], p[9]),
			 'incre': p[11],
			 'stmts': p[14],
			 'line info': (p.lineno(1), p.lineno(15))
	}


def p_if(p):
	'if : IF LPAR arithexp cmp arithexp RPAR LBRA stmtlist RBRA'
	p[0] = { 'identity': 'if',
			 'condition': (p[3], p[4], p[5]),
			 'stmts': p[8],
			 'line info': (p.lineno(1), p.lineno(9))
	}

def p_cmp(p):
	"""cmp : LGREATER
		   | RGREATER
		   | EQUAL
		   | NOTEQUAL
		   | RGREQUAL
		   | LGREQUAL"""
	p[0] = p[1]


def p_funccall(p):
	"""funccall : ID LPAR arglist RPAR
				| ID LPAR RPAR"""
	if len(p) == 5:
		args = p[3]
		end = 4
	else:
		args = None
		end = 3
	p[0] = { 'identity': 'function call',
			 'function symbol': p[1],
			 'args': args,
			 'line info': (p.lineno(1), p.lineno(end))
	}


def p_arglist(p):
	"""arglist : arg
			   | arg COMMA arglist"""
	if len(p) == 2:
		p[0] = [p[1]]
	else:
		p[0] = [p[1]] + p[3]


def p_arg(p):
	"""arg : arithexp
		   | string"""
	p[0] = p[1]

def p_string(p):
	'string : STRING'
	p[0] = { 'identity': 'string',
			 'content': p[1][1:-1],
			 'line info': (p.lineno(1), p.lineno(1))
	}

def p_var_declaration(p):
	"""var_declaration : type varlist"""
	if len(p) == 3:
		p[0] = { 'identity': 'declare var',
				 'var type': p[1],
				 'vars': p[2],
				 'line info': (p.lineno(1), p.lineno(2))
		}


def p_varlist(p):
	"""varlist : id
			   | id COMMA varlist"""
	if len(p) == 4:
		p[0] = [p[1]] + p[3]
	else:
		p[0] = [p[1]]


def p_var_assign(p):
	'var_assign : id ASSIGN arithexp'
	p[0] = { 'identity': 'assign',
			 'var symbol': p[1],
			 'expr': 'arithexp',
			 'line info': (p.lineno(1), p.lineno(3))
	}

def p_arithexp(p):
	"""arithexp : LPAR arithexp RPAR
				| term arithexptail
				| term"""
	if len(p) == 2:
		p[0] = p[1]
	elif len(p) == 3:
		p[0] = [p[2][0], p[1], p[2][1]]
	else:
		p[0] = p[2]


def p_arithexptail(p):
	"""arithexptail : PLUS term arithexptail
					| PLUS term
					| MINUS term arithexptail
					| MINUS term"""
	if len(p) == 3:
		p[0] = [p[1], p[2]]
	else:
		p[0] = [p[1], [p[3][0], p[2], p[3][1]]]


def p_term(p):
	"""term : factor termtail
			| factor"""
	if len(p) == 2:
		p[0] = p[1]
	else:
		p[0] = [p[2][0], p[1], p[2][1]]



def p_termtail(p):
	"""termtail : STAR factor termtail
				| STAR factor
				| DIVIDE factor termtail
				| DIVIDE factor"""
	if len(p) == 3:
		p[0] = [p[1], p[2]]
	else:
		p[0] = [p[1], [p[3][0], p[2], p[3][1]]]

def p_factor_num(p):
	"""factor : NUMBER
			  | PLUS NUMBER
			  | MINUS NUMBER
			  | incre"""
	if len(p) == 2:
		p[0] = { 'identity': 'number',
				 'content': p[1],
				 'line info': (p.lineno(1), p.lineno(1))
		}
	elif p[1].isdigit():
		p[0] = { 'identity': 'number',
				 'content': p[1] + p[2],
				 'line info': (p.lineno(1), p.lineno(3))
		}
	else:
		p[0] = p[1]


def p_incre(p):
	"""incre : INCREMENT id
			 | id INCREMENT"""

	if p[1] == '++':
		symbol = p[2]
	else:
		symbol = p[1]

	p[0] = { 'identity': 'incre',
			 'symbol': symbol,
			 'isPreFix': (p[1] == '++'),
			 'line info': (p.lineno(1), p.lineno(2))
	}


def p_factor_notnum(p):
	"""factor : id
			  | funccall"""
	p[0] = p[1]


def p_id(p):
	"""id : ID
		  | ID LBRAC arithexp RBRAC"""
	if len(p) == 5:
		identity = 'array'
		index = p[3]
		end = 4
	else:
		identity = 'id'
		index = None
		end = 1
	p[0] = { 'identity': identity,
			 'symbol': p[1],
			 'index': index,
			 'line info': (p.lineno(1), p.lineno(end))
	}

####################################################################

def p_error(p):
	print("Syntax error : line", p.lineno)
	exit()

####################################################################

mylexer = MyLexer()
lexer = mylexer.build()
tokens = mylexer.tokens
parser = yacc.yacc()