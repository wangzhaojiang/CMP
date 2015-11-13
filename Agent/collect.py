# coding=utf-8
# __author__ = 'JakeyWang'
# 采集数据 发送数据
import sys
import pika
import json
from utils import *


def data_tran(message):
    connection = pika.BlockingConnection(pika.ConnectionParameters(
            host='10.0.0.100'))
    channel = connection.channel()

    channel.exchange_declare(exchange='logs',
                             type='fanout')

    channel.basic_publish(exchange='logs',
                          routing_key='',
                          body=message)
    print " [x] Sent %r" % (message,)
    # todo: Log
    connection.close()


def execmd(cmd):
    result = {}
    result['type'] = cmd
    # 数据统一用json串发送
    try:
        if cmd == "cpu":
            result['data'] = get_cpu_rate()
        elif cmd == "memory":
            result['data'] = get_mem_rate()
        elif cmd == "diskio":
            result['data'] = get_diskio_rate()
        elif cmd == "network":
            result['data'] = get_net_rate()
        elif cmd == 'hostinfo':
            result['data'] = get_host_info()
    except Exception, e:
        pass
        print e
        # todo: Log

    return result


if __name__ == "__main__":
    if sys.argv[1] and sys.argv[1] in ['cpu', 'memory', 'diskio', 'network', 'hostinfo']:
        result = execmd(sys.argv[1])
        data_tran(json.dumps(result))
    else:
        # todo: Log error param
        pass

