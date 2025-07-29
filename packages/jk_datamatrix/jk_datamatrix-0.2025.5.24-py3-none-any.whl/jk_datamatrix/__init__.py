

__author__ = "Jürgen Knauth"
__version__ = "0.2025.5.24"
__email__ = "pubsrc@binary-overflow.de"
__license__ = "Apache2"
__copyright__ = "Copyright (c) 2021-2025, Jürgen Knauth"



# the writers. they don't have a dependency to DataMatrix.
from .DataMatrixCSVWriter import DataMatrixCSVWriter
from .DataMatrixJSONWriter import DataMatrixJSONWriter

# the DataMatrix and associated classes
from .DataMatrixRow import DataMatrixRow
from .DataMatrix import DataMatrix

# the loaders. they require an already defined DataMatrix.
from .DataMatrixJSONLoader import DataMatrixJSONLoader



# convenience methods
loadFromJSONFile = DataMatrixJSONLoader.loadFromJSONFile
loadFromJSONStr = DataMatrixJSONLoader.loadFromJSONStr

