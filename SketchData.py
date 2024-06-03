class SketchData():
	def __init__(self):
		self.name = None
		self.version = None
		self.baudrate = None
		self.adornedFunctions = {}

	def __str__(self):
		string = ""
		string+="name: "+self.name+"\n"
		string+="version: "+self.version+"\n"
		string+="baudrate: "+str(self.baudrate)+"\n"
		for key in self.adornedFunctions:
			string += key+"\n"
			for function in self.adornedFunctions[key]:
				string += str(function)+"\n"
		return string

class FunctionData():
	def __init__(self):
		self.name = None
		self.returnType = None
		self.args = []

	def __str__(self):
		args = [x.ctype+" "+x.name for x in self.args]
		argString = ", ".join(args)
		string = ""
		if not self.returnType == None:
			string += self.returnType
			string += " "
		string += self.name
		string += "("
		string += argString
		string += ")"
		return string


class FunctionArg():
	ctype = None
	ptype = None
	array = None
	length = None
	name =  None

	def __str__(self):
		string = str(ctype)
		string += "->"
		string += str(ptype)
		return string
