# coding=utf-8
# __author__ = 'JakeyWang'

import ConfigParser
import time

cf = ConfigParser.ConfigParser()
# file_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + "/conf"
# cf.read("file_dir")
# print file_dir
cf.read("conf")
cpu_ti = float(cf.get("collecting time interval", "cpu_ti"))


def get_cdata():
    with open("/proc/stat", "r") as f:
        data = f.readline().split()[1:8]
        for i in range(7):
            data[i] = float(data[i])
    return data


def caculate_c(data_old, data_new):
    co_ttime = reduce(lambda x, y: x + y, data_old)
    cn_ttime = reduce(lambda x, y: x + y, data_new)
    co_used = data_old[0] + data_old[1] + data_old[2] + data_old[4] + data_old[5]
    cn_uesd = data_new[0] + data_new[1] + data_new[2] + data_new[4] + data_new[5]

    return (cn_uesd - co_used) / (cn_ttime - co_ttime)


def get_cpu_rate():
    global cpu_ti
    data_old = get_cdata()
    time.sleep(cpu_ti)
    data_new = get_cdata()
    cpu_rate = float("%0.3f" % (caculate_c(data_old, data_new) * 100))
    return cpu_rate

if __name__ == "__main__":
    result = get_cpu_rate()
    print result
