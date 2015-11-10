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
diskio_ti = float(cf.get("collecting time interval", "diskio_ti"))
network_ti = float(cf.get("collecting time interval", "network_ti"))


# Cpu
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


# Memory
def get_mem_rate():
    with open("/proc/meminfo", "r") as f:
        mem_total = float(f.readline().split()[1])
        mem_free = float(f.readline().split()[1])
        mem_used_rate = float("%0.3f" % ((mem_total - mem_free) / mem_total))
        return mem_used_rate


# Diskio
def get_ddata():
    data = {}
    with open("/proc/vmstat") as f:
        for line in f:
            if line.strip():
                content = line.split()
                if content[0] in ["pgpgin", "pgpgout"]:
                    data[content[0]] = float(content[1])
            if len(data) == 2:
                break
    return data


def get_diskio_rate():
    global diskio_ti
    data_old = get_ddata()
    time.sleep(diskio_ti)
    data_new = get_ddata()
    pgpgin_rate = (data_new["pgpgin"] - data_old["pgpgin"]) / diskio_ti
    pgpgout_rate = (data_new["pgpgout"] - data_old["pgpgout"]) / diskio_ti

    return {"pgpgin": float("%0.3f" % pgpgin_rate), "pgpgout": float("%0.3f" % pgpgout_rate)}


def get_ndata():
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


def caculate_n(data_old, data_new):
    global network_ti
    net = {}
    for key in data_old.iterkeys():
        # net[key] = (
        #    # 此处居然转化不了精度！！！
        #    round((float(data_new[key][0]) - float(data_old[key][0])) / network_ti, 1),
        #    round((float(data_new[key][8]) - float(data_old[key][8])) / network_ti, 1)
        # )
        tra = round((float(data_new[key][8]) - float(data_old[key][8])) / network_ti, 1)
        rec = round((float(data_new[key][0]) - float(data_old[key][0])) / network_ti, 1)
        print rec, tra
        net[key] = (rec, tra)
    print net
    return net


def get_net_rate():
    global network_ti
    data_old = get_ndata()
    time.sleep(network_ti)
    data_new = get_ndata()
    net = caculate_n(data_old, data_new)
    return net
