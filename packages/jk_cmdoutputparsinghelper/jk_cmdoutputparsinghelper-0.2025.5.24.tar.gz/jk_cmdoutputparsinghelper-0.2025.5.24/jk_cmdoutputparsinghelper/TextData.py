


import typing

from .LineList import LineList
from .CharMatrix import CharMatrix







#
# This class represents text. It converts text automatically to a LineList or to string as required.
# So if you access the stored data via <c>text</c> you will receive the text content as a single string.
# If you access the stored data via <c>lines</c> you will receive the text content as a set of text lines.
# Conversion occurs automatically depending on which property you use.
#
# This mechanism provided by this class
# allows you to work efficiently with text data as a string or a string list, depending on the current
# requirements, while avoiding unnecessary intermediate conversions.
#
class TextData(object):

	################################################################################################################################
	## Constructor
	################################################################################################################################

	#
	# Constructor method.
	#
	def __init__(self, data:typing.Union[str,tuple,list,LineList]):
		self.__bStoringLines = False
		self.__data = ""
		if isinstance(data, str):
			self.text = data
		else:
			self.lines = data
	#

	################################################################################################################################
	## Public Properties
	################################################################################################################################

	@property
	def lines(self) -> LineList:
		if not self.__bStoringLines:
			# convert to lines
			if self.__data:
				self.__data = LineList(self.__data.split("\n"))
			else:
				self.__data = LineList()
			self.__bStoringLines = True
		return self.__data
	#

	@lines.setter
	def lines(self, value:typing.Union[tuple,list,LineList]):
		assert isinstance(value, (tuple, list, LineList))
		for x in value:
			assert isinstance(x, str)

		if isinstance(value, LineList):
			self.__data = value
		else:
			self.__data = LineList(value)
		self.__bStoringLines = True
	#

	@property
	def text(self) -> str:
		if self.__bStoringLines:
			# convert to text
			self.__data = "\n".join(self.__data)
			self.__bStoringLines = False
		return self.__data
	#

	@text.setter
	def text(self, value:str):
		assert isinstance(value, str)
		self.__data = value
		self.__bStoringLines = False
	#

	################################################################################################################################
	## Helper Methods
	################################################################################################################################

	################################################################################################################################
	## Public Methods
	################################################################################################################################

	def __str__(self):
		if self.__bStoringLines:
			return "\n".join(self.__data)
		else:
			return self.__data
	#

	def __repr__(self):
		if self.__bStoringLines:
			return repr("\n".join(self.__data))
		else:
			return repr(self.__data)
	#

	def toCharMatrix(self) -> CharMatrix:
		ret = CharMatrix()
		for line in self.__data.split("\n"):
			ret.addRow(line)
		return ret
	#

#










