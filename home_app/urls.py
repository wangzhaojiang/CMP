# coding=utf-8
# __author__ = 'JakeyWang'
from django.conf.urls import include, url, patterns
from views import *

urlpatterns = [
    # Examples:
    # url(r'^$', 'CMP.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^$', index),
]
