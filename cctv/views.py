from django.shortcuts import render
from django.views.generic.base import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

from django.views.decorators import gzip
from django.http import StreamingHttpResponse
import cv2
import threading

from multiprocessing import Process, Queue
from cctv.segmentationCam import Segmentation as Seg
from django.http import HttpResponse,JsonResponse
import json

status= [
    { "title": "오염 유형", "value": "나뭇잎, 흙먼지", "unit": "", "icon_color":"bg-info","icon_class": "fas fa-broom" },
    { "title": "예상 발전 감소량", "value": "35", "unit": "MWh", "icon_color":"bg-info","icon_class": "fas fa-bolt" },
    { "title": "오염된 패널 수", "value": "4", "unit": "/ 4개", "icon_color":"bg-info","icon_class": "fas fa-solar-panel" },
    { "title": "오염 레벨", "value": "경고", "unit": "", "icon_color":"bg-warning","icon_class": "fas fa-sad-tear" },
]



#cam 관련 클래스
class VideoCamera(object):
    def __init__(self):
        print('초기화')
        self.video = cv2.VideoCapture(0)
        (self.grabbed, self.frame) = self.video.read()
        threading.Thread(target=self.update, args=()).start()

    def __del__(self):
        self.video.release()

    def get_image(self, frame):
        image = frame
        _, jpeg = cv2.imencode('.jpeg', image)
        return jpeg.tobytes()

    def get_frame(self):
        return self.frame

    def update(self):
        while True:
            (self.grabbed, self.frame) = self.video.read()

    
# frame단위로 이미지를 계속 반환하게 만드는 클래스. 
class StreamingVideoCamera(object):
    def __init__(self):
        self.camera = VideoCamera()
        self.Seg = Seg()
        self.score =0
    
    def getScore(self):
        return self.score
        
    def gen(self, segmentation=False):
        while True:
            frame = self.camera.get_frame()

            if segmentation ==True : 
                print("segmentation 들어옴")
                fcn = self.Seg.U_Net(frame)
                frame = fcn["frame"]
                print(fcn["score"])
                self.score=(fcn["score"])
            else :
                pass

            frame = self.camera.get_image(frame=frame)
            # frame단위로 이미지를 계속 반환한다. (yield)
            yield(b'--frame\r\n'b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')
        

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

    def Seg(self,request):
        try:
            # frame단위로 이미지를 계속 송출한다
            return StreamingHttpResponse(self.cam.gen(segmentation=True), content_type="multipart/x-mixed-replace;boundary=frame")
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



class cctv(LoginRequiredMixin, TemplateView):

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['status_box'] = status
        return context
