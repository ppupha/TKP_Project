from django.urls import path
from . import views



app_name = 'user'

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    #path('login/', views.LoginClass.as_view(), name='login'),
    #path('signup/', views.SignupView.as_view(), name='signup'),
    path("", views.IndexView.as_view(), name='user_profile'),
]