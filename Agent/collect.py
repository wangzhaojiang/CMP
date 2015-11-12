# coding=utf-8
# __author__ = 'JakeyWang'
from utils import *
import threading

data = {}


def execmd(cmd):
    try:
        if cmd == "cpu":
            data[cmd] = get_cpu_rate()
        elif cmd == "memory":
            data[cmd] = get_mem_rate()
        elif cmd == "diskio":
            data[cmd] = get_diskio_rate()
        elif cmd == "network":
            data[cmd] == get_net_rate()

    except Exception, e:
        pass
        # todo: Log

if __name__ == "__main__":
    cmds = ['cpu', 'diskio', 'memory', 'network']
    threads = []
    # todo: Log -- 开始采集监控数据
    print "开始采集监控数据"
    for cmd in cmds:
        th = threading.Thread(targer = execmd, args=(cmd,))
        th.start()
        threads.append(th)

    for th in threads:
        th.join()

    # todo: Log -- 采集结束
    print "采集结束"

    #rabbitmq to do