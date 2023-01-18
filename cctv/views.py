from django.views.generic.base import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin

from django.http import StreamingHttpResponse
from django.shortcuts import render



from django.http import HttpResponse
from django.http import JsonResponse
import json


from cctv.segmentationCam import StreamingVideoCamera
import numpy as np
from cctv.crop import Crop
import cv2

import os
from django.conf import settings



status= [
    { "title": "오염 유형", "value": "나뭇잎, 흙먼지", "unit": "", "icon_color":"bg-info","icon_class": "fas fa-broom" },
    { "title": "예상 발전 감소량", "value": "35", "unit": "MWh", "icon_color":"bg-info","icon_class": "fas fa-bolt" },
    { "title": "오염된 패널 수", "value": "4", "unit": "/ 4개", "icon_color":"bg-info","icon_class": "fas fa-solar-panel" },
    { "title": "오염 레벨", "value": "경고", "unit": "", "icon_color":"bg-warning","icon_class": "fas fa-sad-tear" },
]

pts= [
    {"name":"1", "loc":"(279,129),(402,130),(441,214),(305,214)"},
    {"name":"2","loc":"(484,130),(607,130),(662,212),(533,212)"},
    {"name":"3","loc":"(127,226),(313,224),(358,355),(154,357)"},
    {"name":"4","loc":"(440,265),(607,230),(680,352),(488,354)"},
]

class Screen(object):
    def __init__(self) -> None:
        self.cam = StreamingVideoCamera() #웹캠 호출
        pass

    def Origin(self,request):
        try:
            # frame단위로 이미지를 계속 송출한다.
            return StreamingHttpResponse(self.cam.gen(), content_type="multipart/x-mixed-replace;boundary=frame")
        except:
            print("에러")
            pass

    def Seg(self,request, pt):
        try:
            # frame단위로 이미지를 계속 송출한다
            print("pt : ", pt)    
            return StreamingHttpResponse(self.cam.gen(segmentation=True, pt=pt), content_type="multipart/x-mixed-replace;boundary=frame")
        except:
            print("에러")
            pass

    def Score(self,request):
        if request.is_ajax(): #ajax 방식일 때 아래 코드 실행
            print("ajax성공")
            context = {'score' : self.cam.getScore()}
            print("context :", context)
            return HttpResponse(json.dumps(context), content_type='application/json')
        else :
            print('ajax 실패')
            pass


class cropper(object):
    def __init__(self) -> None:
        self.Crop = Crop()
        pass
    
    def crop(self,request):
        if request.is_ajax(): #ajax 방식일 때 아래 코드 실행
            print("ajax성공")
            img_src = request.GET.get("img_src")
            print("img_src : ", img_src)

            # image_nparray = np.asarray(bytearray(img_src, dtype=np.uint8))
            img_path = "C:/Users/dalab/Desktop/internet_panel_3.jpg"
            print("img_path:", img_path)
            img = cv2.imread(img_path, cv2.IMREAD_COLOR)
            
            
            np_pt = np.array(eval(pts[0]['loc']), dtype = "float32")
            cv2.imwrite('11result.png', self.Crop.drawROI(img,np_pt))
            context = {'msg' : "성공"}
            return JsonResponse(context)
        else :
            print('ajax 실패')
            pass


class cctv(LoginRequiredMixin, TemplateView):

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['status_box'] = status
        context['pts']=pts
        return context






