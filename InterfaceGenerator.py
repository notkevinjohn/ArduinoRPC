class InterfaceGenerator():
	key = 'callable'
	def __init__(self, sketchData):
		print (sketchData)
		for key in sketchData.adornedFunctions:
			if key == self.key:
				print (key, sketchData.adornedFunctions[key])


	def writeFile(self, fileName):
		pass
