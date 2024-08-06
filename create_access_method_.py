import requests
import urllib3
import xmltodict
import base64
from requests.auth import HTTPBasicAuth
import random
import re

# Disable ssl warning

urllib3.disable_warnings()

# Give credential and convert base64

username = 'admin'
password = 'admin'
credentials = f"{username}:{password}"
encoded_credential = base64.b64encode(credentials.encode()).decode()

headers = {
  'Content-Type': 'application/json',
  'Authorization': encoded_credential
}

def getCoSpacesIdList ():
    """
    The function `getCoSpacesIdList` retrieves a list of coSpace IDs by making API requests with
    pagination.
    :return: The function `getCoSpacesIdList` is returning two values: `coSpace_id_list` and
    `all_cospaces`. The `coSpace_id_list` contains a list of IDs for each coSpace retrieved from the
    API, while `all_cospaces` contains a list of all coSpaces data retrieved from the API.
    """

    coSpace_id_list = []
    offset = 0
    all_cospaces = []

    while True:

        # Create coSpaceList

        base_url = "https://192.168.91.152:443/api/v1/coSpaces/"
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

    for cospace in all_cospaces:
        cospace_id = cospace['@id']
        coSpace_id_list.append(cospace_id)
    
    return coSpace_id_list,all_cospaces

def createAccessMethod ():
    """
    The function `createAccessMethod` generates random call IDs and creates access methods for CoSpaces
    using the generated call IDs and URIs.
    """

    coSpace_id_list, all_cospaces = getCoSpacesIdList()

    rnd_callId_list = []
    uri_list = []

    number_of_callids = len(coSpace_id_list)

    i = number_of_callids
    t = 0

    while  t < i :

        rnd_callId = random.randint(100000000, 999999999)

        if rnd_callId in rnd_callId_list:
            rnd_callId = random.randint(100000000, 999999999)
        else:
            rnd_callId_list.append(rnd_callId)
            t = t + 1

    for cospace in all_cospaces:
        if 'uri' in cospace:
            uri = cospace['uri']
            access_method_uri = re.sub(r'\..*', '',uri)
            uri_list.append(access_method_uri)

    uri_callId_cospace_id_list = zip(uri_list, rnd_callId_list, coSpace_id_list)

    for uri, call_id, cospace_id in uri_callId_cospace_id_list:
        
        createAccessMethod_url =  f"https://192.168.91.152:443/api/v1/coSpaces/{cospace_id}/accessMethods"

        payload = {'uri' : uri,
                'callId' : call_id}
        
        print (uri, call_id, cospace_id, createAccessMethod_url, sep = '\n')

        response = requests.post(url=createAccessMethod_url,
                            auth= HTTPBasicAuth(username, password),
                            headers=headers,
                            data = payload,
                            verify=False
                            )
        if response.status_code == 200:
            print ('success')
            print ('x' * 100)
        else:
            print (f'Error is occured : {response.status_code}')
            print ('x' * 100)

createAccessMethod()
