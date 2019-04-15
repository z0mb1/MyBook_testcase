from django.conf.urls import url
from django.urls import path, include
from book_list import views

app_name = 'book_list'
urlpatterns = [
    url(r'^$', views.book_list, name='book_list'),
    url(r'^clear_session/$', views.clear_session, name='clear_session'),
]
