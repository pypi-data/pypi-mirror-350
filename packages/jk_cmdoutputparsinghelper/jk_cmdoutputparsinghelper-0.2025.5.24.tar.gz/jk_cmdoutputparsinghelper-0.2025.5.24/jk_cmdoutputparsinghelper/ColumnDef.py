


#
# This class specifies information about a column.
#
class ColumnDef(object):

	################################################################################################################################
	## Constructors
	################################################################################################################################

	#
	# Constructor method.
	#
	# @param		str name				(required) The name of the column.
	# @param		callable valueParser	(optional) A value parser.
	# @param		str typeName			(optional) The name of the type.
	#
	def __init__(self, name:str, valueParser = None, typeName = None):
		assert isinstance(name, str)
		if valueParser is not None:
			assert callable(valueParser)

		self.name = name
		self.valueParser = valueParser
		self.typeName = typeName
	#

	################################################################################################################################
	## Public Properties
	################################################################################################################################

	################################################################################################################################
	## Helper Methods
	################################################################################################################################

	################################################################################################################################
	## Public Methods
	################################################################################################################################

	def __str__(self):
		_typeName = None
		if self.typeName is not None:
			_typeName = self.typeName
		else:
			if isinstance(self.valueParser, type):
				_typeName = self.valueParser.__name__
			else:
				_typeName = "???"
		return self.name + ":" + _typeName
	#

	def __repr__(self):
		_typeName = None
		if self.typeName is not None:
			_typeName = self.typeName
		else:
			if isinstance(self.valueParser, type):
				_typeName = self.valueParser.__name__
			else:
				_typeName = "???"
		return self.name + ":" + _typeName
	#

#

