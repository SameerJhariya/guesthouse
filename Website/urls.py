from django.conf.urls import url,include
from django.conf.urls import url
from django.contrib import admin
from django.contrib.auth import views as auth_views
from . import views


urlpatterns = [
	url(r'^$',views.index),
	url(r'^login/$', auth_views.login, name='login'),
	url(r'^signup/$', views.register, name='signup'),
    url(r'^logout/$', auth_views.logout, name='logout'),
    url(r'^book/$', views.book, name='book'),
    url(r'^block/$', views.block, name='block'),
    url(r'^room/$', views.room, name='room'),
    url(r'^payment/$', views.payment, name='payment'),
    url(r'^changecap/$', views.changecap, name='changecap'),
    url(r'^request/$', views.request_room, name='request_room'),  
    url(r'^check/$', views.check_request, name='check_request'),  
    url(r'^occupied/$', views.occupied, name='occupied'),   
]