from django.shortcuts import render
from django.views.generic.base import TemplateView

status= [
    { "title": "누적 발전량", "value": "3,000", "unit": "MWh", "icon_class": "fas fa-solar-panel fa-fw" },
    { "title": "최대 발전량", "value": "1,234", "unit": "MWh", "icon_class": "fas fa-bolt" },
    { "title": "발전 최적 시간대", "value": "11 ~ 15", "unit": "시", "icon_class": "fas fa-stopwatch" },
    { "title": "누적 수익", "value": "67,200", "unit": "원", "icon_class": "fas fa-hand-holding-usd" },
]



class report(TemplateView):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['status_box'] = status
        return context