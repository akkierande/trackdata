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
from trackdata.views import logout_view
from django.contrib.auth import views
from django.contrib.auth.views import logout
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    url(r'^$', track_views.index, name='index'),


    url(r'^admin/', admin.site.urls),
    url(r'^accounts/', include('django.contrib.auth.urls')),
    url(r'^accounts/login/', include('django.contrib.auth.urls'),{'next_page': '/login/'}),
    url(r'^accounts/logout/$', logout_view, name='logout'),
    #url(r'^accounts/logout/$','django.contrib.auth.views.logout',{'next_page': '/logged_out/'}),
    #url(r'^accounts/logout/',track_views.logout_view,{'next_page': '/logged_out/'}),
    url(r'^register/$', track_views.register, name='register'),
    url(r'^tracksheet/',include('tracksheet.urls')),


]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
