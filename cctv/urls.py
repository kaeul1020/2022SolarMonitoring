from django.urls import path
from django.views.generic.base import TemplateView
from . import views as cctv_view
from requests import request
import numpy as np



app_name = 'cctv'


Screen=cctv_view.Screen()
Cropper = cctv_view.Cropper()

urlpatterns=[
    path('', cctv_view.cctv.as_view(template_name='cctv/cctv.html'), name='cctv'),
    path('setting/', TemplateView.as_view(template_name='cctv/cctv_setting.html'), name='cctv_setting'),
    path('crop/<num>/', Cropper.cropper),
    # 실시간 연결
    # path('screen/', Screen.Origin, name="cctv_screen"),
    # path('screen_score/', Screen.Score, name="cctv_screen_score"),
    # path('seg_screen_frame/<pt>/', Screen.SegFrame),
    path('seg_screen_image/<num>/', Screen.setSegImage),
    path('crop_preview/',Cropper.CropPreView, name="cropper_preview"),
    path('cropLocSave/',Cropper.CropLocSave, name="cropper_save"),
] 