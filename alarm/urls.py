from django.urls import path
from django.views.generic.base import TemplateView
from . import views as alarm_view


app_name = 'alarm'

urlpatterns=[
    path('', alarm_view.alarm.as_view(template_name='alarm/alarm.html'), name='alarm'),
]
