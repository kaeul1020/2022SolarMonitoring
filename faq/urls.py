from django.urls import path
from django.views.generic.base import TemplateView
from . import views as faq_view


app_name = 'faq'

urlpatterns=[
    path('', faq_view.Faq.as_view(template_name='faq/faq.html'), name='faq'),
]

