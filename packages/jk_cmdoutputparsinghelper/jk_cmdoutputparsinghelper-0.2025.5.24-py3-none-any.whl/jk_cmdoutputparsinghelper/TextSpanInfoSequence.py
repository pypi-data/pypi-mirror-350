

import typing

import jk_typing
import jk_prettyprintobj

from .TextSpanInfo import TextSpanInfo





#
# This class represents space/non-space information about a sequence of characters boolean values.
#
class TextSpanInfoSequence(jk_prettyprintobj.DumpMixin):

	################################################################################################################################
	## Constructor
	################################################################################################################################

	#
	# Constructor method.
	#
	@jk_typing.checkFunctionSignature()
	def __init__(self,
			values:typing.Iterable[TextSpanInfo],
		):

		if isinstance(values, list):
			self.values = values
		else:
			self.values = list(values)
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

	def __iter__(self):
		yield from self.values
	#

	def __len__(self):
		return len(self.values)
	#

	def __str__(self) -> str:
		return "TextSpanInfoSequence<( {} )>".format(self.values)
	#

	def __repr__(self) -> str:
		return self.__str__()
	#

	def thinoutSpaceSegments(self, minLength:int):				# -> TextSpanInfoSequence
		ret = list(self.values)

		# set unwanted spaces to non-spaces

		for i in range(0, len(ret)):
			c = ret[i]
			if c.bIsSpace:
				if c.length < minLength:
					ret[i] = TextSpanInfo(False, c.pos, c.length)

		# now aggregate

		i = 0
		while i < len(ret) - 1:
			cur = ret[i]
			next = ret[i+1]
			if cur.bIsNonSpace and next.bIsNonSpace:
				# merge
				cur = TextSpanInfo(False, cur.pos, cur.length + next.length)
				ret[i] = cur
				del ret[i+1]
			else:
				i += 1

		return TextSpanInfoSequence(ret)
	#

	def extractOnlyNonSpaceSegments(self):				# -> TextSpanInfoSequence
		ret = []

		for c in self.values:
			if not c.bIsSpace:
				ret.append(c)

		return TextSpanInfoSequence(ret)
	#

	def mergeColumns(self, colNo1:int, colNo2:int):
		assert isinstance(colNo1, int)
		assert isinstance(colNo2, int)
		assert colNo1 >= 0
		assert colNo2 == colNo1+1

		col1 = self.values[colNo1]
		col2 = self.values[colNo2]
		newCol = TextSpanInfo(col1.bIsSpace, col1.pos, col1.length + col2.length)
		del self.values[colNo2]
		self.values[colNo1] = newCol
	#

	#
	# If you calculate the columns on the title column alone the last span will only span to the end of the title column,
	# Maybe this is too short. In that case call this method to enlarge the last span until it spans the desired maximum
	# line length you want it to span.
	#
	def expandWidthTo(self, maxLen:int):
		assert isinstance(maxLen, int)
		assert maxLen >= 0

		_lsp = self.values[-1]
		assert maxLen >= _lsp.pos + _lsp.length
		_lsp.length = maxLen - _lsp.pos
	#

	def __getitem__(self, ii:int) -> TextSpanInfo:
		return self.values[ii]
	#

	def __setitem__(self, ii:int, value:TextSpanInfo) -> None:
		assert isinstance(value, TextSpanInfo)
		self.values[ii] = value
	#

	def _dumpVarNames(self) -> typing.List[str]:
		return [
			"values",
		]
	#

#







