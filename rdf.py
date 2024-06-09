from janes.assets.logutils import sdkGenericinfo 
from typing import Any, Dict, List
from rdflib import Graph
import json
from pathlib import Path
from copy import deepcopy

class TransformRDF:
"""

Class to transform Intara JSON data to one of the following RDF Formats - "nt", "n3", "ttl", "trig", "jsonld".
Args:
input_json (List[Dict(str, Any]]): The input JSON data.
input_context (Dict[str, Any]): The Input Context data.
"""
CONTEXT_ATTRIBUTE = "@context"

VALID_OUTPUT_FORMATS = ["nt", "n3", "ttl", "trig", "jsonld"]

def_init_(self, input_json: List[Dict[str, Any]], input_context: Dict[str, Any]):
self._input_json = input_Json 
self._input_context = input_context

def validate_output_format(self, file_format: str) -> None:
"""
Validate the output format.

Args: file_format (str): The output format.

Raises:

ValueError: If the output format is invalid.
"""
if file_format not in self.VALID_OUTPUT_FORMATS:

raise ValueError(
     f"Invalid output format '{file_format}'. Specify the output format to be one of ({', '.join(self.VALID_OUTPUT_FORMATS)})"
)

def parse_jsonld(self, entities: List[Dict[str, Any]]) -> Graph:
"""
Parse a JSON-LD entity to an RDF graph.

Args: entities (List[Dict[str, Any]]): The JSON-LD entities.

Returns:

Graph: The parsed RDF graph.
"""
if not isinstance(entities, list): 
    raise ValueError("Invalid entity. Expected a JSON array.")

entities_copied = deepcopy(entities)

for entity in entities_copied: 
    entity.update({self.CONTEXT_ATTRIBUTE: self._input_context})

jsonld_string = json.dumps(entities_copied) 
g = Graph().parse(data=jsonld_string, format="json-ld")
return g

def save_rdf(self, g: Graph, output_path: str, file_format: str) -> None:
"""
Save the RDF graph to a file.
Args:

g (Graph): The graph to save.

output_path ( str): The output path.

file_format (str): The file format.
""" 
if not isinstance(g, Graph):
    raise ValueError(

"Invalid graph object. Expected rdflib.graph.Graph object."
    )
with open(output_path, "w+", encoding="UTF-8") as f:
f.write(g.serialize(format=file_format))

def transform(self, mode: str = "file", file_format: str = None, **kwargs)-> None:
"""
Transform JSON to an RDF format.
Args:
mode (str): The mode of transformation. Can be one of "file" or "memory"
file_format (str): The file format. Can be one of "nt", "n3", "ttl", "trig", "Jsonld"
"""
output_path = kwargs.get("output_path", None)

if mode not in ["file", "memory"]:

raise ValueError(

"Invalid mode. Specify the mode to be one of ('file', 'memory')"
)
SdkGenericInfo("Transforming Data")

transformed = self.parse_jsonld(self._input_json) 
SdkGenericInfo("Transformation Complete!")

if mode == "memory":
return transformed

elif mode == "file":
if not output_path:
raise valueError("Output path is required for file node.")

SdkGenericInfo("Validating Arguments")
self.validate_output_format(file_format)

SdkGenericInfo("Saving Data")

file = Path(output_path)

file.parent.mkdir(parents=True, exist_ok=True)

self.save_rdf(transformed, output_path, file_format)
