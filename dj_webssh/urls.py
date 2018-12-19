"""dj_webssh URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
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
from django.http import HttpResponseRedirect
from django.contrib import admin
from project_apps.webssh import views
from django.conf.urls.static import static
from django.conf import settings


def favicon_ico_redirect(request):
    return HttpResponseRedirect('/static/img/favicon.ico')


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', views.login),
    url(r'^login/', views.login),
    url(r'^logout/', views.logout),
    url(r'^index/', views.index),
    url(r'^log/', views.get_log),
    url(r'^host/(?P<user_bind_host_id>\d+)/$', views.connect),
    url(r'^favicon.ico$', favicon_ico_redirect),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
