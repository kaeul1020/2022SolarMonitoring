from django.shortcuts import render
from django.views.generic.base import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.conf import settings
from home.models import ModuleData
import json
from decimal import Decimal

status= [
    { "title": "누적 발전량", "value": "3,000", "unit": "MWh", "icon_class": "fas fa-solar-panel fa-fw" },
    { "title": "최대 발전량", "value": "1,234", "unit": "MWh", "icon_class": "fas fa-bolt" },
    { "title": "발전 최적 시간대", "value": "11 ~ 15", "unit": "시", "icon_class": "fas fa-stopwatch" },
    { "title": "누적 수익", "value": "67,200", "unit": "원", "icon_class": "fas fa-hand-holding-usd" },
]

class DecimalEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Decimal):
            return float(obj)
        return json.JSONEncoder.default(self, obj)

class report(LoginRequiredMixin, TemplateView):
    login_url = settings.LOGIN_URL

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        queryset = ModuleData.objects.values('dt', 'dt_hour', 'dc_kw1', 'dc_kw2', 'dc_kw3', 'dc_kw4')
        # queryset_float = float(queryset.values)

        context['datas'] = json.dumps(list(queryset), cls=DecimalEncoder)
        context['status_box'] = status
        return context