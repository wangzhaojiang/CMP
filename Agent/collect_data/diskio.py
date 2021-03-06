# coding=utf-8
# __author__ = 'JakeyWang'

import ConfigParser
import time

cf = ConfigParser.ConfigParser()
cf.read("../conf")
diskio_ti = float(cf.get("collecting time interval", "diskio_ti"))


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

if __name__ == "__main__":
    result = get_diskio_rate()
    print result
