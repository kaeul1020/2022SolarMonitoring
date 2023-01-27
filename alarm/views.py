from django.shortcuts import render
from django.views.generic.base import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.conf import settings
from .models import AlarmModel
from django.contrib.auth.models import User

class alarm(LoginRequiredMixin,TemplateView):
    login_url = settings.LOGIN_URL
    
    def alarms(self,request):
        username = request.user
        user = User.objects.get(username = username)
        nows = AlarmModel.objects.filter(now = 1,user_id = user.id).order_by('-time')
        '''
        for now in nows:
            now.now = False
            now.save()
        '''
        timelines = AlarmModel.objects.filter(user_id = user.id).order_by('-time')
        return render(request,'alarm/alarm.html',{'nows':nows ,'timelines' : timelines})