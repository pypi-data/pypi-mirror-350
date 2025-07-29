

import json

import jk_json

from ._IDataMatrix import _IDataMatrix





class DataMatrixJSONWriter(object):

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
	def saveAsJSONFilePretty(dm:_IDataMatrix, filePath:str, *, jsonEncoder:json.JSONEncoder = None):
		assert isinstance(dm, _IDataMatrix)
		assert isinstance(filePath, str)
		assert filePath

		jData = dm.toJSON()

		if jsonEncoder is None:
			jsonEncoder = jk_json.ObjectEncoder

		with open(filePath, "w", encoding="utf-8", newline="\n") as f:
			json.dump(jData, f, indent="\t", sort_keys=True, cls=jsonEncoder)
	#

	@staticmethod
	def saveAsJSONFile(dm:_IDataMatrix, filePath:str, *, jsonEncoder:json.JSONEncoder = None):
		assert isinstance(dm, _IDataMatrix)
		assert isinstance(filePath, str)
		assert filePath

		jData = dm.toJSON()

		if jsonEncoder is None:
			jsonEncoder = jk_json.ObjectEncoder

		with open(filePath, "w", encoding="utf-8", newline="\n") as f:
			json.dump(jData, f, cls=jsonEncoder)
	#

	# --------------------------------------------------------------------------------------------------------------------------------

	@staticmethod
	def toJSONStrPretty(dm:_IDataMatrix, *, jsonEncoder:json.JSONEncoder = None) -> str:
		assert isinstance(dm, _IDataMatrix)

		jData = dm.toJSON()

		if jsonEncoder is None:
			jsonEncoder = jk_json.ObjectEncoder

		return json.dumps(jData, indent="\t", sort_keys=True, cls=jsonEncoder)
	#

	@staticmethod
	def toJSONStr(dm:_IDataMatrix, *, jsonEncoder:json.JSONEncoder = None) -> str:
		assert isinstance(dm, _IDataMatrix)

		jData = dm.toJSON()

		if jsonEncoder is None:
			jsonEncoder = jk_json.ObjectEncoder

		return json.dumps(jData, cls=jsonEncoder)
	#

	################################################################################################################################
	## Public Static Methods
	################################################################################################################################

#





