

import typing

try:
	import jk_datamatrix
	bHasDataMatrix = True
except:
	bHasDataMatrix = False

from .ColumnDef import ColumnDef






#
# This class is derived from <c>list</c> and represents a very simple table. The items in this (table) list are rows of this table.
# The member <c>columnDefs</c> stores an array of <c>ColumnDef</c> objects that provide information about each column.
#
class Table(list):
	# @field		ColumnDef[] columnDefs		The table column definitions

	################################################################################################################################
	## Constructors
	################################################################################################################################

	#
	# @param		ColumnDef[] columnDefs		The table column definitions
	# @param		str[][] rows				The list of row data for this table.
	#
	def __init__(self, columnDefs:typing.List[ColumnDef], rows:list):
		assert isinstance(columnDefs, (tuple, list))
		assert isinstance(rows, (tuple, list))
		if len(rows) > 0:
			assert len(columnDefs) == len(rows[0])
		for h in columnDefs:
			assert isinstance(h, ColumnDef)

		super().__init__()

		self.columnDefs = columnDefs
		self.extend(rows)
	#

	################################################################################################################################
	## Public Properties
	################################################################################################################################

	#
	# Returns the number of columns of this table.
	#
	@property
	def nColumns(self) -> int:
		return len(self[0])
	#

	#
	# Returns the number of rows in this table.
	#
	@property
	def nRows(self) -> int:
		return len(self)
	#

	#
	# The variable <c>columnDefs</c> contains all header specifications. This property returns the header titles only.
	#
	# @return		str[]			Returns the titles of the column definitions.
	#
	@property
	def columnTitles(self) -> typing.List[str]:
		return self.__createListOfTitles(self.columnDefs)
	#

	################################################################################################################################
	## Helper Methods
	################################################################################################################################

	def __createListOfTitles(self, columnDefs:typing.List[ColumnDef]) -> list:
		assert isinstance(columnDefs, (tuple,list))
		for x in columnDefs:
			assert isinstance(x, ColumnDef)

		return [ x.name for x in columnDefs ]
	#

	def __createListOfValueParsers(self, columnDefs:typing.List[ColumnDef]) -> list:
		assert isinstance(columnDefs, (tuple,list))
		for x in columnDefs:
			assert isinstance(x, ColumnDef)

		return [ x.valueParser for x in columnDefs ]
	#

	################################################################################################################################
	## Public Methods
	################################################################################################################################

	def dump(self, prefix:str = None, printFunc = None):
		if prefix is None:
			prefix = ""
		else:
			assert isinstance(prefix, str)

		if printFunc is None:
			printFunc = print
		else:
			assert callable(printFunc)

		# ----

		prefix2 = prefix + "\t"
		printFunc(prefix + "{")
		if self.columnDefs:
			sout = [ prefix2, "[ " ]
			for cd in self.columnDefs:
				if len(sout) > 2:
					sout.append(", ")
				sout.append(str(cd))
			sout.append(" ]")
			printFunc("".join(sout))
		for row in self:
			sout = [ prefix2, "[ " ]
			for cell in row:
				if len(sout) > 2:
					sout.append(", ")
				sout.append(repr(cell))
			sout.append(" ]")
			printFunc("".join(sout))
			
		printFunc(prefix + "}")
	#

	#
	# Build a data matrix from this table.
	#
	# NOTE: Invoking this method requires the python module "<c>jk_datamatrix</c>" to be installed.
	#
	def toDataMatrix(self, columnDefs:typing.List[ColumnDef] = None) -> jk_datamatrix.DataMatrix:
		if not bHasDataMatrix:
			raise Exception("For invoking toDataMatrix() you need to install jk_datamatrix first: 'pip install jk_datamatrix'")

		# ----

		if columnDefs is None:
			columnDefs = self.columnDefs
		assert len(columnDefs) == self.nColumns

		columnTitles = self.__createListOfTitles(columnDefs)
		valueParsers = self.__createListOfValueParsers(columnDefs)

		m = jk_datamatrix.DataMatrix(columnTitles)

		for row in self:
			rowData = []
			for s, valueParser in zip(row, valueParsers):
				if valueParser:
					rowData.append(valueParser(s))
				else:
					rowData.append(s)
			m.addRow(*rowData)

		return m
	#

	#
	# Returns an iterator that provides dictionaries of data, one for each row.
	#
	def rowDictIterator(self) -> typing.Iterable[typing.Dict[str,typing.Any]]:
		_nColumns = self.nColumns
		for row in self:
			ret = {}
			for i in range(0, _nColumns):
				ret[self.columnDefs[i].name] = row[i]
			yield ret
	#

#









