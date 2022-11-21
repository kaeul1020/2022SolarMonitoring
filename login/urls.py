from django.contrib import admin
from django.urls import path, reverse_lazy
from django.conf.urls import url, include
from django.contrib.auth import views as auth_views
from django.views.generic.base import TemplateView
from . import views as login_views


app_name = 'login'

password_reset_patterns=[
    path('', login_views.UserPasswordResetView.as_view(),name='password_reset'),
    path('done/', 
        auth_views.PasswordResetDoneView.as_view(template_name='login/password_reset_done.html'),name="password_reset_done"),
    path('confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(success_url=reverse_lazy('login:password_reset_complete')), name='password_reset_confirm'),
    path('complete/', auth_views.PasswordResetCompleteView.as_view(template_name='login/password_reset_complete.html'), name='password_reset_complete')
]

register_patterns=[
    path('', login_views.register, name='register'),
    path('done/', TemplateView.as_view(template_name='login/register_done.html'), name='register_done'),
]

urlpatterns=[
    path('',auth_views.LoginView.as_view(template_name='login/login.html'), name='login'),
    path('password_reset/', include(password_reset_patterns)),
    path('register/',  include(register_patterns)),
]



