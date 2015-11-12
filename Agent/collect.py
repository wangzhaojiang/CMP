# coding=utf-8
# __author__ = 'JakeyWang'
import sys
from utils import *


def data_tran(data):
    

def execmd(cmd):
    global data
    try:
        if cmd == "cpu":
            data[cmd] = get_cpu_rate()
        elif cmd == "memory":
            data[cmd] = get_mem_rate()
        elif cmd == "diskio":
            data[cmd] = get_diskio_rate()
        elif cmd == "network":
            print get_net_rate()
    except Exception, e:
        pass
        print e
        # todo: Log



if __name__ == "__main__":
    if sys.argv[1]:
        category = sys.argv[1]
