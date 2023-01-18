from django.urls import path
from django.views.generic.base import TemplateView
from . import views as cctv_view
from requests import request
import numpy as np



app_name = 'cctv'


Screen=cctv_view.Screen()
Cropper = cctv_view.cropper()

urlpatterns=[
    path('', cctv_view.cctv.as_view(template_name='cctv/cctv.html'), name='cctv'),
    path('setting/', TemplateView.as_view(template_name='cctv/cctv_setting.html'), name='cctv_setting'),
    path('crop/', TemplateView.as_view(template_name='cctv/cctv_cropper.html'), name='cctv_cropper'),
    path('screen/', Screen.Origin, name="cctv_screen"),
    path('screen_score/', Screen.Score, name="cctv_screen_score"),
    path('seg_screen/<pt>/', Screen.Seg),
    path('testcrop/',Cropper.crop, name="testcropper"),
]

print("!! urlpatterns : ", urlpatterns)