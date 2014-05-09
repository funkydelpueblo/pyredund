import os
import ast


class ModuleHolder(ast.AST):

	def __init__(self):
		ast.AST.__init__(self)
		self.body = []
		self.names = []
		self._fields = ('body', 'names')

	def addModule(self, module):
		self.body.append(module)

	def addName(self, name):
		self.names.append(name)

def all_files(directory):
    for path, dirs, files in os.walk(directory):
        for f in files:
            yield os.path.join(path, f)

def master_ast(directory):
	py = [f for f in all_files(directory) if f.endswith('.py')]

	asts = list()

	for f in py:
		reader = open(f, 'r')
		text = ast.parse(reader.read())
		reader.close()
		asts.append((f, text))

	MH = ModuleHolder()
	for a in asts:
		#print a._fields
		MH.addModule(a[1])
		MH.addName(a[0])


	#print ast.dump(MH)

	return MH

#your_directory = raw_input("What directory? ")
#py = [f for f in all_files(your_directory)
#               if f.endswith('.py')]

#for f in py:
#	print f

#your_directory = "tests/tweepy-master"

#allfiles = master_ast(your_directory)
#for f in allfiles:
#	print f
