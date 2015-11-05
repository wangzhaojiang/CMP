# coding=utf-8
# __author__ = 'JakeyWang'

import ConfigParser
import time

cf = ConfigParser.ConfigParser()
cf.read("../conf")
diskio_ti = float(cf.get("collecting time interval", "diskio_ti"))

def getdata_diskio():
    with open("/proc/vmstat") as f:
