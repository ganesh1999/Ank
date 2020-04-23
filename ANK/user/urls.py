from django.contrib import admin
from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [


    path('', views.home, name="home"),
    path('login/', views.loginpage, name='login'),
    path('logout', views.logoutpage, name='logout'),
    path('register/', views.registerpage, name='register'),
    path('profile/', views.profilepage, name='profile'),
    path('results/', views.results, name='results'),
    path('demo/', views.demo, name='demo'),
    path('downloadpdf/', views.Downloadpdf, name='downloadpdf'),


    path('reset_password/', auth_views.PasswordResetView.as_view(template_name='reset_password.html'),
         name='reset_password'),
    path('reset_password_sent/', auth_views.PasswordResetDoneView.as_view(template_name='reset_password_sent.html'),
         name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='reset_password_confirm.html'),
         name='password_reset_confirm'),
    path('reset_password_complete/', auth_views.PasswordResetCompleteView.as_view(template_name='reset_password_complete.html'),
         name='password_reset_complete'),


]
