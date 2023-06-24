import pika
import time
import json
from util.notify import notify_authorities

connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
channel = connection.channel()
channel.exchange_declare(exchange='transacoes', exchange_type='topic')
channel.queue_declare(queue='transacoes.financeiras')


def callback(ch, method, properties, body):
    ch.basic_ack(delivery_tag=method.delivery_tag)
    print("[x] Recebida %r" % body)

    validate_transaction(body)
    print('[x] Processada...')
    time.sleep(1)
    
channel.basic_qos(prefetch_count=1)     
channel.basic_consume(queue='transacoes.financeiras', on_message_callback=callback, auto_ack=False)


def validate_transaction(transaction_bytes):
    transaction_dict = json.loads(transaction_bytes.decode('utf-8'))
    if(float(transaction_dict["valor"]) > 40000):
        print("\033[93m [*] INFORMANDO RECEITA E POLICIA \033[0m")
        notify_authorities(json.dumps(transaction_dict))

print('Esperando mensagens...')

channel.start_consuming()