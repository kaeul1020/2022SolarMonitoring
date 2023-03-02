
import warnings

warnings.filterwarnings('ignore')
import cv2
import numpy as np
import time

# FCN
from PIL import Image
import torch
import torchfcn

# U-Net
import tensorflow as tf

# DeepLab
from cctv.DeepLabModeling.deeplab import *
from torchvision import transforms

#crop
from cctv.crop import Crop
# realtime
import threading

from django.conf import settings


class SegmentationModels(object):
    def __init__(self, modelName):
        print("SegmentationCam.py __init__ 들어옴")

        self.modelName = modelName
        self.device = torch.device('cpu')

        if self.modelName == "FCN":
            # FCN setting
            self.model_fcn = torchfcn.models.FCN8s(n_class=2)
            self.model_fcn.eval()
            self.model_data = torch.load('./cctv/trainedModels/FCN_model_best.pth.tar',map_location=self.device) #model file 위치
            try:
                self.model_fcn.load_state_dict(self.model_data)
            except Exception:
                self.model_fcn.load_state_dict(self.model_data['model_state_dict'])
            self.mean_bgr = np.array([104.00698793, 116.66876762, 122.67891434])
        elif self.modelName == "DeepLab" :
            # DeepLab setting
            print("DeepLab setting 들어옴")
            self.model_deep = DeepLab(num_classes = 2,
                        backbone = 'xception',
                        output_stride = 16,
                        sync_bn = False,
                        freeze_bn = False)
            checkpoint_deeplab = torch.load('./cctv/trainedModels/DeepLab_model_best.pth.tar' ,map_location=self.device)
            self.model_deep.load_state_dict(checkpoint_deeplab['state_dict'])
            self.model_deep.eval()
            self.composed_transforms = transforms.Compose([
                transforms.ToTensor(),
                transforms.Normalize(mean=(0.485, 0.456, 0.406), std=(0.229, 0.224, 0.225))])
        elif self.modelName == "U_Net": 
            # U-Net setting
            self.model_uNet = tf.keras.models.load_model('./cctv/trainedModels/UNet_0823_newdataset_pat10.h5')
            pass
        else :
            print("SegmentationCam.py __init__ 에서 어느 모델도 초기화 X") 
            pass


    def predictColoring(self, frame, pred_model):
        try : 
            score = np.bincount(pred_model.flatten().tolist())[1]
            score = round((score/(pred_model.shape[0]*pred_model.shape[1]))*100, 4)
        except :
            score = 0
            
        if score <= 25 : 
            color = (59,167,40)
        elif score <= 50 : 
            color = (7,193,255)
        elif score <= 75 : 
            color = (20,126,253)
        else : 
            color = (69,53,220)

        cnt=0
        for i in range(pred_model.shape[0]):
            for j in range(pred_model.shape[1]):
                if pred_model[i][j] == 1:
                    frame[i][j] = color
                    cnt+=1
        return {"frame":frame, "score":score}
    
    def model(self, frame):
        print("self.modelName == ", self.modelName)
        
        if self.modelName == "FCN":
            start_total = time.time()
            #openCV Image to PIL Image
            image = cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
            img = Image.fromarray(image).convert('RGB')

            #FCN image
            img = np.array(img, dtype=np.uint8)[:, :, ::-1] # RGB -> BGR
            img = img.astype(np.float64)
            img -= self.mean_bgr
            img = img.transpose(2, 0, 1)
            img = torch.from_numpy(img).float().unsqueeze(0)

            #FCN
            start = time.time()
            pred_fcn = self.model_fcn(img)
            print("pred FCN time :", time.time() - start)
            start = time.time()
            pred_fcn = pred_fcn.data.max(1)[1].cpu().numpy()[0]

            result = self.predictColoring(frame, pred_fcn)
            print("total FCN time :", time.time() - start_total)

            return result
        elif self.modelName == "DeepLab" :
            start_total = time.time()

            image = cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
            image = Image.fromarray(image).convert('RGB')
            image = self.composed_transforms(image)
            image = image.unsqueeze(0)

            with torch.no_grad():
                start = time.time()
                pred_deep = self.model_deep(image)
                print("pred DeepLab time :", time.time() - start)
            
            pred_deep = pred_deep.data.cpu().numpy()
            pred_deep = np.argmax(pred_deep, axis=1)
            pred_deep = pred_deep[0]

            result = self.predictColoring(frame, pred_deep)
        
            print("total DeepLab time :", time.time() - start_total)
            return result
        elif self.modelName == "U_Net" : 
            start_total = time.time()

            #u-net iamge
            h, w, _ = frame.shape

            frame_unet = cv2.resize(frame,(112,112))
            image_unet = frame_unet
            image_unet = np.reshape(image_unet,(112,112,-1))
            image_unet = np.array([image_unet])/255
            start = time.time()
            pred_unet = self.model_uNet.predict(image_unet)
            print("pred U-Net time :", time.time() - start)
            pred_unet = pred_unet[0]

            _, pred_unet = cv2.threshold(np.array(pred_unet*255,dtype='uint8'),0,1,cv2.THRESH_BINARY)
            
            result= self.predictColoring(frame_unet, pred_unet)
            result['frame'] = cv2.resize(result['frame'],(w, h),  interpolation=cv2.INTER_CUBIC)

            print("total U-Net time :", time.time() - start_total)
            return result
        else :
            pass

#cam 관련 클래스
class VideoCamera(object):
    def __init__(self):
        self.video = cv2.VideoCapture(0)
        if self.video.isOpened():
            self.video.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
            self.video.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

            print("FRAME width, height : ", self.video.get(cv2.CAP_PROP_FRAME_WIDTH), self.video.get(cv2.CAP_PROP_FRAME_HEIGHT))

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
        self.Seg = SegmentationModels("DeepLab")
        self.crop = Crop()
        self.score ={}
        
    def getScore(self):
        try : 
            sum = 0
            for score in self.score.values():
                sum += score
            result = sum/len(self.score.values())
        except :
            result =-1
        return result

    def gen(self, segmentation=False, pt=None):
        while True:
            frame = self.camera.get_frame()

            if segmentation ==True : 
                # print("segmentation 들어옴")

                if pt is not None : 
                    np_pt = np.array(eval(pt), dtype = "float32")
                    frame = self.crop.getFrame(frame, np_pt)

                seg = self.Seg.model(frame)

                frame = seg["frame"]
                print(seg["score"])
                self.score[pt]=(seg["score"]) # TODO : 이거 값 따로 어떻게 가져올 지 생각해보기
                 
            else :
                pass

            frame = self.camera.get_image(frame=frame)
            # frame단위로 이미지를 계속 반환한다. (yield)
            yield(b'--frame\r\n'b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')
            
# 저장된 CCTV이미지용 seg 출력
class StaticSegImage(object):
    def __init__(self) -> None:
        self.Seg = SegmentationModels("DeepLab")
        self.crop = Crop()
        pass

    def getSeg(self, img, pt):
        np_pt = np.array(eval(pt), dtype = "float32")
        frame = self.crop.getFrame(img, np_pt)
        seg = self.Seg.model(frame)
        
        return seg