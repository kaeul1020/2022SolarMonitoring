from django.urls import path
from . import views as index_view


app_name = 'home'


urlpatterns=[
    path('', index_view.login.as_view(template_name='home/index.html'), name='home'),
]



