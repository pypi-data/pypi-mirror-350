




#
# This class represents space/non-space information about a sequence of characters boolean values.
#
class TextSpanInfo(object):

	################################################################################################################################
	## Constructor
	################################################################################################################################

	#
	# Constructor method.
	#
	def __init__(self,
			bIsSpace:bool,
			pos:int,
			length:int,
		):

		assert isinstance(bIsSpace, bool)
		assert isinstance(pos, int)
		assert isinstance(length, int)
		assert length > 0
		
		self.bIsSpace = bIsSpace
		self.pos = pos
		self.length = length
	#

	################################################################################################################################
	## Public Properties
	################################################################################################################################

	@property
	def bIsNonSpace(self) -> bool:
		return not self.bIsSpace
	#

	################################################################################################################################
	## Helper Methods
	################################################################################################################################

	################################################################################################################################
	## Public Methods
	################################################################################################################################

	def __str__(self) -> str:
		return "TextSpanInfo<( {}, pos={}, len={} )>".format(
			"space" if self.bIsSpace else "non-space",
			self.pos,
			self.length
		)
	#

	def __repr__(self) -> str:
		return self.__str__()
	#

#







