class TypeMapping:
	types = {
		'bool':'bool',
		'void': 'null',
		'char':'str',
		'int':'int'
	}

	@staticmethod
	def validateType(type):
		if not type in TypeMapping.types:
			return False
		return True

