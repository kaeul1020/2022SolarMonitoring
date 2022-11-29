from django.urls import path
from django.views.generic.base import TemplateView


app_name = 'predict'


urlpatterns=[
    path('', TemplateView.as_view(template_name='predict/predict.html'), name='predict'),
]