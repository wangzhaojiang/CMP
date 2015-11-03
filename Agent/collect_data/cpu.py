# coding=utf-8
# __author__ = 'JakeyWang'

import ConfigParser
import time

cf = ConfigParser.ConfigParser()
# file_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + "/conf"
# cf.read("file_dir")
# print file_dir
cf.read("../conf")
cpu_ti = cf.get("collecting time interval", "cpu_ti")

def getdata():
    file_stat = open("/proc/stat", "r")
    data = ''
    try:
        data = file_stat.readline().split()[1:8]
        for i in range(7):
            data[i] = int(data[i])
    except Exception, e:
        # todo: LOG
        pass
    finally:
        return data


def caculate(data_old, data_new):
    co_ttime = reduce(lambda x, y: x + y, data_old)
    cn_ttime = reduce(lambda x, y: x + y, data_new)
    co_used = data_old[0] + data_old[1] + data_old[2] + data_old[4] + data_old[5]
    cn_uesd = data_new[0] + data_new[1] + data_new[2] + data_new[4]

    return (cn_uesd - co_used) * 100 / (cn_ttime - co_ttime)

def get_cpu_rate():
    global cpu_ti
    data_old = getdata()
    time.sleep(cpu_ti)
    data_new = getdata()
    cpu_rate = caculate(data_old, data_new)
    return cpu_rate