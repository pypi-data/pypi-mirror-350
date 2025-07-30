


import typing





DataMatrixRow = typing.NewType("DataMatrixRow", object)

class DataMatrixRow(object):

	################################################################################################################################
	## Constructor Method
	################################################################################################################################

	def __init__(self, columnNamesToIndexMap:typing.Dict[str,int], rowData:typing.List[typing.Any]):
		self.__columnNamesToIndexMap = columnNamesToIndexMap
		self.__rowData = rowData
	#

	################################################################################################################################
	## Public Properties
	################################################################################################################################

	################################################################################################################################
	## Helper Method
	################################################################################################################################

	################################################################################################################################
	## Public Method
	################################################################################################################################

	def __getitem__(self, ii:typing.Union[int,str]):
		if isinstance(ii, int):
			return self.__rowData[ii]
		elif isinstance(ii, str):
			n = self.__columnNamesToIndexMap[ii]
			return self.__rowData[n]
		elif isinstance(ii, slice):
			return self.__rowData[ii]
		else:
			raise Exception()
	#

	def get(self, ii:typing.Union[int,str]) -> typing.Any:
		if isinstance(ii, int):
			if (ii < 0) or (ii > len(self.__rowData)):
				return None
			return self.__rowData[ii]
		elif isinstance(ii, str):
			n = self.__columnNamesToIndexMap.get(ii)
			if n is None:
				return n
			return self.__rowData[n]
		else:
			raise Exception()
	#

	def __setitem__(self, ii:typing.Union[int,str], value):
		if isinstance(ii, int):
			self.__rowData[ii] = value
		elif isinstance(ii, str):
			n = self.__columnNamesToIndexMap[ii]
			self.__rowData[n] = value
		else:
			raise Exception()
	#

	def __len__(self):
		return len(self.__rowData)
	#

	def __iter__(self):
		return self.__rowData.__iter__()
	#

	def clone(self) -> DataMatrixRow:
		return DataMatrixRow(self.__columnNamesToIndexMap, list(self.__rowData))
	#

#








