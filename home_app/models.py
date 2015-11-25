# coding=utf-8

from django.db import models

# Create your models here.
class HostInfo(models.Model):
    hostname = models.CharField(u'主机名', max_length=64, primary_key=True)
    memory = models.CharField(u'内存', max_length=1024, blank=False)
    disk = models.CharField(u'磁盘', max_length=1024, blank=False)
    cpu = models.CharField(u'Cpu', max_length=1024, blank=False)
    os = models.CharField(u'OS', max_length=1024, blank=False)
    ip = models.CharField(u'IP', max_length=64, blank=True)

    class Meta:
        verbose_name_plural = u'主机信息'

class Monitoring_data(models.Model):
    CHOICE_TYPE = (
        ('cpu', 'cpu'),
        ('diskio', 'diskio'),
        ('memory', 'memory'),
        ('network', 'network'),
    )
    hostname = models.ForeignKey(HostInfo)
    data_date = models.DateField(u'收集时间')
    type = models.CharField(u'数据类型', choices=CHOICE_TYPE, max_length=16)
    data = models.CharField(u'数据', max_length=1024, blank=False, default='')

    class Meta:
        verbose_name_plural = u'监控数据'