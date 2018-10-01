from django.conf.urls import url, include
from django.contrib.auth import views as auth_views
from website.views import register, account_activation_sent, activate
from website.forms import UserForm
from website.views import *
from . import views
urlpatterns = [
    
    url(r'^$', views.welcome, name='welcome'),
    url(r'^user/$',views.welcome2,name='welcome2'),
    url(r'^create_design/$',views.create_design,name='create_design'),   
    url(r'^details/(?P<pc_name_id>[0-9]+)/$',views.details,name='details'),
    url(r'^accounts/register/$',views.register, name='register'),
    url(r'^user_selected_product/(?P<u_pk>[0-9]+)/(?P<c_pk>[0-9]+)/(?P<p_pk>[0-9]+)/$',views.selected_products),
    url(r'^get_cart/(?P<u_pk>[0-9]+)$',views.get_cart,name='get_cart'),
    url(r'^remove_from_cart/(?P<u_pk>[0-9]+)/(?P<p_pk>[0-9]+)/$',views.remove_from_cart),
    url(r'^accounts/', include('registration.backends.default.urls')),
    url(r'^registration/', include('registration.auth_urls')),
    url(r'^login/', auth_views.login, name='login'),
    url(r'^logout/', auth_views.logout, name='logout'),
    url(r'^payment/$', views.payment, name="payment"),
    url(r'^payment/success$', views.payment_success, name="payment_success"),
    url(r'^payment/failure$', views.payment_failure, name="payment_failure"),
    url(r'^user_id$',views.display_uid),
    
    url(r'^account_activation_sent/$', views.account_activation_sent, name='account_activation_sent'),
    url(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        views.activate, name='activate'),
    url(r'^activation_complete/$', views.activation_complete, name='activation_complete')
]
