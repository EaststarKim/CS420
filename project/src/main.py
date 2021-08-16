from myyacc import parser, lexer

#--------------------------------------------
# CONSTANTS
#--------------------------------------------

#directory
input_file_dir = '../inputs/input3.c'

#--------------------------------------------
# END OF CONSTANTS
#--------------------------------------------

def printTree(doc, pre = ''):
	if type(doc) is list:
		for component in doc:
			if type(component) is list:
				print('{}['.format(pre))
				printTree(component, pre+'    ')
				print('{}]'.format(pre))
			elif type(component) is dict:
				print('{}{}'.format(pre, '{'))
				printTree(component, pre+'    ')
				print('{}{}'.format(pre, '}'))
			else:
				print('{}{},'.format(pre, component))
	else:
		for key in doc:
			component = doc[key]
			if type(component) is list:
				print('{}{}: ['.format(pre, key))
				printTree(component, pre+'    ')
				print('{}]'.format(pre))
			elif type(component) is dict:
				print('{}{}: {}'.format(pre, key, '{'))
				printTree(component, pre+'    ')
				print('{}{}'.format(pre, '}'))
			else:
				print('{}{}: {},'.format(pre, key, component))
			


def main():
	print('Opening files. . .')
	file = open(input_file_dir, 'r')
	lines = file.readlines()
	txt = " ".join(lines)

	print('Parsing. . .')
	result = parser.parse(txt, lexer=lexer)

	print('Total {} functions...'.format(len(result)))
	printTree(result)
	#printTree({'a': 1, 'b': 'B', 'c': {1:'10', 2:'23ab', 3:'asdf'}})
	#printTree([1, 'B', ['10', '23ab', 'asdf']])

	print('Done.')

	

if __name__ == '__main__':
	main()