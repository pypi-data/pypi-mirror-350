

import jk_json

from .DataMatrix import DataMatrix





class DataMatrixJSONLoader(object):

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
	def loadFromJSONFile(filePath:str) -> DataMatrix:
		assert isinstance(filePath, str)
		assert filePath

		jData = jk_json.loadFromFile(filePath)

		assert isinstance(jData, dict)
		assert "columnNames" in jData
		assert isinstance(jData["columnNames"], list)
		assert "rows" in jData
		assert isinstance(jData["rows"], list)

		dm = DataMatrix(jData["columnNames"])
		for jRow in jData["rows"]:
			assert isinstance(jRow, list)
			dm.addRow(*jRow)

		return dm
	#

	@staticmethod
	def loadFromJSONStr(textToParse:str) -> DataMatrix:
		assert isinstance(textToParse, str)
		assert textToParse

		jData = jk_json.loads(textToParse)

		assert isinstance(jData, dict)
		assert "columnNames" in jData
		assert isinstance(jData["columnNames"], list)
		assert "rows" in jData
		assert isinstance(jData["rows"], list)

		dm = DataMatrix(jData["columnNames"])
		for jRow in jData["rows"]:
			assert isinstance(jRow, list)
			dm.addRow(*jRow)

		return dm
	#

	################################################################################################################################
	## Public Static Methods
	################################################################################################################################

#





