

import os
import typing
import collections

import jk_typing
import jk_prettyprintobj

from .ColumnDef import ColumnDef
from .Table import Table
from .TextSpanInfo import TextSpanInfo
from .TextSpanInfoSequence import TextSpanInfoSequence
from .SpaceInfoSequence import SpaceInfoSequence








ColumnPositionInfo = collections.namedtuple("ColumnPositionInfo", [
	"pos", "length"
])





CharMatrix = typing.NewType("CharMatrix", object)

class CharMatrix(jk_prettyprintobj.DumpMixin):

	class _Row(jk_prettyprintobj.DumpMixin):

		def __init__(self, text:str, chars:typing.List[str]) -> None:
			self.text = text
			self.chars = chars
		#

		def _dumpVarNames(self) -> typing.List[str]:
			return [
				"text",
				"chars",
			]
		#

		def expand(self, width:int):
			currentLen = len(self.text)
			if width > currentLen:
				nRequired = width - currentLen
				self.text += " " * nRequired
				for i in range(0, nRequired):
					self.chars.append(" ")
		#

	#

	################################################################################################################################
	## Constructor
	################################################################################################################################

	#
	# Constructor method.
	#
	@jk_typing.checkFunctionSignature()
	def __init__(self,
		):

		self.__width:int = 0
		self.__rows:typing.List[CharMatrix._Row] = []
	#

	################################################################################################################################
	## Public Properties
	################################################################################################################################

	@property
	def width(self) -> int:
		return self.__width
	#

	@property
	def height(self) -> int:
		return len(self.__rows)
	#

	################################################################################################################################
	## Helper Methods
	################################################################################################################################

	def _dump(self, ctx:jk_prettyprintobj.DumpCtx):
		ctx.dumpVar("width", self.width)
		ctx.dumpVar("height", self.height)
		ctx.dumpVar("__rows", self.__rows)
	#

	################################################################################################################################
	## Public Methods
	################################################################################################################################

	def addRow(self, line:str):
		assert isinstance(line, str)

		w = len(line)
		currentRow = CharMatrix._Row(line, list(line))
		currentRow.expand(self.__width)
		self.__rows.append(currentRow)

		# now fill the rows to match the maximum length
		if w > self.__width:
			self.__width = w
			for row in self.__rows:
				row.expand(w)
	#

	def addRows(self, lines:typing.Union[typing.List[str],typing.Tuple[str]]):
		assert isinstance(lines, (list,tuple))

		for line in lines:
			self.addRow(line)
	#

	def clear(self):
		self.__width = 0
		self.__rows.clear()
	#

	#
	# Check if the specified column is a vertical space column (= all characters at position <i>pos</i> are spaces)
	#
	def isSpaceColumn(self, x:int) -> bool:
		if (x < 0) or (x >= self.__width):
			raise Exception("Column index out of bounds: {}".format(x))

		for row in self.__rows:
			if not row.chars[x].isspace():
				return False
		return True
	#

	def isEmptyRow(self) -> bool:
		for row in self.__rows:
			if not row.text.isspace():
				return False
		return True
	#

	#
	# @return		CharMatrix			Retuns a character matrix.
	#
	def extractColumn(self, colPos:ColumnPositionInfo, bIgnoreFirstLine:bool = False) -> CharMatrix:
		assert isinstance(colPos, ColumnPositionInfo)
		assert isinstance(bIgnoreFirstLine, bool)

		nFrom = colPos.pos
		nLen = colPos.length
		if (nFrom < 0) or (nLen <= 0):
			raise Exception("Invalid values specified!")
		nTo = colPos.pos + colPos.length

		ret = CharMatrix()
		for row in self.__rows:
			if bIgnoreFirstLine:
				bIgnoreFirstLine = False
				continue
			ret.__rows.append(CharMatrix._Row(row.text[nFrom:nTo], row.chars[nFrom:nTo]))
			ret.__width = nLen

		return ret
	#

	#
	# @return		CharMatrix[]		Retuns a list of character matrices.
	#
	def extractColumns(self, spanInfos:TextSpanInfoSequence, bIgnoreFirstLine:bool = False) -> typing.List[CharMatrix]:
		ret = []
		for spanInfo in spanInfos:
			ret.append(self.extractColumn(
				ColumnPositionInfo(spanInfo.pos, spanInfo.length),
				bIgnoreFirstLine,
			))
		return ret

	def getRowText(self, n:int, bTrimLeft:bool = True, bTrimRight:bool = True) -> str:
		assert isinstance(n, int)
		assert isinstance(bTrimLeft, bool)
		assert isinstance(bTrimRight, bool)

		# ----

		row = self.__rows[n]

		s = row.text
		if bTrimLeft:
			s = s.lstrip()
		if bTrimRight:
			s = s.rstrip()

		return s
	#

	def deleteRow(self, n:int) -> None:
		assert isinstance(n, int)

		# ----

		del self.__rows[n]
	#

	#
	# Convert all rows in this matrix to values.
	#
	def rowsToValues(self, bTrimLeft:bool = True, bTrimRight:bool = True, bIgnoreFirstLine:bool = False, parserFunction = None) -> list:
		assert isinstance(bTrimLeft, bool)
		assert isinstance(bTrimRight, bool)
		assert isinstance(bIgnoreFirstLine, bool)
		if parserFunction is not None:
			assert callable(parserFunction)

		# ----

		ret = []

		for row in self.__rows:
			s = row.text
			if bIgnoreFirstLine:
				bIgnoreFirstLine = False
				continue

			if bTrimRight:
				s = s.rstrip()
			if bTrimLeft:
				s = s.lstrip()

			if parserFunction is not None:
				s = parserFunction(s)

			ret.append(s)

		return ret
	#

	def identifyAllSpaceColumns(self) -> SpaceInfoSequence:
		ret = []
		for i in range(0, self.__width):
			ret.append(self.isSpaceColumn(i))
		return SpaceInfoSequence(ret)
	#

	#
	# For every single row count the number of leading space characters. Put all these counts into a list (= one count for every row) and return this list.
	#
	# @return				int[]			Returns a list of counts that indicate how many leading space characters there are in each row.
	#
	def getLeadingSpaceCounts(self) -> typing.List[int]:
		counts = []

		for row in self.__rows:
			n = self.__width
			for ix in range(0, self.__width):
				if not row.chars[ix].isspace():
					n = ix
					break
			counts.append(n)

		return counts
	#

	#
	# @param	bool bSpanToNext		(optional) If <c>true<c> a span will automatically end where the next one starts.
	#									If <c>false</c> a span will end right after the last character of this column.
	#									(Default value: <c>false</code>)
	#
	def identifyTextColumnRanges(self, minGapLength:int = 1, bSpanToNext:bool = False) -> TextSpanInfoSequence:
		assert isinstance(minGapLength, int)
		assert minGapLength > 0

		# --------------------------------
		# get a sequence of booleans representing spaces and non-spaces

		columnSpaceFlags = self.identifyAllSpaceColumns()

		# --------------------------------
		# compact and filter the sequence

		compactedSpanInfos:TextSpanInfoSequence = columnSpaceFlags.compact()
		compactedSpanInfos = compactedSpanInfos.thinoutSpaceSegments(minGapLength)
		compactedSpanInfos = compactedSpanInfos.extractOnlyNonSpaceSegments()

		if bSpanToNext:
			for i in range(1, len(compactedSpanInfos.values)):
				cur = compactedSpanInfos.values[i]
				prev = compactedSpanInfos.values[i-1]
				prev.length = cur.pos - prev.pos

		# --------------------------------

		return compactedSpanInfos
	#

	#
	# This method modifies this line list *in place*. It removes all emtpy lines at the end of this line list.
	#
	def removeTrailingEmptyLines(self):
		while self.__rows and self.__rows[-1].text.isspace():
			del self.__rows[-1]
	#

	#
	# This method modifies this line list *in place*. It removes all emtpy lines at the beginning of this line list.
	#
	def removeLeadingEmptyLines(self):
		while self.__rows and self.__rows[0].text.isspace():
			del self[0]
	#

	#
	# This method creates a string table from this line list.
	# It splits the lines at the specified positions and returns an instance of <c>Table</c>
	# containing all data.
	#
	# @param		int[] positions					(required) The split positions
	# @param		bool bLStrip					(required) Perform an <c>lstrip()</c> on each line.
	# @param		bool bRStrip					(required) Perform an <c>rstrip()</c> on each line.
	# @param		bool bFirstLineIsHeader			(required) Specify <c>true</c> here if the first line contains header information.
	# @param		ColumnDef[] columnDefs			(required) A set of column definitions, one for each column.
	#
	def createDataTableFromColumns(self,
			spanInfos:TextSpanInfoSequence,
			bLStrip:bool,
			bRStrip:bool,
			bFirstLineIsHeader:bool,
			columnDefs:typing.List[ColumnDef] = None,
		) -> Table:

		assert isinstance(spanInfos, TextSpanInfoSequence)
		assert isinstance(bLStrip, bool)
		assert isinstance(bRStrip, bool)
		assert isinstance(bFirstLineIsHeader, bool)

		# create list of data matrices, extract the header titles, generate missing column definitions

		charMatrixList:typing.List[CharMatrix] = self.extractColumns(spanInfos)

		_headerTitles:typing.List[str] = None
		if bFirstLineIsHeader:
			_headerTitles = []
			for cm in charMatrixList:
				_headerTitles.append(cm.getRowText(0, True, True))
				cm.deleteRow(0)

		if columnDefs is None:
			columnDefs = []
			if _headerTitles is None:
				for i in range(0, len(spanInfos)):
					columnDefs.append(ColumnDef(str(i), None))
			else:
				for i in range(0, len(spanInfos)):
					columnDefs.append(ColumnDef(_headerTitles[i], None))

		# convert the column matrices to values

		columnData:typing.List[list] = []

		for cm, cd in zip(charMatrixList, columnDefs):
			dataLines = cm.rowsToValues(
				bTrimLeft=bLStrip,
				bTrimRight=bRStrip,
				parserFunction=cd.valueParser,
			)
			columnData.append(dataLines)

		# now convert everything to a table

		tableHeaders:typing.List[ColumnDef] = None
		if columnDefs is not None:
			# we have column definitions
			tableHeaders = columnDefs
		else:
			# we don't have column definitions
			tableHeaders = []
			if bFirstLineIsHeader:
				for title in _headerTitles:
					tableHeaders.append(ColumnDef(title))
			else:
				for i in range(0, len(columnData)):
					tableHeaders.append(ColumnDef(str(i)))

		# convert rows

		rows = []
		w = len(columnData)
		h = len(columnData[0])
		for iy in range(0, h):
			_temp = []
			for ix in range(0, w):
				_temp.append(columnData[ix][iy])
			rows.append(_temp)

		return Table(tableHeaders, rows)
	#

#


