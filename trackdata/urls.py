"""trackdata URL Configuration

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
from django.conf.urls import url,include
from django.contrib import admin
from trackdata import views as track_views
from django.contrib.auth import views

urlpatterns = [
    url(r'^$', track_views.index, name='index'),
    url(r'^admin/', admin.site.urls),
    url(r'^accounts/', include('django.contrib.auth.urls')),
    url(r'^accounts/login/', include('django.contrib.auth.urls'),{'next_page': '/login/'}),
    url(r'^accounts/logout/',track_views.logout_view),
    url(r'^register/$', track_views.register, name='register'),
    url(r'^tracksheet/',include('tracksheet.urls')),

]
