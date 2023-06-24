import pika
import time
import json
import traceback
from util.notify import notify_authorities

connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
channel = connection.channel()
channel.exchange_declare(exchange='transacoes', exchange_type='topic')
channel.queue_declare(queue='transacoes.financeiras')


def callback(ch, method, properties, body):
    ch.basic_ack(delivery_tag=method.delivery_tag)
    print("[Consumer] Recebida %r" % body.decode('utf-8'))
    try:
        validate_transaction(body)
    except:
        print("\033[93m [*] mensagem ja enviada... \033[0m")
    print('\033[92m[x] Processada... \033[0m')
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