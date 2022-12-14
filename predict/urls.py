from django.urls import path
from . import views as predict_view


app_name = 'predict'


urlpatterns=[
    path('', predict_view.predict.as_view(template_name='predict/predict.html'), name='predict'),
]