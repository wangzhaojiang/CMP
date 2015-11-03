#coding=utf-8
#__author__ = 'JakeyWang'


def get_mem_rate():
    file_mem = open("/proc/meminfo", "r")
    mem_total = 0
    try:
        mem_total = float(file_mem.readline().split()[1])
        mem_free = float(file_mem.readline().split()[1])
        file_mem.close()

        mem_used_rate = (mem_total - mem_free) / mem_total
    except Exception, e:
        # todo: LOG
        pass
    finally:
        return mem_used_rate
