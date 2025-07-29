

import typing
import io
import csv

from ._IDataMatrix import _IDataMatrix





class DataMatrixCSVWriter(object):

	################################################################################################################################
	## Constants
	################################################################################################################################

	################################################################################################################################
	## Constructor
	################################################################################################################################

	################################################################################################################################
	## Public Properties
	################################################################################################################################

	################################################################################################################################
	## Helper Methods
	################################################################################################################################

	################################################################################################################################
	## Public Methods
	################################################################################################################################

	@staticmethod
	def saveAsCSVFile(dm:_IDataMatrix, filePath:str):
		assert isinstance(dm, _IDataMatrix)
		assert isinstance(filePath, str)
		assert filePath

		with open(filePath, "w", newline="\n", encoding="UTF-8") as csvfile:
			writer = csv.DictWriter(csvfile, fieldnames=dm.columnNames, lineterminator="\n")
			writer.writeheader()
			writer.writerows(dm.rowdicts)
	#

	@staticmethod
	def toCSVStr(dm:_IDataMatrix) -> str:
		assert isinstance(dm, _IDataMatrix)

		csvfile = io.StringIO(newline="\n")
		with csvfile:
			writer = csv.DictWriter(csvfile, fieldnames=dm.columnNames, lineterminator="\n")
			writer.writeheader()
			writer.writerows(dm.rowdicts)
			return csvfile.getvalue()
	#

	@staticmethod
	def toCSVStrList(dm:_IDataMatrix) -> typing.List[str]:
		assert isinstance(dm, _IDataMatrix)

		_content = dm.toCSVStr()
		return _content.split("\n")
	#

	################################################################################################################################
	## Public Static Methods
	################################################################################################################################

#





