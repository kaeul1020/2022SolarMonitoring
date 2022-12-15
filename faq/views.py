from django.shortcuts import render
from .models import FaqModel
from django.http import HttpResponse
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.conf import settings

class Faq(LoginRequiredMixin, TemplateView):
    queryset = FaqModel.objects.all()  
    login_url = settings.LOGIN_URL

    def get(self, request, *args, **kwargs):
        ctx = {
            'FAQs': self.queryset 
        }
        return self.render_to_response(ctx)


