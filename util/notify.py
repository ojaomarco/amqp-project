import pika
import json

connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
channel = connection.channel()
channel.exchange_declare(exchange='transacoes.suspeitas', exchange_type='fanout')

def notify_authorities(message):
    channel.basic_publish(exchange='transacoes.suspeitas',
                        routing_key='',
                        body=message)
    print("Notified authorities...")
