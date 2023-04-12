from django.apps import AppConfig
from LSTM_Modelling import my_model

class PowGenConfig(AppConfig):
    name = 'pow_gen'
    model = my_model()