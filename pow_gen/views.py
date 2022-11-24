from django.shortcuts import render
from django.http import HttpResponse
import datetime
import re

# def home(request):
#     return HttpResponse("Hello, Django!!!!!!!")
#     #return render(request, 'home.html')

def home(request):
    return render(request, 'pow_gen/home.html')

# Create your views here.
