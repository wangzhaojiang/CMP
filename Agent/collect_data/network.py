# coding=utf-8
# __author__ = 'JakeyWang'

import ConfigParser
import time

cf = ConfigParser.ConfigParser()
cf.read("../conf")
network_ti = float(cf.get("collecting time interval", "network_ti"))


def getdata():
    data = {}
    with open("/proc/net/dev", "r") as f:
        f.next()
        f.next()
        for line in f:
            if line:
                network_card = line.split(":")[0]
                data_network = line.split(":")[1].split()
                data[network_card] = data_network

    return data

def caculate(data_old, data_new):
    global network_ti
    net = {}
    for key in data_old.iterkeys():
       # net[key] = (
       #     # 此处居然转化不了精度！！！
       #     round((float(data_new[key][0]) - float(data_old[key][0])) / network_ti, 1),
       #     round((float(data_new[key][8]) - float(data_old[key][8])) / network_ti, 1)
       # )
	rec = round((float(data_new[key][0]) - float(data_old[key][0])) / network_ti, 1)
	tra = round((float(data_new[key][8]) - float(data_old[key][8])) / network_ti, 1)
	net[key] = (rec, tra)
	print rec,tra

    return net


def get_net_rate():
    global network_ti
    data_old = getdata()
    time.sleep(network_ti)
    data_new = getdata()
    net = caculate(data_old, data_new)
    return net

if __name__ == "__main__":
    result = get_net_rate()
    print result
