from django.urls import path
from django.views.generic.base import TemplateView

app_name = 'pow_gen'

urlpatterns=[
    path('', TemplateView.as_view(template_name='pow_gen/home.html'), name='pow_gen'),

]