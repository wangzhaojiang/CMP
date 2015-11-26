# coding=utf-8
# __author__ = 'JakeyWang'
# 主节点收集数据 写入数据库
import pika
import json
import ConfigParser
import MySQLdb
import datetime
from log import Logger

cf = ConfigParser.ConfigParser()
cf.read('conf')
ip = cf.get('master', 'ip')


def write_sql(data):
    conn = MySQLdb.connect(
        host=ip,
        user='root',
        passwd='123',
        db='CMP',
        charset='utf8',
    )
    cursor = conn.cursor()
    print 'hello'
    if data['type'] == 'hostinfo':
        sql = "select * from home_app_hostinfo where hostname='%s'" % data['data']['hostname']
        result = cursor.execute(sql)
        if len(cursor.fetchall()) == 0:
            sql = "insert into home_app_hostinfo(hostname, os, memory, cpu, ip, disk, update_time) values(%s, %s, %s, %s, %s, %s, %s)"
            param = (
                data['data']['hostname'],
                json.dumps(data['data']['os']),
                json.dumps(data['data']['memory']),
                json.dumps(data['data']['cpu']),
                json.dumps(data['data']['ip']),
                json.dumps(data['data']['disk']),
                datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                  )
            cursor.execute(sql, param)
        else:
            sql = "update home_app_hostinfo set os=%s, memory=%s, cpu=%s, disk=%s, ip=%s, update_time=%s where hostname=%s"
            param = (
                json.dumps(data['data']['os']),
                json.dumps(data['data']['memory']),
                json.dumps(data['data']['cpu']),
                json.dumps(data['data']['disk']),
                json.dumps(data['data']['ip']),
                datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                data['data']['hostname']
            )
            cursor.execute(sql, param)

    else:
        sql = 'insert into home_app_monitoring_data(data_date, data, type, hostname_id) values(%s, %s, %s, %s)'
        param = (
            datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            json.dumps(data['data']),
            data['type'],
            data['hostname'],
        )
        print param
        cursor.execute(sql, param)

    cursor.close()
    conn.commit()


def callback(ch, method, properties, body):
    print " [x] %r" % (body,)
    data = json.loads(body)
    print data
    write_sql(data)


try:
    connection = pika.BlockingConnection(pika.ConnectionParameters(
            host='localhost'))
    channel = connection.channel()

    channel.exchange_declare(exchange='logs',
                             type='fanout')
except Exception, e:
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