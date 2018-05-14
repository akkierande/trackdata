from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import url,include
from . import views
from .views import get_data,HomeView,DisplayView,myexport


urlpatterns = [
    url(r'^$',views.index,name='index'),
    #Project/1/
    url(r'^userprofile/$', views.userprofile, name='profile'),
    url(r'^userprofile/avatars/', include('avatar.urls')),
    url(r'^userprofile/edit/$',views.employee_details, name='employee_form'),

    url(r'^images/$', views.Image_Table.as_view(), name='images'),
    url(r'^images/(?P<pk>\d+)/$', views.imageView, name='image'),

    url(r'^article/$', views.articleView, name='article'),
    #url(r'^images/chart1/$', DisplayView.as_view(), name='chart'),
    url(r'^images/chart/(?P<pk>\d+)/$', views.get_data, name='chart'),
    url(r'^images/chart/$', DisplayView.as_view(), name='graphs'),
    #url(r'^images/data/$', get_data, name='data'),
    #url(r'^images/chart/data/$', ChartData.as_view()),
    url(r'^assign/$', views.Assign_Table.as_view(), name='assignment'),

    url(r'^packages/$', views.Package_Table.as_view(), name='packages'),
    url(r'^projects/$', views.Project_Table.as_view(), name='projects'),
    url(r'^checkout/$', views.Checkout_Table.as_view(), name='checkout'),

    url(r'^checkout/(?P<pk>\d+)/$', views.checkoutimage),
    url(r'^checkout/add/(?P<pk>\d+)/$', views.addCheckout, name='add_checkout'),
    url(r'^checkout/edit/(?P<pk>\d+)/$', views.editCheckout, name='edit_checkout'),
    #url(r'^packages/delete/(?P<pk>\d+)/$', views.package_delete, name='package_delete'),
    url(r'^messages/', include('django_messages.urls')),
    url(r'^myexport/$', myexport, name='myexport'),
    url(r'^items/(?P<pk>\d+)/$',views.ItemListView,name='item'),
    url(r'^items/edit/(?P<pk>\d+)/$', views.ItemUpdateView, name='update'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)