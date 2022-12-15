from django.urls import path
from django.views.generic.base import TemplateView
from . import views as cctv_view



app_name = 'cctv'

urlpatterns=[
    path('', cctv_view.cctv.as_view(template_name='cctv/cctv.html'), name='cctv'),
    path('setting/', TemplateView.as_view(template_name='cctv/cctv_setting.html'), name='cctv_setting'),
    path('crop/', TemplateView.as_view(template_name='cctv/cctv_cropper.html'), name='cctv_cropper'),
]