import pika

connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
channel = connection.channel()
channel.exchange_declare(exchange='transacoes.suspeitas',exchange_type='fanout')
channel.queue_declare(queue='policia.federal', durable=True)
channel.queue_bind(exchange='transacoes.suspeitas',
                   queue='policia.federal')

def callback(ch, method, properties, body):
    print(" [x] Recebida: %r" % body)

channel.basic_consume(queue='policia.federal', on_message_callback=callback)


print('\033[91m [*] Policia Federal aguardando transações... \033[0m')
channel.start_consuming()