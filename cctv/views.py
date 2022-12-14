from django.shortcuts import render
from django.views.generic.base import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.conf import settings

status= [
    { "title": "오염 유형", "value": "나뭇잎, 흙먼지", "unit": "", "icon_color":"bg-info","icon_class": "fas fa-broom" },
    { "title": "예상 발전 감소량", "value": "35", "unit": "MWh", "icon_color":"bg-info","icon_class": "fas fa-bolt" },
    { "title": "오염된 패널 수", "value": "4", "unit": "/ 4개", "icon_color":"bg-info","icon_class": "fas fa-solar-panel" },
    { "title": "오염 레벨", "value": "경고", "unit": "", "icon_color":"bg-warning","icon_class": "fas fa-sad-tear" },
]



class cctv(LoginRequiredMixin, TemplateView):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['status_box'] = status
        return context
