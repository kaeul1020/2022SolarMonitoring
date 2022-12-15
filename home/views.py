from django.shortcuts import render

from django.contrib.auth import authenticate
from django.shortcuts import render
from django.views.generic.base import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.conf import settings

status= [
    { "title": "현재 발전량", "value": "672", "unit": "kW", "icon_class": "fas fa-bolt" },
    { "title": "누적 발전량", "value": "3,000", "unit": "MWh", "icon_class": "fas fa-battery-full" },
    { "title": "발전 시간", "value": "10", "unit": "시간", "icon_class": "fas fa-clock" },
    { "title": "발전 최적 시간대", "value": "11 ~ 15", "unit": "시", "icon_class": "fas fa-stopwatch" },
    { "title": "수익", "value": "1,000", "unit": "원", "icon_class": "fas fa-coins" },
    { "title": "누적 수익", "value": "67,200", "unit": "원", "icon_class": "fas fa-hand-holding-usd" },
]



class home(LoginRequiredMixin, TemplateView):
    login_url = settings.LOGIN_URL

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['status_box'] = status
        return context





