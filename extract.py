from Janes.assets.logutils import sdkGenericError, sdkdenericinfo
Import Json
Import math
Import os
import requests
from urllib.parse import urljoin
from tqdm.auto import tqdm
from json stream.writer import streamable_list
from typing import Any, Dict, Generator, List, Optional, Union

class Intara:

"""
Class to extract data from the Janes Intara (and Enterprise Search) API. It supports extracting to memory, a single file,

multiple files, or streaming to a file. It has the following attributes:

type: Type of the reader

query: Query object

update: Boolean value to indicate if the data is to be updated

update from: Date from which the data is to be updated

authentication: Authentication object
"""

def__init__(self, authentication: Any, query: Any):

self.type ="Intara_API_Reader"
self.query= query
self.update= False
self.update_from= None 
self.authentication =authentication

self.map_endpoints(endpoint=query.endpoint)

self.parameters=query.parameters

def map_endpoints(self, endpoint: str) -> None:
"""
This method maps the endpoint name to the corresponding endpoint URL.

Arguments:
def map_endpoints(self, endpoint: str) -> None:

Arguments:

endpoint: Name of the endpoint to be queried
"""
endpoint_mapper = {
"equipment":"/graph/equipment",
"events":"/graph/events",
"installations": "/graph/installations", 
" military-groups": "/graph/military-groups",
"ships":"/graph/ships",
"organizations": "/graph/organizations",
"non-state-groups": "/graph/non-state-groups",
 "classifications": "graph/classifications",
"locations": "graph/locations",
 "Inventory": "graph/inventory",
"orbats": "graph/orbats",
"units": "graph/units",
"specifications": "graph/specifications",
"news": "text/news",
"analysis": "text/analysis",
"profiles": "text/profiles",
}
self.endpoint_path= endpoint_mapper.get(endpoint, None)
self.endpoint =endpoint

def get_response(

self, query_string: str, params: Dict[str, Any], verbose=False

)-> Dict[str, Any]:
"""
This method sends a get request to the API and returns the response.

Arguments:
query_string: URL for the query
params: Dictionary of parameters to be used in the query string

Returns:

dict: JS0N response from the API
"""
r=requests.get(

query_string, params=params, headers=self.authentication.session.headers

if verbose:
    SdkGenericinfo("Response URL: {r.url}")

r.raise_for_status()

return r.json()

def get_total_results(self, response: Dict[str, Any])-> int:
    """This method returns the total number of results from the response.

Arguments:
response: JSON response from the API
Returns:
Int: Total number of results from the response
"""
return response.get("search", {}).get("totalhesults", 0)

def yield_results(

self, response: Dict[str, Any]

)-> Generator[Dict[str, Any], None, None):
""" This method yields the results from the response.

Arguments:

response: JSON response from the API
yield_results(

Yields:

dict: JSON dictionary from the response
"""
results= response.get("results", [])

if results:

for result in results:

yield result
else:
    SdkGenericInfo("No results found for the query.")

def retrieve(self) -> Generator [Dict[str, Any], None, None]:
"""
This method retrieves data from the Janes Intara API based on the query and query parameters. 
It constructs the URL for query string using the Base URL and Endpoint name and sends a get request.
If the response code is not 200, it raises an error.
Otherwise if the total number of results are not 0, it parses the first page of results as a json. It then counts the total number of pages, iterates through each one and appends the results into the json.

Returns:

list: JSON array of dictionaries from the json response
"""
SdkGenericInfo(f"Collecting {self.query.endpoint} data from Janes Intara")

query_string=urljoin(self.authentication.url_base, self.endpoint_path)

response=self.get_response(query_string, self.parameters, verbose=True)

yield from self.yield_results(response)

total_results=self.get_total_results (response)

self.total_results=total_results

SdkGenericInfo("Your query returned {total_results} results.")

if total results==0:

SdkGenericInfo(

"The API did not return any results for the query. Please check your query parameters."
)
else:
    total_pages=math.ceil(total_results/len(response["results"])) 
    SdkGenericInfo(f"Total pages to retrieve: {total_pages}")
    with tqdm(total=total_pages) as pbar:
      pbar.update()

#iterate through each page

while "next" in response.get("_links", {}):

pbar.update()

#get next page

query_string=urljoin(

self.authentication.url_base,

response.get("_links", {}).get("next", {}).get("href", ""),
)

response=self.get_response(query_string, self.parameters) 
yield from self.yield_results(response)

def stream_retrieve(self) -> Generator[Dict[str, Any], None, None]:
"""
This method allows the user to stream the data from the Janes Intara API based on the query and query parameters.
"""
retrieved=self.retrieve()

return streamable_list(retrieved)

def check_output_path(self, output_path: Optional[str]) -> str:

If output_path is None:
 raise SdkGenericError("The output path is not specified.")

return output_path

def extract_to_memory(self) -> List[Dict(str, Any]]:
    return [result for result in self.retrieve()]
    
def extract_to_file(self, output_path: str) -> None: 
    output_path = self.check_output_path(output_path) 
    results = [result for result in self.retrieve()] 
    with open(output_path, "w", encoding="utf-8") as f: 
        json.dump(results, f, ensure_ascii=False, indent=4)

def extract_to_stream(self, output path: str) -> None: 
    output path = self.check_output_path(output_path) 
    retrieved_stream = self.stream_retrieve() 
    with open(output_path, "w", encoding="utf-8") as f: 
        json.dump(retrieved_stream, f, ensure_ascii=False, indent=4)

def extract_to_multiple_files(self, output_directory: str) -> None: 
    output_directory = self.check_output_path(output_directory)
     if not os.path.exists(output_directory):

SdkGenericInfo(

f"output directory does not exist. Creating directory {output_directory}"

)

os.makedirs (output_directory)

page_size = int(self.query.parameters.get("pageSize", 1000))

current_file=[]
for i, result in enumerate(self.retrieve()):

current_file.append(result) 
if (i + 1) % page_size = 0: 
    with open( 
        f"{output_directory}/{self.endpoint}_{i+1}.json", "w", encoding="utf-8", 

) as f:

json.dump(current_file, f, ensure_ascii=False, indent=4)
current_file = []
if current_file:
with open(

f"{output directory}/{self.endpoint}_{i+1}.json", "w", encoding="utf-8"

)as f:
json.dump(current file, f, ensure_ascii=False, indent=4)

def extract(

self, mode: str="memory", **kwargs: Any ) -> Union[List[Dict [str, Any]], None]:
if mode=="memory":
    return self.extract_to_memory()
elif mode=="file":
    return self.extract_to_file(kwargs.get("output_path", None))
elif mode=="stream":
    return self.extract_to_stream(kwargs.get("output_path", None))
elif mode=="multiple-files":
    return self.extract_to_multiple_files(kwargs.get("output_directory", None))
else:
    raise Exception(
         f"Your mode {mode} has not been implemented yet. Please specify the mode to be one of ('memory', 'file', 'stream', 'multiple-files'): {Exception}"
    )
