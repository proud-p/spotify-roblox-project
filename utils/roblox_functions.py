import requests
from bs4 import BeautifulSoup
import configparser
import time
import json
from tqdm import tqdm

# ------Functions to deal with API keys and logging in -------



class RobloxAuthConfig:
    def __init__(self, config_path):
        """Initializes the AuthConfig object by reading from the provided .ini config path"""
        self.config_path = config_path
        self.config = configparser.ConfigParser()
        self.config.read(config_path)
        self.api_key = self.config['RobloxAPI']['api_key']
        self.client_id = self.config['RobloxAPI']['client_id']
        self.client_secret = self.config['RobloxAPI']['client_secret']
        self.redirect_uri = self.config['RobloxAPI']['redirect_uri']
        self.cookie = self.config['RobloxAPI']['cookie']
        self.place_id = self.config['RobloxAPI']['place_id']
        self.universe_id = get_universe_id(self.place_id)



# Functions to get universe id from place id

def get_game_page_source(place_id):

    # get page source
    
    url = f"https://www.roblox.com/games/{place_id}/onemorebits-Place"

    # Set headers to mimic a browser request
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }

    response = requests.get(url, headers=headers)

    # Check if the request was successful
    if response.status_code == 200:
        page_source = response.text
        # print(page_source) 
    else:
        print(f"Failed to retrieve the page. Status code: {response.status_code}")

    return page_source

def parse_response_for_universe_id(response):

    soup = BeautifulSoup(response, 'html.parser')

    # Find the div by ID and get the data-universe-id attribute
    game_detail_div = soup.find("div", id="game-detail-meta-data")
    if game_detail_div:
        universe_id = game_detail_div.get("data-universe-id")
        # print("Data-Universe-ID:", universe_id)
    else:
        print("Div not found")

    return universe_id


# Call this to get universe_id

def get_universe_id(place_id):
    """input: place_id -> str
        output: universe_id -> str"""
    response = get_game_page_source(place_id)
    universe_id = parse_response_for_universe_id(response)

    return universe_id




# ------ Functions to get and update the scripts in roblox -----

def get_children(auth, instance_id = 'root'):
    """Get list of child instances of root returns list of children, each child is dict
    Input: default api keys, game place_id, instance id defaults to root
    Output: Returns json loaded object"""
    # code taken from: # https://create.roblox.com/docs/cloud/open-cloud/instance



    # Keep this the same
    api_keyHeaderKey = "x-api-key"

    listChildrenUrl = "https://apis.roblox.com/cloud/v2/universes/%s/places/%s/instances/%s:listChildren"
    getOperationUrl = "https://apis.roblox.com/cloud/v2/%s"

    numberOfRetries = 10
    retryPollingCadence = 5

    doneJSONKey = "done"

    def ListChildren():
        url = listChildrenUrl % (auth.universe_id, auth.place_id, instance_id)
        headerData = {api_keyHeaderKey: auth.api_key}
        results = requests.get(url, headers = headerData)
        return results

    def GetOperation(operationPath):
        url = getOperationUrl % (operationPath)
        headerData = {api_keyHeaderKey: auth.api_key}
        results = requests.get(url, headers = headerData)
        return results

    def PollForResults(operationPath):
        currentRetries = 0
        while (currentRetries < numberOfRetries):
            time.sleep(retryPollingCadence)
            results = GetOperation(operationPath)
            currentRetries += 1

            if (results.status_code != 200 or results.json()[doneJSONKey]):
                return results

    response = ListChildren()
    # Parse the Operation object's path to use in polling for the instance resource.
    operationPath = response.json()['path']
    response = PollForResults(operationPath)
    print("Response:", response.status_code)

    return json.loads(response.text)


