from dotenv import load_dotenv
import os
from janes.authentication import Authentication
from janes.extract import Intara, Query
import logging 
import argparse

## create logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class Parsekwargs(argparse.Action):
def __call__(self, parser, namespace, values, option_string=None): 
    setattr(namespace, self.dest, dict())
    for value in values:
        key, value = value.split("=", 1)
        getattr(namespace, self.dest)[key] = value

def parse_args():
    parser = argparse.ArgumentParser(description="Extract data from Janes Intara API")
    parser.add_argument(
        "--endpoint", type=str, help="The endpoint to extract data from"
    )
    parser.add_argument("--mode", type=str, help="The mode to extract data with") 
    parser.add_argument("--output_path", type=str, help="The output file name")
    parser.add_argument("--output_directory", type=str, help="The output directory")
    parser.add_argument( "--x_api_key", type=str, help="The x-api-key key to authenticate with")
    parser.add_argument("--token", type=str, help="The token to authenticate with") 
    parser.add_argument("--api_url", type=str, help="The API URL to use for queries")
    parser.add_argument("--client_id", type=str, help="The client ID to authenticate with")
    parser.add_argument("--client_secret", type=str, help="The client secret to authenticate with")
    parser.add_argument("--query_parameters", nargs="*", action=Parsekwargs) 
    return parser.parse_args()

##load env variables if not provided by args
load_dotenv()

def authorize_no_token(api_url: str, client_id: str, client_secret: str, api_key: str):
"""
Authorize with Janes Intara API without a token

Args:
api_url (str): The API URL to use for queries 
client_id (str): The client ID to authenticate with 
client_secret (str): The client secret to authenticate with 
api_key (str): The x-api-key key to authenticate with

Returns:
Authentication: The authentication object
"""
if not client_id or not client_secret:

raise ValueError(
"No token provided. Please provide client_id and client_secret to generate token."
)

auth = Authentication( 
    url_base=api_url, 
    client_id=client_id, 
    client_secret=client_secret, 
    api_key=api_key,
)
auth.authenticate()

return auth

def authorize_with_token(api_url: str, token: str, api_key: str):
"""
Authorize with Janes Intara API with a token

Args:
api_url (str): The API URL to use for queries 
token (str): The token to authenticate with 
api_key (str): The x-api-key key to authenticate with

Returns: 
Authentication: The authentication object 
"""
##authenticate if token is passed as an argument 
logger.info("Authenticating with Janes Intara API")

auth = Authentication(
url_base=api_url,
api_key=api_key,
token=token,
)
auth.authenticate()

return auth

def validate_vars(api_key, api_url, token):
if not api_key or not api_url or not token:
logger.info(
"""Please either provide the following CLI arguments or set the following environment variables:
--x_api_key (INTARA_API_KEY), --api_url (INTARA_API_URL), --token (INTARA_API_TOKEN)"""
)

def run_extraction(
endpoint: str, 
auth: Authentication,
query_parameters: dict,
mode: str,
output_path: str,
output_directory: str,
)->list:
    """
run the extraction process

Args:

endpoint (str): The endpoint to extract data from 
auth (Authentication): The authentication object 
query_parameters (dict): the query parastors to use 
mode (str): The node to extract data with 
output_path (str): the output file name 
output_directory (str): The output directory

Returns:

list: The extracted data
"""
##extract data
logger.info("Extracting data from {endpoint} using mode: {mode}")

query=Query(
  endpoint=endpoint,
  parameters=query_parameters,
)
intara = Intara(authentication=auth, query=query)
results = intara.extract(
mode=mode, output_path=output_path, output_directory=output_directory
)
logger.info(f"Total results: {intara.total_results}")

return results

def get_api_url(api_url: str):
return (
api_url
if api_url
else os.getenv("INTARA_API_URL", "https://intara-api.janes.com")
)
def get_client_id(client_id: str):
return client_id if client_id else os.getenv("INTARA_CLIENT_ID", None)

def get_client_secret(client_secret: str):
return client_secret if client_secret else os.getenv("INTARA_CLIENT_SECRET", None)

def get_token(token: str):
return token if token else os.getenv("INTARA_API_TOKEN", None)


def get api_key(api_key: str):
return api_key if api_key else os.getenv("INTARA_API_KEY", None)


def main(args=None):

## parse arguments

if args is None:
args= parse_args()

endpoint = args.endpoint
output_path = args.output_path
output_directory = args.output_directory
mode = args.mode
token = get_token(args.token)
api_key = get_api_key(args.x_api_key)
api_url = get_api_url(args.api_url)
client_id = get_client_id(args.client_id)
client_secret = get_client_secret(args.client_secret)
query_parameters = args.query_parameters if args.query_parameters else {}
query_parameters.update({"pageSize": "1000"})

##check vars
validate_vars(api_key, api_url, token)

if mode in["file", "stream"] and not output_path and not output_directory:
  raise ValueError("Please provide an output path or directory")


## handle output path

if mode in ["file", "stream"] and not output_path and output_directory: 
    output_path = rf"{output_directory}/{endpoint}.json"

if not token:
     auth = authorize_no_token(api_url, client_id, client_secret, api_key)

else:
     auth= authorize_with_token(api_url, token, api_key)

try:

results = run_extraction(

endpoint, auth, query_parameters, mode, output path, output_directory
)

if mode == "memoгy":
return results

except Exception as e:

raise RuntimeError(f"An error occurred: {e}")

saved_to = output_path if mode in ["file", "stream"] else output_directory
logger.info("Extract complete!")
if mode!= "memory":
logger.info(f"Data saved to: {saved_to}")

if__name__ == "__main__":
main()

