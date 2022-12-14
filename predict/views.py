from django.shortcuts import render
from django.views.generic.base import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.conf import settings


# Create your views here.
class predict(LoginRequiredMixin, TemplateView):
    login_url = settings.LOGIN_URL

