from django.urls import path
from . import views as alarm_view

app_name = 'alarm'
Alarm = alarm_view.alarm()

urlpatterns=[
    path('', alarm_view.alarm.as_view(template_name = 'alarm/alarm.html'), name='alarm'),
    path('delallnow/',Alarm.remove_allnow, name='delallnow'),
    path('delalram/<int:id>',Alarm.remove_onenow, name='delallnow'),
]
