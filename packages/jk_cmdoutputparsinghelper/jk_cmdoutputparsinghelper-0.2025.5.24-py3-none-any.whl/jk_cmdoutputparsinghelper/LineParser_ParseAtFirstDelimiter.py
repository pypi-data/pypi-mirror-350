


import typing

from .ValueParserDef import ValueParserDef






class LineParser_ParseAtFirstDelimiter(object):

	################################################################################################################################
	## Constructors
	################################################################################################################################

	def __init__(self,
		delimiter:str = ":",
		bValueCanBeWrappedInDoubleQuotes:bool = False,
		bKeysReplaceSpacesWithUnderscores:bool = False,
		nIgnoreEmptyLines:bool = True):

		self.delimiter = delimiter
		self.bKeysReplaceSpacesWithUnderscores = bKeysReplaceSpacesWithUnderscores
		self.bValueCanBeWrappedInDoubleQuotes = bValueCanBeWrappedInDoubleQuotes
		self.bIgnoreEmptyLines = nIgnoreEmptyLines
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

	def parseLinesReturnList(self, lines:typing.Union[tuple,list], valueParserMap:dict = None) -> list:
		assert isinstance(lines, (tuple, list))
		if valueParserMap is not None:
			assert isinstance(valueParserMap, dict)

		# ---

		ret = []

		for line in lines:
			if not line and self.bIgnoreEmptyLines:
				continue
			k, v = line
			valueParser = valueParserMap.get(k)
			if valueParser is None:
				continue
			assert isinstance(valueParser, ValueParserDef)
			if valueParser.parseFunc is not None:
				v = valueParser.parseFunc(v)
			ret.append(self.parseLine(line))

		return ret
	#

	def parseLinesReturnDict(self, lines:typing.Union[tuple,list], valueParserMap:dict = None) -> dict:
		assert isinstance(lines, (tuple, list))
		if valueParserMap is not None:
			assert isinstance(valueParserMap, dict)

		# ---

		ret = {}
		for line in lines:
			if not line and self.bIgnoreEmptyLines:
				continue
			k, v = self.parseLine(line)
			if k:
				valueParser = valueParserMap.get(k)
				if valueParser is None:
					continue
				assert isinstance(valueParser, ValueParserDef)
				if valueParser.parseFunc is not None:
					v = valueParser.parseFunc(v)
				ret[valueParser.outputKey] = v

		return ret
	#

	def parseLine(self, line:str) -> tuple:
		assert isinstance(line, str)

		pos = line.find(self.delimiter)
		if pos > 0:
			k = line[:pos].strip()
			v = line[pos+1:].strip()
			if self.bValueCanBeWrappedInDoubleQuotes:
				if v.startswith("\"") and v.endswith("\""):
					v = v[1:-1]
					v = v.replace("\\\"", "\"")
			if self.bKeysReplaceSpacesWithUnderscores:
				k = k.replace(" ", "_")
			return k, v
		else:
			return None, None
	#

#







