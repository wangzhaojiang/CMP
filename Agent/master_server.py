# coding=utf-8
# __author__ = 'JakeyWang'
import pika
import json

connection = pika.BlockingConnection(pika.ConnectionParameters(
        host='localhost'))
channel = connection.channel()

channel.exchange_declare(exchange='logs',
                         type='fanout')

result = channel.queue_declare(exclusive=True)
queue_name = result.method.queue

channel.queue_bind(exchange='logs',
                   queue=queue_name)

print ' [*] Waiting for logs. To exit press CTRL+C'

def callback(ch, method, properties, body):
    # todo: 写入mysql并纪录日志
    print " [x] %r" % (body,)
    data = json.loads(body)
    print data

channel.basic_consume(callback,
                      queue=queue_name,
                      no_ack=True)

channel.start_consuming()