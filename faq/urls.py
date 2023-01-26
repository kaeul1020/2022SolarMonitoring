from django.urls import path
from django.views.generic.base import TemplateView
from . import views as faq_view


app_name = 'faq'
Faq = faq_view.Faq()

urlpatterns=[
    path('', Faq.faq_list, name='faq'),
]

