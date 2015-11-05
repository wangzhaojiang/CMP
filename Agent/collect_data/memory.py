# coding=utf-8
# __author__ = 'JakeyWang'


def get_mem_rate():
    with open("/proc/meminfo", "r") as f:
        mem_total = float(f.readline().split()[1])
        mem_free = float(f.readline().split()[1])
        mem_used_rate = (mem_total - mem_free) / mem_total
        return mem_used_rate
