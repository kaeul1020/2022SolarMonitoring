from django.urls import path
from django.views.generic.base import TemplateView
from . import views as FaqView


app_name = 'faq'

urlpatterns=[
    path('', FaqView.FaqView.as_view(template_name='faq/faq.html'), name='faq'),
]

