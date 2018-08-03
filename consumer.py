# example_consumer.py
import pika, os, time
import adal
import requests
import pandas as pd
import json
from json import loads


def function(msg):
  print(" processing")
  print(" Received %r" % msg)



  authentication_endpoint = 'https://login.microsoftonline.com/'
  resource = 'https://management.core.windows.net/'

  # get an Azure access token using the adal library
  context = adal.AuthenticationContext(authentication_endpoint + 'eff7f985-dc58-4935-a906-050609be85c3')
  token_response = context.acquire_token_with_client_credentials(resource, 'f2642234-880a-465f-bf1a-7fc31130f2fd',
                                                                 'Ld++kH96y5SHXmiGUkdTex44MvOokxrHfXsRemfbL8c=')

  access_token = token_response.get('accessToken')

  List_VM = msg

  headers = {"Authorization": 'Bearer ' + access_token}
  json_output = requests.get(List_VM, headers=headers).json()

  # print(json_output)

  text_json_list_VM = json.dumps(json_output)

  d1 = json.dumps(json.loads(text_json_list_VM))

  df = pd.read_json(d1)
  print(df)
  df.to_csv('results_list_VM.csv')

  metric = 'https://management.azure.com//subscriptions/64caccf3-b508-41e7-92ed-d7ed95b32621/resourceGroups/LONG-WT20RG/providers/Microsoft.Compute/virtualMachines/wint20ser2/providers/microsoft.insights/metrics?api-version=2017-05-01-preview&timespan=2018-06-01/2018-07-20&interval=PT1H&metric=Percentage CPU'

  headers = {"Authorization": 'Bearer ' + access_token}
  json_output1 = requests.get(metric, headers=headers).json()

  # print(json_output)

  text_json_metric = json.dumps(json_output1)

  df1 = pd.read_json(text_json_metric)
  print(df1)
  df1.to_csv('results_metric.csv')

#  time.sleep(5) # delays for 5 seconds
  print(" Processing finished");
  return;

# Access the CLODUAMQP_URL environment variable and parse it (fallback to localhost)
url = os.environ.get('CLOUDAMQP_URL', 'amqp://hgtgexcy:rXte959Mz0_E57VOqlI5_1YkWzLR86Tp@lion.rmq.cloudamqp.com/hgtgexcy')
params = pika.URLParameters(url)
connection = pika.BlockingConnection(params)
channel = connection.channel() # start a channel
channel.queue_declare(queue='process1') # Declare a queue

# create a function which is called on incoming messages
def callback(ch, method, properties, body):
  process_function(body)

# set up subscription on the queue
channel.basic_consume(callback,
  queue='process1',
  no_ack=True)

# start consuming (blocks)
channel.start_consuming()
connection.close()
