import pika

connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
channel = connection.channel()
channel.exchange_declare(exchange='transacoes.suspeitas',exchange_type='fanout')
channel.queue_declare(queue='policia.federal', durable=False)
channel.queue_bind(exchange='transacoes.suspeitas',
                   queue='policia.federal')

def callback(ch, method, properties, body):
    print("\033[91m [PF]\033[0m Transação: %r" % body.decode('utf-8'))

channel.basic_consume(queue='policia.federal', on_message_callback=callback)


print('\033[91m [*] Policia Federal aguardando transações... \033[0m')
channel.start_consuming()