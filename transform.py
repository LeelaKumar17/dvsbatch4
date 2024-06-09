from janes.assets.logutils import SdkGenericinfo
from typing import Any, Dict, List, Optional
from Janes.transform import (
TransformEdgelist,
TransformNetworkX,
TransformRDF,
TransformGeojson,
)
class TransformIntara:
"""
High-level class to transform Intara JSON data into all formats defined within the 'transform' module.
wraps lower-level classes such as TransformDF and TransformNetworkX.
"""
CONTEXT_ATTRIBUTE = "@context"
VALID_FILE_FORMATS = [
"nt",
"n3",
"ttl",
"trig",
"jsonld",
"networkx",
"graphml",
"csv",
"parquet",
"geojson",
"dataframe",
]
VALID_TRANSFORMATIONS = ["rdf", "networkx", "edgelist", "geojson"]
VALID_MODES = ["memory", "file"]
EXCLUDE_KEYS = ["id", "label", "type", "metadata"]

def_init_(
self,
input_json: List[Dict[str, Any]],
Input_context: Dict[str, Any] = None,
geometry_type: str = "Point",
):
self._input_json = input_json
self._input_context = input_context
self._geometry_type = geometry_type

#################################
##validation Methods
#################################

def validate_file_format(self, file_format: str) -> None:
"""
Validate the output format.
Args: file_format (str): The output format.
Raises: ValueError: If the output format is invalid.
"""
if file_format not in self.VALID_FILE_FORMATS:
raise ValueError( 
    f"Invalid output format '{file_format}'. Specify the output format to be one of ({', '.join(self.VALID_FILE_FORMATS)})"
)
def validate_transformation(self, transformation: str) -> None:
"""
Validate the transformation.
Args: transformation (str): The transformation.
Raises:
ValueError: If the transformation is invalid.
"""
if transformation not in self.VALID_TRANSFORMATIONS:
raise ValueError(
f"Invalid transformation '{transformation}', specify the transformation to be one of ({', '.join(self.VALID_TRANSFORMATIONS)})"
)
def validate_mode(self, mode: str) -> None:
"""
Validate the mode.
Args:
mode (str): The mode.
Raises:
ValueError: If the mode is invalid.
"""
if mode not in self.VALID_MODES: 
    raise ValueError(

f"invalid mode '{mode}'. Specify the mode to be one of ({', '.join(self.VALID_MODES)})"
    )
def validate_args(self, **kwargs)-> None:
"""
Validate the arguments.
Args:
kwargs (Dict[str, Any]): The keyword arguments.
"""
transformation = kwargs.get("transformation", None)
file_format = kwargs.get("file_format", None)
mode = kwargs.get("mode", None)
if file_format:
    self.validate_file_format(file_format)
self.validate_transformation(transformation)
self.validate_mode(mode)

###################################
##Transformation / Saving Methods
###################################
def transform(
self,
transformation: str,
mode: str,
output_path: Optional[str] = None, 
file_format: Optional[str] = None,
longitude: Optional[str] = None, 
latitude: Optional[str] = None,
flatten: Optional[bool] = False,
separator: Optional[str] = "|",
)-> None:
"""
Transform the JSON data into the desired format.
Args:
transformation (str): The transformation type. One of "rdf", "networkx", "edgelist", "geojson". 
mode (str): The mode of transformation. Can be one of "file" or "memory".
output_path (str): The output path.
file_format (str): The file format.
longitude (str): the longitude key (only for GeoJSON transformation)
latitude (str): The latitude key (only for GeoJSON transformation) 
flatten (bool): whether to flatten the JSON data(only for GeoJSON transformation) 
separator (str): The separator for flattening (only for GeoJSON transformation)
"""
self.validate_args(transformation=transformation, mode=mode)
if not transformation:
raise ValueError("Transformation type not specified")
if not mode:
raise ValueError("Mode not specified")
SdkGenericInfo(f"Performing {transformation} transformation to {mode}")

if transformation == "rdf":
returned = TransformRDF(
input_json=self._input_json, input_context=self._input_context 
).transform(file_format=file_format, mode=mode, output_path=output_path)
elif transformation == "networkx":
returned = TransformNetworkX(
input_json=self._input_json, input_context=self._input_context 
).transform(file_format=file_format, mode=mode, output_path=output_path)
elif transformation == "edgelist": 
returned = TransformEdgelist(
input_json = self._input_json, input_context=self._input_context 
).transform(file_format=file_format, mode=mode, output_path=output_path)
elif transformation == "geojson":
returned = TransformGeoJson(
input_json=self._input_json, geometry_type=self._geometry_type
).transform(
file_format=file_format,
mode=mode,
output_path=output_path, 
longitude=longitude,
latitude=latitude,
flatten=flatten,
separator=separator,
)
else:

raise ValueError(f"Invalid transformation '{transformation}'")

SdkGenericinfo("Transformation complete!")
return returned
