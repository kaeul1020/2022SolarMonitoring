from django.contrib.auth import authenticate
from django.views.generic.base import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.conf import settings
from alarm.models import AlarmModel
from pow_gen.models import MonitoringDataset as predict
from .models import ModuleData as gen
from django.contrib.auth.models import User
from django.db.models import Sum,Q
from datetime import date,timedelta,datetime


status_value= [
    { "title": "현재 발전량", "value": "", "unit": "W", "icon_class": "fas fa-bolt" },
    { "title": "금일 예측 발전량", "value": "", "unit": "W", "icon_class": "fas fa-battery-full" },
    { "title": "누적 발전량", "value": "", "unit": "Wh", "icon_class": "fas fa-clock" },
    { "title": "발전시간", "value": "", "unit": "시간", "icon_class": "fas fa-stopwatch" },
    { "title": "전일 대비 발전량", "value": "", "unit": "W", "icon_class": "fas fa-coins" },
    { "title": "발전 효율", "value": "", "unit": "%", "icon_class": "fas fa-hand-holding-usd" },
]

cctv_value = [
    { "cctv_num" : 0, "im_src" : "/static/cctv_images/PanelImageSample.jpg","soiling_type" : "모래", "soiling_area" : "25%" , "active" : "active"},
    { "cctv_num" : 1, "im_src" : "/static/cctv_images/PanelImageSample_1.jpg","soiling_type" : "새똥", "soiling_area" : "17%", "active" : ""},
    { "cctv_num" : 2, "im_src" : "/static/cctv_images/PanelImageSample_2.jpg","soiling_type" : "꽃가루", "soiling_area" : "75%", "active" : ""},
    { "cctv_num" : 3, "im_src" : "/static/cctv_images/PanelImageSample_3.jpg","soiling_type" : "꽃가루", "soiling_area" : "5%", "active" : ""}
]

class home(LoginRequiredMixin, TemplateView):
    login_url = settings.LOGIN_URL

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        timelines = self.alarm_data()
        status_value = self.get_status()
        pred_data = self.graph_status()

        context['timelines'] = timelines
        context['status_box'] = status_value
        context['pred_data'] = pred_data
        context['cctv'] = cctv_value

        return context

    def alarm_data(self):
        username = self.request.user
        user = User.objects.get(username = username)
        timelines = AlarmModel.objects.filter(user_id = user.id).order_by('-time')
        return timelines
    
    def get_status(self):

        nowgen = gen.objects.order_by('-dt','-dt_hour').first()
        status_value[0]['title'] = '현재 발전량 \t ('+str(nowgen.dt_hour) + '시)'
        status_value[0]['value'] = round(nowgen.dc_kw4)

        cumulative_powgen = gen.objects.filter(dt=date.today()).aggregate(Sum('dc_kw4'))
        status_value[2]['value'] = round(sum(cumulative_powgen.values()))

        gen_time = gen.objects.filter(Q(dt=date.today()) & (~Q(dc_kw4__lt=0.1))).count()
        status_value[3]['value'] = gen_time

        yesterday = date.today() - timedelta(1)
        yesterday_powgen = gen.objects.filter(dt=yesterday, dt_hour__range = [0,datetime.now().hour]).aggregate(Sum('dc_kw4'))
        diff = round(sum(cumulative_powgen.values()) - sum(yesterday_powgen.values()))
        status_value[4]['value'] = diff

        return status_value
    
    def graph_status(self):

        pred_data = []
        pred = predict.objects.filter(year = 2022 , month = 6, day = 7)
        
        for p in pred:
            if p.hour >= 6 and p.hour <= 21:
                pred_data.append({"time" : str(p.hour)+'시', "pred" : float(p.pred_y), "actual" : float(p.y)})
        
        return pred_data
    




