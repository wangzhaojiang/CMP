# coding=utf-8
# __author__ = 'JakeyWang'


def get_mem_rate():
    with open("/proc/meminfo", "r") as f:
        mem_total = float(f.readline().split()[1])
        mem_free = float(f.readline().split()[1])
        mem_used_rate = float("%0.3f" % ((mem_total - mem_free) / mem_total))
        return mem_used_rate

if __name__ == "__main__":
    result = get_mem_rate()
    print result
