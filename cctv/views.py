from django.views.generic.base import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin

from django.http import StreamingHttpResponse
import cv2


from cctv.segmentationCam import StreamingVideoCamera as Cam
from django.http import HttpResponse
import json

status= [
    { "title": "오염 유형", "value": "나뭇잎, 흙먼지", "unit": "", "icon_color":"bg-info","icon_class": "fas fa-broom" },
    { "title": "예상 발전 감소량", "value": "35", "unit": "MWh", "icon_color":"bg-info","icon_class": "fas fa-bolt" },
    { "title": "오염된 패널 수", "value": "4", "unit": "/ 4개", "icon_color":"bg-info","icon_class": "fas fa-solar-panel" },
    { "title": "오염 레벨", "value": "경고", "unit": "", "icon_color":"bg-warning","icon_class": "fas fa-sad-tear" },
]


class Screen(object):
    def __init__(self) -> None:
        self.cam = Cam() #웹캠 호출
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
