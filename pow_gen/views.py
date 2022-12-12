from django.shortcuts import render
from django.views.generic.base import TemplateView

status= [
    { "title": "현재 날짜","id":"today", "value": "", "unit": "", "icon_class": "fas fa-calendar-alt" },
    { "title": "현재 시간","id":"todayclock", "value": "", "unit": "", "icon_class": "fas fa-clock" },
    { "title": "현재 발전량", "id":"","value": "672", "unit": "kW", "icon_class": "fas fa-bolt" },
    { "title": "발전 시간", "id":"","value": "10", "unit": "시간", "icon_class": "fas fa-clock" },
    { "title": "누적 발전량", "id":"","value": "3,000", "unit": "MWh", "icon_class": "fas fa-solar-panel" },
    { "title": "수익", "id":"","value": "79,000", "unit": "원", "icon_class": "fas fa-money-bill-alt" },
]



class pow_gen(TemplateView):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['status_box'] = status
        return context