from django.contrib import admin
from django.urls import path
from django.conf.urls import url, include
from django.contrib.auth import views as auth_views
from django.views.generic.base import TemplateView


urlpatterns=[
    path('',auth_views.LoginView.as_view(template_name='login/login.html')),
    path('forgot-password/', TemplateView.as_view(template_name='login/forgot-password.html')),
    path('forgot-password-success/', TemplateView.as_view(template_name='login/forgot-password-success.html')),
    path('register/', TemplateView.as_view(template_name='login/register.html')),
    path('register-success/', TemplateView.as_view(template_name='login/register-success.html')),
]