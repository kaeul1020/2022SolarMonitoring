from django.urls import path
from . import views as pow_gen_view

app_name = 'pow_gen'

urlpatterns=[
    path('', pow_gen_view.pow_gen.as_view(template_name='pow_gen/pow_gen.html'), name='pow_gen'),
]