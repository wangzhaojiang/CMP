from django.shortcuts import render, render_to_response
from models import *
import json
from django.http import HttpResponse

# Create your views here.


def base_render():
    host_list = []
    for item in HostInfo.objects.all():
        host_list.append(item.hostname)
    return host_list

def index(request):
    return render(request, 'home_app/base.html', {'host_list': base_render()})


def host(request):
    render_param = {}
    render_param['host_list'] = base_render()
    hostname = request.GET.get('host', '')
    render_param['host'] = hostname
    hostinfo = HostInfo.objects.filter(hostname=hostname)[0]
    render_param['cpu_core'] = json.loads(hostinfo.cpu)['cpu_core']
    render_param['os'] = hostinfo.os
    render_param['memory'] = json.loads(hostinfo.memory)['mem_total']
    render_param['disk'] = hostinfo.disk
    render_param['ip'] = hostinfo.ip
    return render_to_response('home_app/host.html', render_param)

