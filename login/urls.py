from django.contrib import admin
from django.urls import path
from django.conf.urls import url, include
from django.contrib.auth import views as auth_views
from django.views.generic.base import TemplateView

 
password_reset_patterns=[
    path('', auth_views.PasswordResetView.as_view(template_name='login/forgot-password.html')),
    path('done/', auth_views.PasswordResetDoneView.as_view()),
    path('confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view()),
    path('complete/', auth_views.PasswordResetCompleteView.as_view(template_name='login/forgot-password-success.html'))
]

urlpatterns=[
    path('',auth_views.LoginView.as_view(template_name='login/login.html')),
    path('password_reset/', include(password_reset_patterns)),
    path('register/', TemplateView.as_view(template_name='login/register.html')),
    path('register-success/', TemplateView.as_view(template_name='login/register-success.html')),
]



