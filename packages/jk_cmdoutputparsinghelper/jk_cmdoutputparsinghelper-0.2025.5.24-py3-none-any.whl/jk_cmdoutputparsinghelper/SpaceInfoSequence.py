

import typing

import jk_typing

from .TextSpanInfo import TextSpanInfo
from .TextSpanInfoSequence import TextSpanInfoSequence






#
# This class represents space/non-space information about a sequence of characters boolean values.
#
class SpaceInfoSequence(object):

	################################################################################################################################
	## Constructor
	################################################################################################################################

	#
	# Constructor method.
	#
	@jk_typing.checkFunctionSignature()
	def __init__(self,
			values:typing.Iterable[bool],
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
		return "SpaceInfoSequence<( {} )>".format(self.values)
	#

	def __repr__(self) -> str:
		return self.__repr__()
	#

	#
	# Converts a sequence of boolens to TextSpanInfo objects.
	#
	def compact(self) -> TextSpanInfoSequence:
		ret:typing.List[TextSpanInfo] = []

		_currentValue = None
		_temp = []
		pos = 0
		for b in self.values:
			if _currentValue != b:
				if _temp:
					ret.append(TextSpanInfo(_currentValue, pos-len(_temp), len(_temp)))
				_currentValue = b
				_temp = []
			_temp.append(b)
			pos += 1

		if _temp:
			ret.append(TextSpanInfo(_currentValue, pos-len(_temp), len(_temp)))

		return TextSpanInfoSequence(ret)
	#

#







