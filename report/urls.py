from django.urls import path
from django.views.generic.base import TemplateView
from . import views as FaqView


app_name = 'report'

urlpatterns=[
    path('', TemplateView.as_view(template_name='report/report.html'), name='report'),
]
