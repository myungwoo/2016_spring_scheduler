"""scheduler URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin

from scheduler.views import views_static_serve
from main.views import *

urlpatterns = [
    url(r'^admin/', admin.site.urls),

    url(r'^$', member_list),
    url(r'^schedule/$', schedule_list),
    url(r'^meeting/$', meeting_list),

    url(r'^static/(?P<path>.*)$', views_static_serve),
]
