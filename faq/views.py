from django.shortcuts import render
from .models import FaqModel
from django.http import HttpResponse
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.conf import settings

from django.contrib.auth.models import User

class Faq(LoginRequiredMixin, TemplateView):
    login_url = settings.LOGIN_URL

    def faq_list(self,request):
        faqs = FaqModel.objects.all() 
        return render(request,'faq/faq.html',{'FAQs' : faqs})


