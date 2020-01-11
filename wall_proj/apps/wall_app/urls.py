from django.conf.urls import url
from . import views
                    
urlpatterns = [
    url(r'^wall$', views.wall),
    url(r'^post_message$', views.postMessage),
    url(r'^post_comment$', views.postComment),
    url(r'^delete_message$', views.deleteMessage),
    url(r'^delete_comment$', views.deleteComment),

]