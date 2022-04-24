from django.urls import path
from . import views



app_name = 'user'

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('authors/', views.AuthorsView.as_view(), name='authors'),
]