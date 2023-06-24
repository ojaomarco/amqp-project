import pika
from util.csv_handler import csv_to_json
import json

connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
channel = connection.channel()
channel.queue_declare(queue='transacoes.financeiras')

csv_path = "util/transacoes.csv"

transaction_json= csv_to_json(csv_path)

for transaction in transaction_json :
    channel.basic_publish(exchange='',
                         routing_key='transacoes.financeiras',
                         body=json.dumps(transaction))   
    print("Transação enviada...")


connection.close()