from django.shortcuts import render

from django.contrib.auth import authenticate
from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import logout
from django.shortcuts import redirect
from django.contrib.auth.models import User
from django.contrib.auth import login

from django.contrib.auth.decorators import login_required
from django.views.generic.base import TemplateView
from django.contrib.auth import views as auth_views
from django.contrib.auth.mixins import LoginRequiredMixin
from django.conf import settings


class login(LoginRequiredMixin, TemplateView):
    login_url = settings.LOGIN_URL

