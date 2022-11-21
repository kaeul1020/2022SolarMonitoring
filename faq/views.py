from django.shortcuts import render
from .models import FaqModel
from django.http import HttpResponse
from django.views.generic import TemplateView

class FaqView(TemplateView):
    queryset = FaqModel.objects.all()  

    def get(self, request, *args, **kwargs):
        ctx = {
            'FAQs': self.queryset 
        }
        return self.render_to_response(ctx)


