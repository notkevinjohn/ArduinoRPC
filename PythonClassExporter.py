#!/usr/bin/python3
from TypeMapping import TypeMapping

class PythonClassExporter():
	adornmentKey = "callable"
	indentation = "\t"

	def __init__(self, sketchData, device):
		self.sketchData = sketchData
		self.filename = sketchData.name+".py"
		self.device = device
		self.clearFile()
		self.writeImports()
		self.writeClassDefinition(sketchData.name)
		self.writeConstructor(device, sketchData.baudrate, sketchData.name, sketchData.version)
		self.writeAdornedFunctions()
		self.writePOECode()

	def clearFile(self):
		with open(self.filename, "w+") as file:
			file.write("")

	def writeImports(self):
		lines = []
		lines.append('from SerialManager import SerialManager')
		self.writeIndentedCode(lines,0)

	def writeClassDefinition(self, classname):
		lines = []
		lines.append("class "+classname+"():")
		self.writeIndentedCode(lines,0)

	def writeConstructor(self, device, baudrate, firmware, version):
		lines = []
		lines.append("def __init__(self):")
		lines.append(self.indentation+'self.serialManager = SerialManager('+str(baudrate)+',"'+str(device)+'","'+str(firmware)+'","'+str(version)+'")')
		lines.append(self.indentation+'self.serialManager.connect()')
		self.writeIndentedCode(lines, 1)

	def writePOECode(self):
		lines = []
		lines.append('if __name__ == "__main__":')
		lines.append(self.indentation+self.sketchData.name.lower()+"="+self.sketchData.name+"()")
		self.writeIndentedCode(lines,0)

	def writeAdornedFunctions(self):
		lines = []
		for function in self.sketchData.adornedFunctions[self.adornmentKey]:
			lines.append(self.writeFunctionHeader(function))
			lines.append(self.indentation+"self.serialManager.sendCommand("+str(bytes(1))+")")
		self.writeIndentedCode(lines, 1)

	def writeFunctionHeader(self, function):
		header = "def "
		header += function.name
		header += "("
		pargs = ['self']
		for arg in function.args:
			pargs.append(arg.name+' : '+arg.ptype)
		header+=", ".join(pargs)
		header += "):"
		header += " -> "
		header += function.returnPType
		return header


	def writeIndentedCode(self, lines, indentation):
		with open(self.filename, "a+") as file:
			for line in lines:
				for i in range(0, indentation):
					line = self.indentation+line
				file.write(line+'\n')
			file.write("\n")
