



def getPositionsOfWords(line:str) -> list:
	ret = []
	bLastWasSpace = True
	for i, c in enumerate(line):
		if c.isspace():
			bLastWasSpace = True
		else:
			if bLastWasSpace:
				ret.append(i)
			bLastWasSpace = False
	return ret
#











