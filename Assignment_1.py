import adal
import requests
import pandas as pd
from json import loads
import json


authentication_endpoint = 'https://login.microsoftonline.com/'
resource  = 'https://management.core.windows.net/'

# get an Azure access token using the adal library
context = adal.AuthenticationContext(authentication_endpoint + 'eff7f985-dc58-4935-a906-050609be85c3')
token_response = context.acquire_token_with_client_credentials(resource, 'f2642234-880a-465f-bf1a-7fc31130f2fd', 'Ld++kH96y5SHXmiGUkdTex44MvOokxrHfXsRemfbL8c=')

access_token = token_response.get('accessToken')

List_VM = 'https://management.azure.com/subscriptions/64caccf3-b508-41e7-92ed-d7ed95b32621/providers/Microsoft.Compute/virtualMachines?api-version=2017-12-01'

headers = {"Authorization": 'Bearer ' + access_token}
json_output = requests.get(List_VM,headers=headers).json()

#print(json_output)

text_json_list_VM = json.dumps(json_output)

d1 = json.dumps(json.loads(text_json_list_VM))


df=pd.read_json(d1)
print(df)
df.to_csv('results_list_VM.csv')


metric = 'https://management.azure.com/64caccf3-b508-41e7-92ed-d7ed95b32621/providers/microsoft.insights/metrics?api-version=2017-05-01-preview&timespan=2018-06-01/2018-07-012018-06-27&interval=PT256H&metric=Percentage CPU'


headers = {"Authorization": 'Bearer ' + access_token}
json_output1 = requests.get(metric,headers=headers).json()

#print(json_output)

text_json_metric = json.dumps(json_output1)
print("ghay")
df1=pd.read_json(text_json_metric)
print(df1)
df.to_csv('results_metric.csv')



