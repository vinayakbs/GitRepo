# example_publisher.py
import pika, os, logging
logging.basicConfig()

# Parse CLODUAMQP_URL (fallback to localhost)
url = os.environ.get('CLOUDAMQP_URL', 'amqp://hgtgexcy:rXte959Mz0_E57VOqlI5_1YkWzLR86Tp@lion.rmq.cloudamqp.com/hgtgexcy')
params = pika.URLParameters(url)
params.socket_timeout = 5

connection = pika.BlockingConnection(params) # Connect to CloudAMQP
channel = connection.channel() # start a channel
channel.queue_declare(queue='pdfprocess1') # Declare a queue
# send a message
msg = 'https://management.azure.com/subscriptions/64caccf3-b508-41e7-92ed-d7ed95b32621/providers/Microsoft.Compute/virtualMachines?api-version=2017-12-01'

channel.basic_publish(exchange='', routing_key='pdfprocess1', body= msg)
print ("[x] Message sent to consumer")
connection.close()