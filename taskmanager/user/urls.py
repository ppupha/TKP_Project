from django.urls import path
from . import views



app_name = 'user'

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('authors/', views.AuthorsView.as_view(), name='authors'),
    path('help/', views.HelpView.as_view(), name='help'),
    # path('login/', views.LoginClass.as_view(), name='login'),
    #path('signup/', views.SignupView.as_view(), name='signup'),
    path('profile/', views.user_profile, name='user_profile'),
    # path("user_profile", views.IndexView.as_view(), name='user_profile'),
]