
import warnings

from matplotlib.animation import ImageMagickBase
warnings.filterwarnings('ignore')
import cv2
import numpy as np
from torchvision import transforms

from PIL import Image
# from modeling.deeplab import *
import torch
import torchfcn
import time

#fcn model
device = torch.device('cpu')
model_fcn = torchfcn.models.FCN8s(n_class=2)
model_data = torch.load('FCN_model_best.pth.tar',map_location=device) ####### model file 위치 적어야함!
try:
    model_fcn.load_state_dict(model_data)
except Exception:
    model_fcn.load_state_dict(model_data['model_state_dict'])



if __name__ == "__main__":
    # Connent to camera
    cap = cv2.VideoCapture(0)
    prev_time = 0
    FPS = 30
    mean_bgr = np.array([104.00698793, 116.66876762, 122.67891434])

    if not cap.isOpened():
        print("Could not open webcam")
        exit()

    model_fcn.eval()
    with torch.no_grad():
        while(cap.isOpened()):

            start_time = time.time()

            ret, frame = cap.read()
            current_time = time.time() - prev_time
            if (ret is True) and (current_time > 1./ FPS) :
                # frame_input = cv2.resize(frame,(510,380))
                cv2.imshow("Input",frame)
                #frame = cv2.resize(frame,(112,112))
                #frame_unet = frame
                #openCV Image to PIL Image
                image = cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
                img = Image.fromarray(image).convert('RGB')
                # img = image
                # image = composed_transforms(image)
                # image = image.unsqueeze(0)

                #FCN image
                img = np.array(img, dtype=np.uint8)[:, :, ::-1] # RGB -> BGR
                img = img.astype(np.float64)
                img -= mean_bgr
                img = img.transpose(2, 0, 1)
                img = torch.from_numpy(img).float().unsqueeze(0)

                '''
                # u-net iamge
                # frame_unet = cv2.resize(frame_unet,(112,112))
                # image_unet = frame_unet
                # image_unet = np.reshape(image_unet,(112,112,-1))
                # image_unet = np.array([image_unet])/255
                # pred_unet = model.predict(image_unet)
                # pred_unet = pred_unet[0]

                # _, pred_unet = cv2.threshold(np.array(pred_unet*255,dtype='uint8'),0,255,cv2.THRESH_OTSU)
                
                # for i in range(pred_unet.shape[0]):
                #     for j in range(pred_unet.shape[1]):
                #         if pred_unet[i][j] == 255:
                #             frame_unet[i][j] = (255,255,0)

                # frame_unet = cv2.resize(frame_unet,(510,380))
                # cv2.imshow("U-Net",frame_unet)

                #DeepLab
                # model_deep.eval()
                # with torch.no_grad():
                #     pred = model_deep(image)
            
                # #frame = cv2.resize(frame,(133,133))
                # frame_fcn = frame
                # pred = pred.data.cpu().numpy()
                # pred = np.argmax(pred, axis=1)
                # pred = pred[0]
            
                # for i in range(pred.shape[0]):
                #     for j in range(pred.shape[1]):
                #         if pred[i][j] == 1:
                #             frame[i][j] = (255,255,0)
                # frame = cv2.resize(frame,(112,112))        
                # frame = cv2.resize(frame,(510,380))
                # cv2.imshow("DeepLab",frame)
                '''
                #FCN
                # frame_fcn = frame
                
                pred_fcn = model_fcn(img)
                pred_fcn = pred_fcn.data.max(1)[1].cpu().numpy()[0]
                
                for i in range(pred_fcn.shape[0]):
                    for j in range(pred_fcn.shape[1]):
                        if pred_fcn[i][j] == 1:
                            frame[i][j] = (255,255,0)
                
                
                cv2.imshow(str((time.time() - start_time)*1000)+"s",frame)
                
                if cv2.waitKey(100) & 0xFF == ord('q'):
                    print("Stopped by q")
                    break
            else:
                break
        
    cap.release(all)
    cv2.destroyAllWindows()