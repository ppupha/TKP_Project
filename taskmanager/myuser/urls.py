from django.urls import path
from . import views

app_name = 'myuser'

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('signup/', views.SignupView.as_view(), name='signup'),
    path('login/', views.LoginClass.as_view(), name='login'),

]