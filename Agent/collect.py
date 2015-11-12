# coding=utf-8
# __author__ = 'JakeyWang'
from utils import *
import threading

data = {}


def execmd(cmd):
    global data
    try:
        if cmd == "cpu":
            print 'cpu'
            data[cmd] = get_cpu_rate()
        elif cmd == "memory":
            print 'mem'
            data[cmd] = get_mem_rate()
        elif cmd == "diskio":
            print 'disk'
            data[cmd] = get_diskio_rate()
        elif cmd == "network":
            # todo: 线程无法执行完成！！！
            print 'net'
            print get_net_rate()
            print 'haha'
    except Exception, e:
        pass
        print e
        # todo: Log

if __name__ == "__main__":
    cmds = ['cpu', 'diskio', 'network', 'memory']
    threads = []
    # todo: Log -- 开始采集监控数据
    print "开始采集监控数据"
    for cmd in cmds:
        th = threading.Thread(target = execmd, args=(cmd,))
        th.start()
        threads.append(th)

    for th in threads:
        th.join()

    # todo: Log -- 采集结束
    print "采集结束"
    print data
    #rabbitmq to do
