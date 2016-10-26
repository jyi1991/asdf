from django.conf.urls import url
from . import views

urlpatterns = [
	url(r'^$', views.reroute, name='login_init'),
    url(r'^main$', views.index, name='login_index'),
    url(r'^register$', views.register, name='login_register'),
    url(r'^login$', views.login, name='login_login'),
    url(r'^logout$', views.logout, name='login_logout')
]
