
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


class Segmentation(object):
    def __init__(self):
        print("SegmentationCam.py __init__ 들어옴")
        #fcn model
        self.device = torch.device('cpu')
        self.model_fcn = torchfcn.models.FCN8s(n_class=2)
        self.model_fcn.eval()
        self.model_data = torch.load('./cctv/FCN_model_best.pth.tar',map_location=self.device) #model file 위치
        try:
            self.model_fcn.load_state_dict(self.model_data)
        except Exception:
            self.model_fcn.load_state_dict(self.model_data['model_state_dict'])
        self.mean_bgr = np.array([104.00698793, 116.66876762, 122.67891434])

        self.model_uNet = tf.keras.models.load_model('./cctv/UNet_0823_newdataset_pat10.h5')
    
    def predictColoring(frame, pred_model):
        start = time.time()
        try : 
            score = np.bincount(pred_model.flatten().tolist())[1]
            score = (score/(pred_model.shape[0]*pred_model.shape[1]))*100
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
        print("cnt :",cnt)
        print(pred_model.shape[0],pred_model.shape[1])
        
        print("seg time :", time.time() - start)
        
        return {"frame":frame, "score":score}
    
    def FCN(self, frame):
        #openCV Image to PIL Image
        start = time.time()
        image = cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
        img = Image.fromarray(image).convert('RGB')
        print("openCV Image to PIL Image time :", time.time() - start)

        #FCN image
        start = time.time()
        img = np.array(img, dtype=np.uint8)[:, :, ::-1] # RGB -> BGR
        img = img.astype(np.float64)
        img -= self.mean_bgr
        img = img.transpose(2, 0, 1)
        img = torch.from_numpy(img).float().unsqueeze(0)
        print("FCN image time :", time.time() - start)

        #FCN
        start = time.time()
        pred_fcn = self.model_fcn(img)
        print("pred FCN time :", time.time() - start)
        start = time.time()
        pred_fcn = pred_fcn.data.max(1)[1].cpu().numpy()[0]
        print("max FCN time :", time.time() - start)

        return self.predictColoring(frame, pred_fcn)

    def U_Net(self, frame):
        #u-net iamge
        frame = cv2.resize(frame,(510,380))

        frame_unet = cv2.resize(frame,(112,112))
        image_unet = frame_unet
        image_unet = np.reshape(image_unet,(112,112,-1))
        image_unet = np.array([image_unet])/255
        pred_unet = self.model_uNet.predict(image_unet)
        pred_unet = pred_unet[0]

        _, pred_unet = cv2.threshold(np.array(pred_unet*255,dtype='uint8'),0,255,cv2.THRESH_OTSU)
            
        result= self.predictColoring(frame_unet, pred_unet)
        result['frame'] = cv2.resize(result['frame'],(510,380))
        
        return result
        
