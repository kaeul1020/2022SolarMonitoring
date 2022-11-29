from django.urls import path
from django.views.generic.base import TemplateView



app_name = 'cctv'

urlpatterns=[
    path('', TemplateView.as_view(template_name='cctv/cctv.html'), name='cctv'),
    path('setting', TemplateView.as_view(template_name='cctv/cctv_setting.html'), name='cctv_setting'),
]