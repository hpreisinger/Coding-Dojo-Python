from django.conf.urls import url
from . import views
                    
urlpatterns = [
    url(r'^$', views.index),
    url(r'^dashboard$', views.dashboard),
    url(r'^results$', views.results),
    url(r'^location/(?P<location_id>\d+)$', views.profile),
    url(r'^favorites$', views.favorites),
    url(r'^process$', views.process),
    url(r'^login$', views.login),
    url(r'^register$', views.register),
    url(r'^logout$', views.logout),
    url(r'^location/(?P<location_id>\d+)/add_fav$', views.add_fav),
    url(r'^location/(?P<location_id>\d+)/remove_fav$', views.remove_fav),
    url(r'^reset$', views.clear_search),
    url(r'^test$', views.test),
]