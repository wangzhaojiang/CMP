# coding=utf-8
# __author__ = 'JakeyWang'
from django.http import HttpResponse
from models import *
from django.db.models import Q
import json
import time


# def ajax_monitoring_init_data(request):
#     xyaxis = []
#     data = {}
#     monitor_type = request.GET.get('type')
#     hostname = request.GET.get('host')
#     sql_result = Monitoring_data.objects.order_by('data_date').filter(type=monitor_type, hostname=hostname)
#     if monitor_type == 'cpu' or monitor_type == 'memory':
#         for item in sql_result:
#             xyaxis.append([time.mktime(item.data_date.timetuple())*1000, float(item.data)])
#
#         data = {'result': True, 'data': xyaxis}
#     # elif monitor_type == 'memory':
#     #     for item in sql_result:
#     #         xyaxis.
#     return HttpResponse(json.dumps(data))

def ajax_monitoring_init_data(request):
    xyaxis = {'cpu': [], 'memory': [], 'diskio': {'pgpgin': [], 'pgpgout': []}}
    hostname = request.GET.get('host')
    if hostname:
        for item in Monitoring_data.objects.order_by('data_date').filter(Q(hostname=hostname) & Q(type='cpu') | Q(type='memory')):
            if item.type == 'cpu':
                xyaxis['cpu'].append([time.mktime(item.data_date.timetuple())*1000, float(item.data)])
            else:
                xyaxis['memory'].append([time.mktime(item.data_date.timetuple())*1000, float(item.data)])
        for item in Monitoring_data.objects.order_by('data_date').filter(Q(hostname=hostname) & Q(type='diskio')):
            disk_data = json.loads(item.data)
            xyaxis['diskio']['pgpgin'].append([time.mktime(item.data_date.timetuple()) * 1000, float(disk_data['pgpgin'])])
            xyaxis['diskio']['pgpgout'].append([time.mktime(item.data_date.timetuple()) * 1000, float(disk_data['pgpgout'])])

        data = {'result': True, 'data': xyaxis}
    else:
        data = {'result': False, 'data': xyaxis}
    return  HttpResponse(json.dumps(data))
