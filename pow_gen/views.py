from django.shortcuts import render
from django.views.generic.base import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.conf import settings
from home.models import ModuleData
import json
from decimal import Decimal

status= [
    { "title": "현재 발전량","id":"power", "value": "", "unit": "", "icon_class": "fas fa-calendar-alt" },
    { "title": "금일 누적 발전량","id":"happower", "value": "", "unit": "", "icon_class": "fas fa-clock" },
    { "title": "금일 예측 발전량", "id":"","value": "9915 kw", "unit": "", "icon_class": "fas fa-bolt" },
    { "title": "발전 시간", "id":"time","value": "", "unit": "", "icon_class": "fas fa-clock" },
    { "title": "발전 효율", "id":"","value": "80", "unit": "%", "icon_class": "fas fa-solar-panel" },
    { "title": "예측 정확도", "id":"","value": "95", "unit": "%", "icon_class": "fas fa-money-bill-alt" },
]

class DecimalEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Decimal):
            return float(obj)
        return json.JSONEncoder.default(self, obj)

class pow_gen(LoginRequiredMixin, TemplateView):
    login_url = settings.LOGIN_URL

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        queryset = ModuleData.objects.values('dt', 'dt_hour', 'dc_kw1', 'dc_kw2', 'dc_kw3', 'dc_kw4')
        # queryset_float = float(queryset.values)

        context['datas'] = json.dumps(list(queryset), cls=DecimalEncoder)
        context['status_box'] = status
        return context