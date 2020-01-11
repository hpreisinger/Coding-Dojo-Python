from django.conf.urls import url
from . import views
                    
urlpatterns = [
    url(r'^$', views.redirectToShows),
    url(r'^shows$', views.index),
    url(r'^shows/new$', views.new),
    url(r'^shows/create$', views.create),
    url(r'^shows/(?P<show_id>\d+)$', views.profile),
    url(r'^shows/(?P<show_id>\d+)/edit$', views.edit),
    url(r'^shows/(?P<show_id>\d+)/update$', views.update),
    url(r'^shows/(?P<show_id>\d+)/destroy$', views.destroy),
]