def find_matching_level(dict_list, search_value):
    """Find matching dict in list of dicts. Assumes search key is Name, returns as matching dict"""
    # Find the dictionary
    matching_dict = next((d for d in dict_list if d['engineInstance']['Name'] == search_value), None)
    if matching_dict:
        print("Found dictionary:", matching_dict)
    else:
        print("No matching dictionary found.")
    
    return matching_dict

def find_instance_id(auth,object_path):
    """Input the path of object you want to find. E.g. if there is a script at path 
    Workspace/MyScript , put in Workspace/MyScript as object path 
    
    Input: Object path -> str
    Output: instance id -> str"""

    recurse = object_path.split("/")
    # set to root instance for first level
    instance = "root"
    for level in tqdm(recurse):
        print(f"At level: {level}")
        children = get_children(auth,instance_id=instance)
        children = children['response']['instances']
        # find matching child
        matching_level_dict = find_matching_level(children,level)
        instance = matching_level_dict["engineInstance"]["Id"]
    
    print(f"Final instance id returned: {instance}")

    return instance

def get_instance(auth,instance_id,propertyName,propertyValue,instanceType):

    """Get actual instance of the object through returning operation path instead of just showing properties, code from:
    https://create.roblox.com/docs/cloud/open-cloud/instance#polling-for-results"""

    # Request header
    api_keyHeaderKey = "x-api-key"
    contentTypeHeaderKey = "Content-type"
    contentTypeHeaderValue = "application/json"
    # Endpoint URL for Update Instance method
    updateInstanceUrl = "https://apis.roblox.com/cloud/v2/universes/%s/places/%s/instances/%s"
    # JSON keys
    detailsJSONKey = "Details"
    engineInstanceJSONKey = "engineInstance"

    def GeneratePostData():
        propertiesDict = {propertyName: propertyValue}
        detailsDict = {instanceType: propertiesDict}
        print(detailsDict)
        instanceDict = {detailsJSONKey: detailsDict}
        outerDict = {engineInstanceJSONKey: instanceDict}
        return json.dumps(outerDict)

    def UpdateInstance(postData):
        url = updateInstanceUrl % (auth.universe_id, auth.place_id, instance_id)
        headerData = {api_keyHeaderKey: auth.api_key,
        contentTypeHeaderKey: contentTypeHeaderValue}
        return requests.patch(url, headers = headerData, data = postData)

    postData = GeneratePostData()
    response = UpdateInstance(postData)
    print("Response:", response.status_code, response.text)

    # Parse the Operation object's path from response. Poll for results to perform
    # the update.
    operationPath = response.json()['path']

    return operationPath



def update_request_instance(auth,operationPath):
    """Request instance update, no returns"""
    # Use the Operation path from your initial request
    # Takes the form of "universes/<universe_id>/places/<place_id>/instances/<INSTANCE_ID>/operations/<OPERATION_ID>"
    operationPath = operationPath

    # Polling constants
    numberOfRetries = 10
    retryPollingCadence = 5

    # Request header
    api_keyHeaderKey = "x-api-key"
    # Endpoint URL for long-running operation polling
    getOperationUrl = "https://apis.roblox.com/cloud/v2/%s"
    # JSON keys
    doneJSONKey = "done"

    def GetOperation(operationPath):
        url = getOperationUrl % (operationPath)
        headerData = {api_keyHeaderKey: auth.api_key}
        results = requests.get(url, headers = headerData)
        return results

    def PollForResults(operationPath):
        currentRetries = 0
        while (currentRetries < numberOfRetries):
            time.sleep(retryPollingCadence)
            results = GetOperation(operationPath)
            currentRetries += 1

            if (results.status_code != 200 or results.json()[doneJSONKey]):
                return results

    response = PollForResults(operationPath)
    print("Response:", response.status_code, response.text)

def update_instance(auth,instance_id,propertyName,propertyValue,instanceType):
    operationPath = get_instance(auth,instance_id,propertyName=propertyName,propertyValue=propertyValue,instanceType=instanceType)
    update_request_instance(auth,operationPath)
