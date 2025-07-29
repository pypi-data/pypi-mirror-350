

import typing

from .ColumnDef import ColumnDef
from .Table import Table
from .StrNode import StrNode






class LineList(list):

	################################################################################################################################
	## Constructors
	################################################################################################################################

	def __init__(self, *args):
		super().__init__()
		if len(args) == 0:
			pass
		elif len(args) == 1:
			if isinstance(args[0], str):
				self.extend(args[0].rstrip().split("\n"))
			elif isinstance(args[0], (tuple,list)):
				self.extend(args[0])
			else:
				raise TypeError()
		else:
			raise Exception("Parameters!")
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

	#
	# Returns a line numbers of lines that are empty.
	#
	def getLineNumbersOfEmptyLines(self, bStrip:bool = True) -> list:
		assert isinstance(bStrip, bool)

		ret = []
		for lineNo, line in enumerate(self):
			if bStrip:
				line = line.strip()
				if not line:
					ret.append(lineNo)
		return ret
	#

	#
	# Check if the specified column is a vertical space column (= all characters at position <i>pos</i> are spaces)
	#
	def isVerticalSpaceColumn(self, pos:int) -> bool:
		return self.isSpaceColumn(pos)
	#

	#
	# Check if the specified column is a vertical space column (= all characters at position <i>pos</i> are spaces)
	#
	def isSpaceColumn(self, pos:int) -> bool:
		for i in range(0, len(self)):
			line = self[i]
			if pos < len(line):
				if not line[pos].isspace():
					#print("@ " + str(pos) + " with " + repr(line[pos]) + " of " + repr(line))
					return False
		#print("@ " + str(pos) + " is space")
		return True
	#

	#
	# Considers the existing line data as a rectangular block of text. This block is then scanned for vertical lines that only contain spaces.
	# This method then returns a list of boolean values, each representing wether or not this column contains spaces.
	# The length of the list is therefore equal to the length of the longest line.
	#
	# @return		bool[] listOfSpaceColumns		One boolean value for every column.
	#
	def identifyAllSpaceColumns(self) -> typing.List[bool]:
		maxLineLength = max([ len(line) for line in self ])
		assert maxLineLength > 0

		ret = []
		for i in range(0, maxLineLength):
			ret.append(self.isSpaceColumn(i))
		return ret
	#

	#
	# This method identifies all split positions.
	# A split position is characterizd by the previous column being a space column and the current column not being a space column.
	#
	# @param		int? maxSplitPositions			(optional) The maximum number of split positions. Specify None if not applicable.
	# @return		int[] spaceColumnPositions		Suitable positions to split at if you intend to convert this list to a table.
	#
	def identifySpaceColumnPositions(self, maxSplitPositions:int = None) -> typing.List[int]:
		maxLineLength = max([ len(line) for line in self ])
		assert maxLineLength > 0
		if maxSplitPositions is not None:
			assert isinstance(maxSplitPositions, int)
			assert maxSplitPositions > 0

		ret:typing.List[int] = []
		bLastWasSpaceColumn:bool = False
		bAllowAppending:bool = not self.isSpaceColumn(0)
		iLast:int = -1
		for i in range(0, maxLineLength):
			bThisIsSpaceColumn = self.isSpaceColumn(i)
			if not bThisIsSpaceColumn and bLastWasSpaceColumn:
				if bAllowAppending:
					ret.append(iLast)
					if maxSplitPositions and (len(ret) >= maxSplitPositions):
						break
				bAllowAppending = True
			bLastWasSpaceColumn = bThisIsSpaceColumn
			iLast = i

		return ret
	#

	def identifyRowsStartingWithSpaces(self) -> list:
		ret = []
		for i, line in enumerate(self):
			if (len(line) > 0) and (line[0] in ( ' ', '\t' )):
				ret.append(i)
		return ret
	#

	def identifyRowsNotStartingWithSpaces(self) -> list:
		ret = []
		for i, line in enumerate(self):
			if not ((len(line) > 0) and (line[0] in ( ' ', '\t' ))):
				ret.append(i)
		return ret
	#

	def dump(self, prefix:str = None, printFunc = None, splitPositions:list = None):
		if prefix is None:
			prefix = ""
		else:
			assert isinstance(prefix, str)

		if printFunc is None:
			printFunc = print
		else:
			assert callable(printFunc)

		# ----

		if splitPositions:
			table = self.createStrTableFromColumns(splitPositions, False, False, bFirstLineIsHeader=False)
			for row in table:
				line = "|" + "|".join(row) + "|"
				printFunc(prefix + line)
		else:
			printFunc(prefix + "LineList<[")
			for item in self:
				printFunc(prefix + "\t" + repr(item) + ",")
			printFunc(prefix + "]>")
	#

	#
	# For every single line count the number of leading space characters. Put all these counts into a list (= one count for every line) and return this list.
	#
	# @return				int[]			Returns a list of counts that indicate how many leading space characters there are in each line.
	#
	def getLeadingSpaceCounts(self) -> typing.List[int]:
		counts = []
		for line in self:
			bCounted = False
			for n, c in enumerate(line):
				if not c.isspace():
					counts.append(n)
					bCounted = True
					break
			if not bCounted:
				counts.append(len(line))
		minPos = min(counts)

		return counts
	#

	#
	# @param		bool bLStrip					Perform an <c>lstrip()</c> on each line.
	# @param		bool bRStrip					Perform an <c>rstrip()</c> on each line.
	#
	def extractColumn(self, fromPos:typing.Union[int,None], toPos:typing.Union[int,None], bLStrip:bool, bRStrip:bool) -> list:
		if fromPos is not None:
			isinstance(fromPos, int)
		if toPos is not None:
			isinstance(toPos, int)
		if (fromPos is None) and (toPos is None):
			raise Exception("Parameters!")
		assert isinstance(bLStrip, bool)
		assert isinstance(bRStrip, bool)

		ret = []

		for line in self:
			s = line[fromPos:toPos]
			if bLStrip:
				s = s.lstrip()
			if bRStrip:
				s = s.rstrip()
			ret.append(s)

		return ret
	#

	#
	# Get a list of columns. Each column contains the strings found in the specified position range.
	#
	# @param		bool bLStrip					Perform an <c>lstrip()</c> on each line.
	# @param		bool bRStrip					Perform an <c>rstrip()</c> on each line.
	#
	def extractColumns(self, positions:typing.Union[tuple,list], bLStrip:bool, bRStrip:bool) -> list:
		assert positions
		if positions[0] != 0:
			positions = [ 0 ] + positions

		ret = []
		for i in range(1, len(positions)):
			fromPos, toPos = positions[i-1], positions[i]
			ret.append(self.extractColumn(fromPos, toPos, bLStrip, bRStrip))
		ret.append(self.extractColumn(positions[-1], None, bLStrip, bRStrip))

		return ret
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
	#
	def createStrTableFromColumns(self,
			positions:typing.Union[tuple,list],
			bLStrip:bool,
			bRStrip:bool,
			bFirstLineIsHeader:bool
		) -> Table:

		assert isinstance(bLStrip, bool)
		assert isinstance(bRStrip, bool)
		assert isinstance(bFirstLineIsHeader, bool)

		columnsData = self.extractColumns(positions, bLStrip, bRStrip)
		nColumns = len(columnsData)
		nRows = len(columnsData[0])

		ret = []
		for nRow in range(0, nRows):
			row = []
			for nCol in range(0, nColumns):
				row.append(columnsData[nCol][nRow])
			ret.append(row)

		if bFirstLineIsHeader:
			headers = ret[0]
			del ret[0]
		else:
			headers = [ None ] * len(ret[0])

		for i in range(0, nColumns):
			if headers[i] is None:
				headers[i] = ColumnDef(str(i), None)
			else:
				headers[i] = ColumnDef(headers[i], None)

		return Table(headers, ret)
	#

	#
	# Invokes <c>createStrTableFromColumns()</c> to create a string table and then converts this data to a data table.
	#
	# @param		int[] positions					(required) The split positions
	# @param		bool bLStrip					(required) Perform an <c>lstrip()</c> on each line.
	# @param		bool bRStrip					(required) Perform an <c>rstrip()</c> on each line.
	# @param		bool bFirstLineIsHeader			(required) Specify <c>true</c> here if the first line contains header information.
	# @param		str[]|ColumnDef[] columnDefs	(required) A set of column definitions, one for each column.
	#												If column definitions are specified together with <c>bFirstLineIsHeader == True</c> the first line is removed and the column definitions
	#												specified are used to form the table header.
	#
	def createDataTableFromColumns(self,
			positions:typing.Union[tuple,list],
			bLStrip:bool,
			bRStrip:bool,
			bFirstLineIsHeader:bool,
			columnDefs:typing.Union[tuple,list,None]
		) -> Table:
		assert positions
		if positions[0] != 0:
			positions.insert(0, 0)
		assert isinstance(bLStrip, bool)
		assert isinstance(bRStrip, bool)
		assert isinstance(bFirstLineIsHeader, bool)

		# ----

		table = self.createStrTableFromColumns(positions, bLStrip, bRStrip, bFirstLineIsHeader=False)

		if columnDefs is not None:
			assert isinstance(columnDefs, (tuple,list))
			if len(columnDefs) != table.nColumns:
				raise Exception("Number of column definitions specified ({}) does not match the number of column splits ({})!".format(len(columnDefs), table.nColumns))
			_tmp = []
			for item in columnDefs:
				if isinstance(item, str):
					_tmp.append(ColumnDef(item, None))
				elif isinstance(item, ColumnDef):
					_tmp.append(item)
				else:
					raise ValueError()
				columnDefs = _tmp
			if bFirstLineIsHeader:
				del table[0]

		else:
			if bFirstLineIsHeader:
				columnTitles = table[0]
				del table[0]
				columnDefs = [ ColumnDef(columnTitle) for columnTitle in columnTitles ]
			else:
				raise Exception("Header specification required!")

		# extract value parsers

		valueParsers = [ x.valueParser for x in columnDefs ]

		# build data table

		ret = []
		for row in table:
			rowData = []
			for s, valueParser in zip(row, valueParsers):
				if valueParser:
					rowData.append(valueParser(s))
				else:
					rowData.append(s)
			ret.append(rowData)

		return Table(columnDefs, ret)
	#

	#
	# Splits the current list of lines at empty lines.
	#
	# @param		bool bRStrip		Perform an <c>rstrip()</c> on each line.
	#
	def splitAtEmptyLines(self, bRStrip:bool = True) -> list:
		assert isinstance(bRStrip, bool)

		ret = []
		buffer = LineList()

		for line in self:
			if bRStrip:
				line = line.rstrip()
			if line:
				buffer.append(line)
			else:
				if buffer:
					ret.append(buffer)
					buffer = LineList()

		if buffer:
			ret.append(buffer)

		return ret
	#

	#def createStrTableAtSpaceColumns(

	#
	# This method modifies this line list *in place*. It removes all trailing white spaces of each line.
	#
	def rightTrimAllLines(self):
		for i in range(0, len(self)):
			self[i] = self[i].rstrip()
	#

	#
	# This method modifies this line list *in place*. It removes all emtpy lines at the beginning of this line list.
	#
	def removeLeadingEmptyLines(self):
		while self and not self[0]:
			del self[0]
	#

	#
	# This method modifies this line list *in place*. It removes all emtpy lines at the end of this line list.
	#
	def removeTrailingEmptyLines(self):
		while self and not self[-1]:
			del self[-1]
	#

	#
	# This method modifies this line list *in place*. It removes all emtpy lines.
	#
	def removeAllEmptyLines(self):
		newList = []
		for line in self:
			if line:
				newList.append(line)
		self.clear()
		self.extend(newList)
	#

	#
	# This method modifies this line list *in place*. It calls <c>getLeadingSpaceCounts()</c> in order to get a map of leading spaces and then trims the start of the line to
	# have all common (!) leading spaces removed.
	#
	def removeAllCommonLeadingSpaces(self):
		counts = self.getLeadingSpaceCounts()
		minPos = min(counts)
		if minPos > 0:
			newLines = [ s[minPos:] for s in self ]
			self.clear()
			self.extend(newLines)
	#

	def findExact(self, lineText:str, startIndex:int = 0) -> int:
		for i in range(startIndex, len(self)):
			line = self[i]
			if line == lineText:
				return i

		return -1
	#

	def findBckwdExact(self, lineText:str, startIndex:int = -1) -> int:
		if startIndex < 0:
			startIndex = len(self) - 1

		for i in reversed(range(0, startIndex)):
			line = self[i]
			if line == lineText:
				return i

		return -1
	#

	def extractFromTo(self, fromIndex:int, toIndex:int = None):
		if toIndex is None:
			ret = self[fromIndex:]
		else:
			ret = self[fromIndex:toIndex]
		return LineList(ret)
	#

	def splitAtRows(self, rowNumbers:list) -> list:
		if not rowNumbers:
			return self

		ret = []
		lastSplitPos = 0
		for rowNo in rowNumbers:
			if rowNo <= lastSplitPos:
				continue
			ret.append(self.extractFromTo(lastSplitPos, rowNo))
			lastSplitPos = rowNo

		if rowNumbers[-1] < len(self):
			ret.append(self.extractFromTo(lastSplitPos))

		return ret
	#

	#
	# Check if all lines have the same prefix
	#
	def hasCommonPrefix(self, text:str) -> bool:
		if not self:
			# no data
			return False

		for line in self:
			if not line.startswith(text):
				return False
		return True
	#

	#
	# Check if all lines have the same prefix and then remove it
	#
	def removeCommonPrefix(self, text:str):
		if not self.hasCommonPrefix(text):
			raise Exception("Not a common prefix: " + repr(text))

		nSkip = len(text)
		newData = []
		for line in self:
			newData.append(line[nSkip:])

		self.clear()
		self.extend(newData)
	#

	#
	# Try to split each line at the specified delimiter and return the result as key value pairs.
	# Lines that do not contain the delimiter are skipped.
	#
	def convertToMapAtDelimIfPossible(self, delim:str) -> dict:
		assert delim

		ret = {}
		for line in self:
			pos = line.find(delim)
			if pos > 0:
				ret[line[:pos].strip()] = line[pos+1:].strip()
		return ret
	#

	#
	# Build a hierarchy of nodes according to line indentation.
	#
	# @param	callable<<int,str>,StrNode>		(optional) A method that instantiates a StrNode (or a subclass of StrNode)
	#
	def groupByIndentation(self, nodeFactory:typing.Callable[[int,str],StrNode] = None, rootNodeFactory:typing.Callable[[int,str],StrNode] = None) -> StrNode:
		if nodeFactory == None:
			nodeFactory = StrNode
		else:
			assert callable(nodeFactory)

		if rootNodeFactory == None:
			rootNodeFactory = StrNode
		else:
			assert callable(rootNodeFactory)

		# ----

		indentationTextTuples:typing.List[typing.Tuple[int,str]] = list(zip(self.getLeadingSpaceCounts(), self))
		if len(indentationTextTuples) == 0:
			raise Exception("No data")

		rootNode = rootNodeFactory(-1, "<root>")

		parentNode = None
		stack:typing.List[StrNode] = []
		currentTopNode = rootNode

		for nLevel, text in indentationTextTuples:
			newNode = nodeFactory(nLevel, text)

			if newNode.nLevel > currentTopNode.nLevel:
				# this is a child node
				stack.append(parentNode)
				currentTopNode.children.append(newNode)
				parentNode = currentTopNode
				currentTopNode = newNode
				continue

			# on same level or below
			while True:
				if newNode.nLevel < currentTopNode.nLevel:
					# below -> pop stack
					currentTopNode = parentNode
					parentNode = stack.pop()
					continue
				if newNode.nLevel == currentTopNode.nLevel:
					# same level
					break
				# error
				raise Exception("Error in input data: There is no element on the stack with corresponding level")

			parentNode.children.append(newNode)
			currentTopNode = newNode

		return rootNode
	#

	################################################################################################################################
	## Static Methods
	################################################################################################################################

#









