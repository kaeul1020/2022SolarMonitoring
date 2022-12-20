from django.shortcuts import render
from django.views.generic.base import TemplateView
from django.views.generic import CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

from django.views.decorators import gzip
from django.http import StreamingHttpResponse
import cv2
import threading

status= [
    { "title": "오염 유형", "value": "나뭇잎, 흙먼지", "unit": "", "icon_color":"bg-info","icon_class": "fas fa-broom" },
    { "title": "예상 발전 감소량", "value": "35", "unit": "MWh", "icon_color":"bg-info","icon_class": "fas fa-bolt" },
    { "title": "오염된 패널 수", "value": "4", "unit": "/ 4개", "icon_color":"bg-info","icon_class": "fas fa-solar-panel" },
    { "title": "오염 레벨", "value": "경고", "unit": "", "icon_color":"bg-warning","icon_class": "fas fa-sad-tear" },
]



class cctv(LoginRequiredMixin, TemplateView):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['status_box'] = status
        return context

    def screen(request):
        try:
            cam = StreamingVideoCamera() #웹캠 호출
            # frame단위로 이미지를 계속 송출한다
            return StreamingHttpResponse(cam.gen(), content_type="multipart/x-mixed-replace;boundary=frame")
        except:
            pass


#cam 관련 클래스
class VideoCamera(object):
    def __init__(self):
        self.video = cv2.VideoCapture(0)
        (self.grabbed, self.frame) = self.video.read()
        threading.Thread(target=self.update, args=()).start()

    def __del__(self):
        self.video.release()

    def get_frame(self):
        image = self.frame
        _, jpeg = cv2.imencode('.jpg', image)
        return jpeg.tobytes()

    def update(self):
        while True:
            (self.grabbed, self.frame) = self.video.read()

    
# frame단위로 이미지를 계속 반환하게 만드는 클래스. 
class StreamingVideoCamera(object):
    def __init__(self):
        self.camera = VideoCamera()
        
    def gen(self):
        while True:
            frame = self.camera.get_frame()
            # frame단위로 이미지를 계속 반환한다. (yield)
            yield(b'--frame\r\n'
                b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')
