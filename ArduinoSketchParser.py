#!/usr/bin/python3
import re
from TypeMapping import TypeMapping
from SketchData import *

class ArduinoSketchParser():
	adornmentPattern = "^\/\/\[(.*?)\]"
	baudRatePattern = "^Serial.begin\((.*?)\);"
	nameVersionPattern = "^Serial.println\(\"(.*?) (.*?)\"\);"
	functionPattern = "^[a-zA-Z0-9]+ [a-zA-Z0-9_]+\((.*?)\)"
	adornedFunctions = {}

	def __init__(self, target):
		self.target = target

	def parse(self):
		sketchData = SketchData()
		currentFunction = None
		with open (self.target) as file:
			lines = file.readlines()
			for i in range(0,len(lines)):
				line = lines[i].strip()
				if self.checkFunctionPattern(line):
					functionData = self.extractFunctionData(line)
					currentFunction = functionData
					lastLine = lines[i-1]
					if self.checkAdornment(lastLine):
						adornmentKeys = self.parseAdornment(lastLine)
						for key in adornmentKeys:
							if not key in sketchData.adornedFunctions:
								sketchData.adornedFunctions[key] = []
							sketchData.adornedFunctions[key].append(functionData)

				if currentFunction!=None and currentFunction.name == "setup":
					if self.checkBaudRate(line):
						sketchData.baudrate = self.extractBaudRate(line)
					elif self.checkNameVersionPattern(line):
						sketchData.name, sketchData.version = self.extractNameVersion(line)

		return sketchData

	def checkFunctionPattern(self, line):
		if re.match(self.functionPattern, line):
			return True
		return False

	def checkNameVersionPattern(self, line):
		if re.match(self.nameVersionPattern, line):
			return True
		return False

	def checkAdornment(self, line):
		if re.match(self.adornmentPattern, line):
			return True
		return False

	def checkBaudRate(self, line):
		if re.match(self.baudRatePattern, line):
			return True
		return False

	def parseAdornment(self, line):
		line = line.replace('[','')
		line = line.replace(']','')
		line = line.replace('/','')
		adornmentKeys = line.split(",")
		adornmentKeys = [x.strip() for x in adornmentKeys]
		return adornmentKeys

	def extractBaudRate(self, line):
		baudRate = line.split('(')[1].split(")")[0]
		baudRate = int(baudRate)
		return baudRate

	def extractNameVersion(self, line):
		args = line.split('"')[1]
		args = args.split(" ")
		name = args[0]
		version = args[1]
		return name, version

	def extractFunctionData(self, fstring):
		fdata = FunctionData()
		fdata.name = fstring.split(" ")[1].split("(")[0]
		returnCType = fstring.split(" ")[0]
		if TypeMapping.validateType(returnCType):
			fdata.returnCType = returnCType
			fdata.returnPType = TypeMapping.types[returnCType]
		args = fstring.split("(")[1].split(")")[0].split(",")
		args = [x.strip() for x in args]
		for arg in args:
			argVals = arg.split(" ")
			if len(argVals) < 2:
				break
			type = arg.split(" ")[0].strip()
			name = arg.split(" ")[1].strip()
			array, length, name = self.checkVariableName(name)
			if TypeMapping.validateType(type):
				farg = FunctionArg()
				farg.name = name
				farg.ctype = type
				farg.ptype = TypeMapping.types[type]
				farg.array = array
				farg.length = length
				fdata.args.append(farg)
		return fdata

	def checkVariableName(self, variableName):
		array = False
		length = None

		if "[" in variableName and "]" in variableName:
			array = True
			length = variableName.split("[")[1]
			length = length.split("]")[0]
			variableName = variableName.replace("["+length+"]", "")
			if length == "":
				length = None
		return array, length, variableName




if __name__ == "__main__":
	asp = ArduinoSketchParser('Firmware.c')
