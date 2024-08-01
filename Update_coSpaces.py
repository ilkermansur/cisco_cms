import requests
import urllib3
import xmltodict
from requests.auth import HTTPBasicAuth


urllib3.disable_warnings()

# Give credential

username = 'admin'
password = 'admin'

# Get CoSpaces

url = "https://192.168.91.152:443/api/v1/coSpaces/"

headers = {
  'Content-Type': 'application/json'
}

response = requests.get(url,
                        auth= HTTPBasicAuth(username, password),
                        headers=headers,
                        verify=False
                        )

# convert xml to json

dict_data = xmltodict.parse(response.content)

# CoSpace list with all features

cospace_list_parameters = dict_data['coSpaces']['coSpace']

# Update CoSpace with tenant_id

def add_tenant_to_cospace ():
    """
    The function `add_tenant_to_cospace` iterates through a list of users and assigns a specific tenant
    ID based on the prefix of the call ID.
    """

    for user in cospace_list_parameters:

        call_id = user['callId']

        if call_id.startswith('25'):
            cospace_id = user['@id']
            tenant_id = '7475dd16-1029-4bde-94ed-f249683146d8'
            mod_url = url + cospace_id
            payload = f"tenant={tenant_id}"
            response = requests.put(mod_url,
                                    auth= HTTPBasicAuth(username, password),
                                    headers=headers,
                                    data=payload,
                                    verify=False
                                    )
            if response.status_code == 200:
                user_space = user['name']

                with open ("logs.txt", "a") as f:
                    f.write (f'{user_space} was uptaded with new {tenant_id}\n')
               
            else:
                with open ("logs.txt", "a") as f:
                    f.write (f'error is occured {response.status_code}\n')

        elif call_id.startswith('35'):
            cospace_id = user['@id']
            tenant_id = '71fc7729-e249-427d-9350-38da5f0e2a11'
            mod_url = url + cospace_id
            payload = f"tenant={tenant_id}"
            response = requests.put(mod_url,
                                    auth= HTTPBasicAuth(username, password),
                                    headers=headers,
                                    data=payload,
                                    verify=False
                                    )
            if response.status_code == 200:
                with open ("logs.txt", "a") as f:
                    f.write (f'{user_space} was uptaded with new {tenant_id}\n')
               
            else:
                with open ("logs.txt", "a") as f:
                    f.write (f'error is occured {response.status_code}\n')

        else:
            print ("No need to UPDATE")

add_tenant_to_cospace()

