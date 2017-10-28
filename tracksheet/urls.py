from django.conf.urls import url,include
from . import views


urlpatterns = [
    url(r'^$',views.index,name='index'),
    #Project/1/
    url(r'^userprofile/$', views.userprofile, name='profile'),
    #url(r'^tracksheet/image/(?P<id>\d+)/$', views.imgDetail),
    #url(r'^packages/$', Package_View.as_view(), name='Packages'),
    url(r'^images/$', views.Image_Table.as_view(), name='images'),
    url(r'^images/(?P<pk>\d+)/$', views.imageView, name='image'),
    #url(r'^images/(?P<pk>\d+)/$', views.Checkout_History_Table.as_view(), name='image'),
    #url(r'^checkout/(?P<pk>\d+)/$', views.Checkout, name='Checkout'),

    #url(r'^checkout/(?P<pk>\d+)/$', views.CheckoutView, name='checkout'),
    #url(r'^checkouts/(?P<pk>\d+)/$', views.CheckoutImageListView.as_view()),
    url(r'^checkout/$', views.Checkout_Table.as_view(), name='checkout'),
    url(r'^checkout/(?P<pk>\d+)/$', views.checkoutimage),
    url(r'^checkout/edit/(?P<pk>\d+)/$', views.editCheckout),
    url(r'^checkout/add/(?P<pk>\d+)/$', views.addCheckout)
    #url(r'^packages/delete/(?P<pk>\d+)/$', views.package_delete, name='package_delete'),
]