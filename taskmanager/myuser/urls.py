from django.urls import path
from . import views

app_name = 'myuser'

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('signup/', views.SignupView.as_view(), name='signup'),
    path('login/', views.LoginClass.as_view(), name='login'),
    path('activate/<uidb64>/<token>/', views.ActivateView.as_view(), name='activate'),
    path('accounts/password_reset/', views.PasswordResetView_.as_view(), name='password_reset'),
    path('accounts/reset/<uidb64>/<token>/', views.PasswordResetConfirmView_.as_view(), name='password_reset_confirm'),
    path('accounts/password_reset/done/', views.PasswordResetDoneView_.as_view(), name='password_reset_done'),
    path('accounts/reset/done/', views.PasswordResetCompleteView_.as_view(), name='password_reset_complete'),
    path('accounts/password_change/', views.PasswordChangeView_.as_view(), name='password_change'),
    path('accounts/password_change/done/', views.PasswordChageDoneView_.as_view(), name='password_change_done'),

]