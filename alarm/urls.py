from django.urls import path
from django.views.generic.base import TemplateView
from . import views as alarm_view


app_name = 'alarm'
Alarm = alarm_view.alarm()

urlpatterns=[
    path('', Alarm.alarms, name='alarm'),
]
