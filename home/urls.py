from django.urls import path
from . import views as home_view


app_name = 'home'
home_data = home_view.home()

urlpatterns=[
    path('', home_data.datas, name='home'),
]



