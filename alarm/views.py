from django.shortcuts import render,redirect
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
        timelines = AlarmModel.objects.filter(user_id = user.id).order_by('-time')
        return render(request,'alarm/alarm.html',{'nows':nows,'timelines' : timelines})
    
    def remove_allnow(self,request):
        username = request.user
        user = User.objects.get(username = username)
        nows = AlarmModel.objects.filter(now = 1,user_id = user.id).order_by('-time')
        
        for now in nows:
            now.now = False
            now.save()
        
        return redirect('alarm:alarm')
    
    def remove_onenow(self,request,id):
        del_now = AlarmModel.objects.get(id=id)
        del_now.now = False
        del_now.save()
        
        return redirect('alarm:alarm')