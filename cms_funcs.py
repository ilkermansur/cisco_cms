import requests
import urllib3
import xmltodict
from requests.auth import HTTPBasicAuth
import base64


urllib3.disable_warnings()

# Give credential

username = 'username'
password = 'password'
host = 'IP-ADDRESS-OF-CMS'
port = '443'

############################ GET COSPACES ############################ 

def get_cospaces_list(
      username=username,
      password=password,
      host=host
      ):
  """
  This Python function retrieves a list of CoSpaces using HTTP requests with basic authentication.
  The function `get_cospaces_list` returns a list of CoSpaces retrieved from a specified host
  using the provided username and password for authentication.

  == Parameters ==

  None

  """

  credentials = f"{username}:{password}"
  encoded_credential = base64.b64encode(credentials.encode()).decode()
  # Get CoSpaces

  url = f"https://{host}:443/api/v1/coSpaces/"

  headers = {
    'Content-Type': 'application/json',
    'Authorization': encoded_credential
  }

  all_cospaces = []
  offset = 0

  while True:
      # Create coSpaceList

      base_url = f"https://{host}:{port}/api/v1/coSpaces/"
      limit = 20

      url = f"{base_url}?offset={offset}"

      response = requests.get(url=url,
                          headers=headers,
                          auth= HTTPBasicAuth(username, password),
                          verify=False
                          )

      if response.status_code == 200:
          dict_data = xmltodict.parse(response.content)
          cospace_list = dict_data['coSpaces']['coSpace']
          all_cospaces.extend(cospace_list)

          if len(cospace_list) < limit:
              break

          offset = offset + limit

  return all_cospaces

############################ DELETE COSPACE ############################ 

def delete_cospace (
      coSpace_id,
      username=username,
      password=password,
      host=host
      ):
  
  """
  This Python function deletes a specified cospace using the provided credentials and host
  information.

  == Parameters ==

  coSpaceID (mandatory)

  """

  credentials = f"{username}:{password}"
  encoded_credential = base64.b64encode(credentials.encode()).decode()

  headers = {
  'Content-Type': 'application/json',
  'Authorization': encoded_credential
  }

  url = f"https://{host}:{port}/api/v1/coSpaces/{coSpace_id}"

  response = requests.delete(url=url,
                    headers=headers,
                    auth= HTTPBasicAuth(username, password),
                    verify=False
                    )
  if response.status_code==200:
     print (f'cospace {coSpace_id} is deleted')

  else:
     print (f'error is occured {response.status_code}')

############################ CREATE COSPACE ############################ 

def create_cospace (
      uri = None,
      name = None,
      callId = None,
      secondaryUri = None):
  
  """
  This Python function creates a CoSpace using the provided parameters and sends a POST request to a
  specified API endpoint.
  
  == Parameters ==

  name
  uri 
  callId (integer)
  secondaryUri

  """

  credentials = f"{username}:{password}"
  encoded_credential = base64.b64encode(credentials.encode()).decode()

  # Define payload

  payload = {
     'name' : name,
     'uri' : uri,
     'callId' : callId,
     'secondaryUri' : secondaryUri
     }

  # Create CoSpace

  url = f"https://{host}:{port}/api/v1/coSpaces/"

  headers = {
    'Content-Type': 'application/json',
    'Authorization': encoded_credential
  }

  response = requests.post(url,
                          auth= HTTPBasicAuth(username, password),
                          headers=headers,
                          data = payload,
                          verify=False
                          )

  if response.status_code == 200:
      print (f"creating coSpace {name} successful")
  else:
      print (f'error is occured {response.status_code}')

############################ CREATE ACCESS METHOD ############################ 
"""
This Python function creates a `Access Method`

== Parameters ==

coSpaceId (mandatory)
uri
callID (integer)
accessMethodName
callLegProfile

"""

def create_access_method (
      coSpace_id,
      uri=None,
      callId=None,
      access_method_name=None,
      callLegProfile=None
      ):

  credentials = f"{username}:{password}"
  encoded_credential = base64.b64encode(credentials.encode()).decode()

  # Define payload

  payload = {'uri' : uri,
             'callId' : callId,
             'name' : access_method_name,
             'callLegProfile': callLegProfile}

  # Create Access Method

  createAccessMethod_url =  f"https://{host}:{port}/api/v1/coSpaces/{coSpace_id}/accessMethods"

  headers = {
    'Content-Type': 'application/json',
    'Authorization': encoded_credential
  }

  response = requests.post(url=createAccessMethod_url,
                          auth= HTTPBasicAuth(username, password),
                          headers=headers,
                          data = payload,
                          verify=False
                          )

  if response.status_code == 200:
      print (f"creating coSpace {access_method_name} successful with {payload}")
  else:
      print (f'error is occured {response.status_code}')
    
############################ GET ACCESS METHODS ############################ 

def get_access_methods (
      username = username,
      password = password,
      host = host
      ):
  """
  This Python function access method info `Access Method`

  == Parameters ==

  None

  """
  credentials = f"{username}:{password}"
  encoded_credential = base64.b64encode(credentials.encode()).decode()
  
  all_cospaces = get_cospaces_list()
  all_cospace_id_list = []

  for coSpace in all_cospaces:
    all_cospace_id_list.append(coSpace['@id'])

  # Check Access Method

  headers = {
    'Content-Type': 'application/json',
    'Authorization': encoded_credential
  }

  cospace_list_that_has_access_method = []
  access_method_list = []

  for cospaceid in all_cospace_id_list:

    getAccessMethod_url =  f"https://{host}:{port}/api/v1/coSpaces/{cospaceid}/accessMethods"

    response = requests.get(url=getAccessMethod_url,
                            auth= HTTPBasicAuth(username, password),
                            headers=headers,
                            verify=False
                            )

    if response.status_code == 200:
        get_access_method = xmltodict.parse(response.content)
        number_of_access_methods = int(get_access_method['accessMethods']['@total'])
        if number_of_access_methods > 0:
           access_method_id = get_access_method['accessMethods']['accessMethod']['@id']
           print (f"this cospace with id {cospaceid} has access method that is {access_method_id}")
           # get info and append lists
           cospace_list_that_has_access_method.append(cospaceid)
           access_method_list.append(access_method_id)
        else :
           print (f"this cospace with id {cospaceid} has not access method")

    else:
        print (f'error is occured {response.status_code}')
    cospaceid_access_method_zip = zip (cospace_list_that_has_access_method, access_method_list)

    return cospaceid_access_method_zip
    
############################ DELETE ACCESS METHOD ############################ 

def delete_access_methods (
      cospaceid,
      access_method_id,
      username = username,
      password = password,
      host = host,
      port = port
      ):
  """
  This Python function delete access method

    == Parameters ==

    cospaceid (mandatory)<br>
    access_method_id (mandatory)


  """

  credentials = f"{username}:{password}"
  encoded_credential = base64.b64encode(credentials.encode()).decode()

  # Delete Access Method

  headers = {
    'Content-Type': 'application/json',
    'Authorization': encoded_credential
  }
  deleteAccessMethod_url =  f"https://{host}:{port}/api/v1/coSpaces/{cospaceid}/accessMethods/{access_method_id}"


  response = requests.delete(url=deleteAccessMethod_url,
                          auth= HTTPBasicAuth(username, password),
                          headers=headers,
                          verify=False
                          )
  if response.status_code == 200:
      print (f'Access Method {access_method_id} deleted successfully')
  else:
      print (f'error is occured {response.status_code}')
