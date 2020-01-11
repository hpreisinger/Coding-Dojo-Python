from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^books/$', views.books),
    url(r'^authors/$', views.authors),
    url(r'^books/(?P<book_id>\d+)$', views.book_profile),
    url(r'^authors/(?P<author_id>\d+)$', views.author_profile),
    url(r'^book_form/$', views.book_form),
    url(r'^author_form/$', views.author_form),
    url(r'^book_dropdown/$', views.book_dropdown),
    url(r'^author_dropdown/$', views.author_dropdown),
]