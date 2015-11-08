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
        f.read()
        f.read()
        for line in f:
            if line:
                network_card = line.split(":")[0]
                data_network = line.split(":")[1].split()
                data[network_card] = data_network

    return data

def caculate(data_old, data_new):
    net = {}
    for key in data_old.fromkeys():
        net[key] = [data_new[key][0] - data_old[key][0], data_new[key][8] - data_new[key][8]]


def get_net_rate():
    global network_ti
    data_old = getdata()
    time.sleep(network_ti)
    data_new = getdata()
    net = caculate(data_old, data_new)
    return net