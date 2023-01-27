from django.views.generic.base import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin

from django.http import StreamingHttpResponse
from django.shortcuts import render



from django.http import HttpResponse
from django.http import JsonResponse
import json

# 실시간 연결
from cctv.segmentationCam import StreamingVideoCamera
from cctv.segmentationCam import StaticSegImage
import numpy as np
from cctv.crop import Crop
import cv2
from datetime import datetime

import os
from django.conf import settings

#알람
from alarm.models import AlarmModel



status= [
    { "title": "오염 유형", "value": "나뭇잎, 흙먼지", "unit": "", "icon_color":"bg-info","icon_class": "fas fa-broom" },
    { "title": "예상 발전 감소량", "value": "35", "unit": "MWh", "icon_color":"bg-info","icon_class": "fas fa-bolt" },
    { "title": "오염된 패널 수", "value": "4", "unit": "/ 4개", "icon_color":"bg-info","icon_class": "fas fa-solar-panel" },
    { "title": "오염 레벨", "value": "경고", "unit": "", "icon_color":"bg-warning","icon_class": "fas fa-sad-tear" },
]

db_dics= [
    {"num":1, "loc":"(279,129),(402,130),(441,214),(305,214)", "score" : -1, "src" : ""},
    {"num":2,"loc":"(484,130),(607,130),(662,212),(533,212)", "score" : -1, "src" : ""},
    {"num":3,"loc":"(127,226),(313,224),(358,355),(154,357)", "score" : -1, "src" : ""},
    {"num":4,"loc":"(440,265),(607,230),(680,352),(488,354)", "score" : -1, "src" : ""},
]

class Dics(object):
    def __init__(self) -> None:
        global db_dics
        pass

    def getLoc(self, num):
        loc = -1

        for db_dic in db_dics:
            if int(num) == db_dic["num"]:
                loc = db_dic["loc"] 
                break

        return loc

    def setLoc(self, num, loc):
        for db_dic in db_dics:
            if int(num) == db_dic["num"]:
                db_dic["loc"] =loc

    def getScore(self, num):
        score = -1

        for db_dic in db_dics:
            if int(num) == db_dic["num"]:
                score = db_dic["score"] 
                break

        return score

    def setScore(self, num, score):
        for db_dic in db_dics:
            if int(num) == db_dic["num"]:
                db_dic["score"] =score

    def getSrc(self, num):
        src = ""

        for db_dic in db_dics:
            if int(num) == db_dic["num"]:
                src = db_dic["src"] 
                break

        return src

    def setSrc(self, num, src):
        for db_dic in db_dics:
            if int(num) == db_dic["num"]:
                db_dic["src"] =src

class Screen(object):
    def __init__(self) -> None:
        self.dics = Dics()
        # self.cam = StreamingVideoCamera() #웹캠 호출
        self.segImage = StaticSegImage()
        self.Crop = Crop()
        pass

    # 실시간연결
    """
    def Origin(self,request):
        try:
            # frame단위로 이미지를 계속 송출한다.
            return StreamingHttpResponse(self.cam.gen(), content_type="multipart/x-mixed-replace;boundary=frame")
        except:
            print("에러")
            pass

    def SegFrame(self,request, pt):
        try:
            # frame단위로 이미지를 계속 송출한다
            print("pt : ", pt)    
            return StreamingHttpResponse(self.cam.gen(segmentation=True, pt=pt), content_type="multipart/x-mixed-replace;boundary=frame")
        except:
            print("에러")
            pass

    def Score(self,request):
        if request.is_ajax(): #ajax 방식일 때 아래 코드 실행
            print("score ajax성공")
            context = {'score' : self.cam.getScore()}
            print("context :", context)
            return HttpResponse(json.dumps(context), content_type='application/json')
        else :
            print('ajax 실패')
            pass
    """

    def setSegImage(self, request, num):
        pt = self.dics.getLoc(num)

        #cctv 이미지 읽어오기
        img_src ="cctv_images\PanelImageSample.jpg"
        basic_img_path = settings.BASE_DIR+ settings.STATIC_URL
        img_path = (basic_img_path+img_src).replace('\\','/')
        img = cv2.imread(img_path, cv2.IMREAD_COLOR)

        #crop + seg 이미지 저장
        seg = self.segImage.getSeg(img=img, pt=pt)
        img_path = (basic_img_path+'cctv_images/11result_seg_'+str(num)+'.png').replace('\\','/')
        cv2.imwrite(img_path, seg["frame"])
        self.dics.setSrc(num, "/static/"+img_path)

        #원본이미지 위에 crop된 위치 표시해주는 이미지 저장
        np_pt = np.array(eval(pt), dtype = "float32")
        cv2.imwrite(basic_img_path +'cctv_images/11result_'+str(num)+'.png', self.Crop.drawROI(img,np_pt))

        #각 패널의 오염면적 저장
        self.dics.setScore(num, seg["score"])
        
        #알림 파트 : 임의로 여기에다가 씀
        if seg["score"] >=50 :
            self.alram = AlarmModel()
            print("request.user.username, 1, num, seg['score'] : ", request.user.username, 1, num, seg['score'])
            self.alram.panel_soiling_alarm(request.user.username, 1, num, seg['score'])


class Cropper(object):

    def __init__(self) -> None:
        self.Crop = Crop()
        self.dics = Dics()
        pass

    def cropper(self, request, num):
        context = {
            'num': num,
            'loc' : self.dics.getLoc(num)
        }
        return render(request, 'cctv/cctv_cropper.html', context)

    def CropPreView(self,request):
        if request.is_ajax(): #ajax 방식일 때 아래 코드 실행
            img_src ="cctv_images\PanelImageSample.jpg"
            pt = request.GET.get("pt")

            basic_img_path = settings.BASE_DIR+ settings.STATIC_URL
            img_path = (basic_img_path+img_src).replace('\\','/')
            
            img = cv2.imread(img_path, cv2.IMREAD_COLOR)

            np_pt = np.array(eval(pt), dtype = "float32")

            new_src = 'cctv_images/11result.png'
            new_crop_src = 'cctv_images/11result_crop.png'
            cv2.imwrite(basic_img_path +new_src, self.Crop.drawROI(img,np_pt))
            cv2.imwrite(basic_img_path +new_crop_src, self.Crop.getFrame(img,np_pt))
            
            context = {'img_src' : new_src, 'crop_img_src' : new_crop_src}
            return JsonResponse(context)
        else :
            print('ajax 실패')
            pass
    
    def CropLocSave(self,request):
        if request.is_ajax(): #ajax 방식일 때 아래 코드 실행
            print("crop ajax성공")
            print(request.GET.get("num"))
            num = int(request.GET.get("num"))
            pt = request.GET.get("pt")
            self.dics.setLoc(num, pt)
            print("db_dics[",str(num),"] 변경 : ", db_dics[num-1])
            return JsonResponse({})
        else :
            print('ajax 실패')
            pass

class cctv(LoginRequiredMixin, TemplateView):

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        screen = Screen()
        global db_dics

        for db_dic in db_dics:
            screen.setSegImage(self.request, num=db_dic["num"])

        context['status_box'] = status
        context['db_dics']=db_dics
        return context







