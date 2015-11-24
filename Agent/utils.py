# coding=utf-8
# __author__ = 'JakeyWang'


import ConfigParser
import time
import os
import psutil
import platform

cf = ConfigParser.ConfigParser()
# file_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + "/conf"
# cf.read("file_dir")
# print file_dir
cf.read("conf")


#cpu
def get_cpu_rate():
    cpu_ti = float(cf.get("collecting time interval", "cpu_ti"))
    return psutil.cpu_percent(cpu_ti)


#memory
def get_mem_rate():
    return psutil.virtual_memory().percent


#diskio 单位为Kb
def get_diskio_rate():
    diskio_ti = float(cf.get("collecting time interval", "diskio_ti"))
    read_io_old = psutil.disk_io_counters().read_bytes
    write_io_old = psutil.disk_io_counters().write_bytes
    time.sleep(diskio_ti)
    read_io_new = psutil.disk_io_counters().read_bytes
    write_io_new = psutil.disk_io_counters().write_bytes
    pgpgin_rate = (float(write_io_new) - write_io_old) / diskio_ti / 1024
    pgpgout_rate = (float(read_io_new) - read_io_old) / diskio_ti / 1024
    return {"pgpgin": float("%0.3f" % pgpgin_rate), "pgpgout": float("%0.3f" % pgpgout_rate)}


#network
def get_net_rate():
    net = {}
    network_ti = float(cf.get("collecting time interval", "network_ti"))
    rec_old = psutil.net_io_counters().bytes_recv, psutil.net_io_counters().packets_recv
    sen_old = psutil.net_io_counters().bytes_sent, psutil.net_io_counters().packets_sent
    time.sleep(network_ti)
    rec_new = psutil.net_io_counters().bytes_recv, psutil.net_io_counters().packets_recv
    sen_new = psutil.net_io_counters().bytes_sent, psutil.net_io_counters().packets_sent
    net['recv_kbyte'] = round((float(rec_new[0]) - rec_old[0]) / 1024, 1)
    net['recv_packet'] = rec_new[1] - rec_old[1]
    net['send_kbyte'] = round((float(sen_new[0]) - sen_old[0]) / 1024, 1)
    net['send_packet'] = sen_new[1] - sen_old[1]
    return net

def get_host_info(): #os hostname cpu memory disk
    host_info = {}
    host_info['memory'] = {'mem_total': float(psutil.virtual_memory().total) / 1024 / 1024, 'mem_used': psutil.virtual_memory().percent}
    host_info['hostname'] = platform.node()
    host_info['os'] = ' '.join(platform.linux_distribution()) + ' ' + ' '.join(platform.architecture())
    host_info['cpu'] = {'cpu_percent': psutil.cpu_percent(), 'cpu_core': psutil.cpu_count()}
    host_info['disk'] = []
    for iterm in psutil.disk_partitions():
        part = psutil.disk_usage(iterm[1])
        data = iterm[1] + ' ' + str(float(part[0]) / 1024 / 1024) + ' ' + str(part[3])
        host_info['disk'].append(data)
    return host_info


# # Cpu
# def get_cdata():
#     with open("/proc/stat", "r") as f:
#         data = f.readline().split()[1:8]
#         for i in range(7):
#             data[i] = float(data[i])
#     return data
#
#
# def caculate_c(data_old, data_new):
#     co_ttime = reduce(lambda x, y: x + y, data_old)
#     cn_ttime = reduce(lambda x, y: x + y, data_new)
#     co_used = data_old[0] + data_old[1] + data_old[2] + data_old[4] + data_old[5]
#     cn_uesd = data_new[0] + data_new[1] + data_new[2] + data_new[4] + data_new[5]
#
#     return (cn_uesd - co_used) / (cn_ttime - co_ttime)
#
#
# def get_cpu_rate():
#     global cpu_ti
#     data_old = get_cdata()
#     time.sleep(cpu_ti)
#     data_new = get_cdata()
#     cpu_rate = float("%0.3f" % (caculate_c(data_old, data_new) * 100))
#     return cpu_rate
#
#
# # Memory
# def get_mem_rate():
#     with open("/proc/meminfo", "r") as f:
#         mem_total = float(f.readline().split()[1])
#         mem_free = float(f.readline().split()[1])
#         mem_used_rate = float("%0.3f" % ((mem_total - mem_free) / mem_total))
#         return mem_used_rate
#
#
# # Diskio
# def get_ddata():
#     data = {}
#     with open("/proc/vmstat") as f:
#         for line in f:
#             if line.strip():
#                 content = line.split()
#                 if content[0] in ["pgpgin", "pgpgout"]:
#                     data[content[0]] = float(content[1])
#             if len(data) == 2:
#                 break
#     return data
#
#
# def get_diskio_rate():
#     global diskio_ti
#     data_old = get_ddata()
#     time.sleep(diskio_ti)
#     data_new = get_ddata()
#     pgpgin_rate = (data_new["pgpgin"] - data_old["pgpgin"]) / diskio_ti
#     pgpgout_rate = (data_new["pgpgout"] - data_old["pgpgout"]) / diskio_ti
#
#     return {"pgpgin": float("%0.3f" % pgpgin_rate), "pgpgout": float("%0.3f" % pgpgout_rate)}
#
#
# def get_ndata():
#     data = {}
#     with open("/proc/net/dev", "r") as f:
#         f.next()
#         f.next()
#         for line in f:
#             if line:
#                 network_card = line.split(":")[0]
#                 data_network = line.split(":")[1].split()
#                 data[network_card] = data_network
#
#     return data
#
#
# def caculate_n(data_old, data_new):
#     global network_ti
#     net = {}
#     for key in data_old.iterkeys():
#         # net[key] = (
#         #    # 此处居然转化不了精度！！！
#         #    round((float(data_new[key][0]) - float(data_old[key][0])) / network_ti, 1),
#         #    round((float(data_new[key][8]) - float(data_old[key][8])) / network_ti, 1)
#         # )
#         tra = round((float(data_new[key][8]) - float(data_old[key][8])) / network_ti, 1)
#         rec = round((float(data_new[key][0]) - float(data_old[key][0])) / network_ti, 1)
#         net[key] = (rec, tra)
#     return net
#
#
# def get_net_rate():
#     global network_ti
#     data_old = get_ndata()
#     time.sleep(network_ti)
#     data_new = get_ndata()
#     net = caculate_n(data_old, data_new)
#     return net
#
#
# def get_host_info():
#     os_info = {}
#     cpu_info = {}
#     hostname = os.popen("hostname").read()
#     os_info['kernel'] = os.popen("uname -r").read()
#     os_info['os'] = os.popen("head -n 1 /etc/issue")
#     memtotal = 0
#     with open("/proc/meminfo") as f:
#         memtotal = int(f.readline().split()[1])
#     cpu_cmd = os.popen("cat /proc/cpuinfo | grep name | cut -f2 -d: | uniq -c").read().strip().split(' ', 1)
#     cpu_info['core'] = cpu_cmd[0]
#     cpu_info['name'] = cpu_cmd[1]
#
#    return {'cpu': cpu_info, 'memory': memtotal, 'hostname': hostname}


