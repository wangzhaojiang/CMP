# coding=utf-8
# __author__ = 'JakeyWang'
# 主节点收集数据 写入数据库
import pika
import json
import ConfigParser
from log import Logger

cf = ConfigParser.ConfigParser()
cf.read('conf')
ip = cf.get('master', 'ip')

def callback(ch, method, properties, body):
    # todo: 写入mysql并纪录日志
    print " [x] %r" % (body,)
    data = json.loads(body)
    print data

try:
    connection = pika.BlockingConnection(pika.ConnectionParameters(
            host='localhost'))
    channel = connection.channel()

    channel.exchange_declare(exchange='logs',
                             type='fanout')
except Exception,e:
    Logger.error(e)


result = channel.queue_declare(exclusive=True)
queue_name = result.method.queue

channel.queue_bind(exchange='logs',
                   queue=queue_name)

print ' [*] Waiting for logs. To exit press CTRL+C'

channel.basic_consume(callback,
                      queue=queue_name,
                      no_ack=True)

channel.start_consuming()