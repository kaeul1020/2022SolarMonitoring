from django.contrib import admin
from django.urls import path
from django.conf.urls import url, include
from django.contrib.auth import views as auth_views
from django.views.generic.base import TemplateView


password_reset_patterns=[
    path('', auth_views.PasswordResetView.as_view(template_name='login/password_reset.html'), name='password_reset'),
    path('done/', auth_views.PasswordResetDoneView.as_view(), name="password_reset_done"),
    path('confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('complete/', auth_views.PasswordResetCompleteView.as_view(template_name='login/password_reset_complete.html'))
]

register_patterns=[
    path('', TemplateView.as_view(template_name='login/register.html')),
    path('done/', TemplateView.as_view(template_name='login/register_done.html')),
]

urlpatterns=[
    path('',auth_views.LoginView.as_view(template_name='login/login.html'), name='login'),
    path('password_reset/', include(password_reset_patterns)),
    path('register/',  include(register_patterns)),
]



