from django.shortcuts import render
from django.views.generic.base import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.conf import settings

data= [
    { 
        "title": "에너지 부족", 
        "content": "저장된 에너지가 10% 이하입니다. 정전에 대비하기 위해 다른 전력공급장치를 가동하십시오.", 
        "time":"2022/11/28 19:35",
        "color":"bg-danger",
        "icon_class": "fas fa-battery-quarter", 
        "more_info": True,
        "href":"",
        "now":True,
    },
    { 
        "title": "패널 온도 상승", 
        "content": "현재 태양광 패널의 온도가 높습니다. 패널의 온도가 높을 경우 발전 효율이 떨어질 수 있습니다.", 
        "time":"2022/11/28 17:28",
        "color":"bg-orange",
        "icon_class": "fas fa-solar-panel", 
        "more_info": False,
        "href":"",
        "now":False,
    },
        { 
        "title": "태양광 패널 오염 감지", 
        "content": "현재 1번 CCTV에 흙먼지가 감지되었습니다. 더보기를 누르시면 구체적인 정보를 확인 할 수 있습니다.", 
        "time":"2022/11/20 16:49",
        "color":"bg-orange",
        "icon_class": "fas fa-solar-panel", 
        "more_info": True,
        "href":"",
        "now":False,
    },
    { 
        "title": "에너지 과잉", 
        "content": "현재 저장된 에너지가 95% 이상입니다. 100%가 되면 더이상 에너지를 저장할 수 없습니다. 남는 에너지를 판매함으로써 수익을 낼 수 있습니다.", 
        "time":"2022/11/20 15:01",
        "color":"bg-green",
        "icon_class": "fas fa-battery-full", 
        "more_info": False,
        "href":"",
        "now":False,
    },
    { 
        "title": "좋음", 
        "content": "현재 발전이 최고효율로 이루어지고 있습니다.", 
        "time":"2022/11/20 11:00",
        "color":"bg-green",
        "icon_class": "fas fa-check-circle", 
        "more_info": False,
        "href":"",
        "now":False,
    },
    ]

now_data = [{
    "title": "에너지 부족", 
    "content": "저장된 에너지가 10% 이하입니다. 정전에 대비하기 위해 다른 전력공급장치를 가동하십시오.", 
    "time":"2022/11/28 19:35",
    "color":"bg-danger",
    "icon_class": "fas fa-battery-quarter", 
    "more_info": True,
    "href":"",
    "now":True,
}]



class alarm(LoginRequiredMixin,TemplateView):
    login_url = settings.LOGIN_URL
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['timelines'] = data
        context['nows'] = now_data
        return context

