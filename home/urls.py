from django.urls import path
from . import views as home_view


app_name = 'home'

urlpatterns=[
    path('', home_view.home.as_view(template_name='home/index.html'), name='home'),
]



