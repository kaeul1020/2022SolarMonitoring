from django.urls import path
from django.views.generic.base import TemplateView
from . import views as report_view


app_name = 'report'

urlpatterns=[
    path('', report_view.report.as_view(template_name='report/report.html'), name='report'),
]
