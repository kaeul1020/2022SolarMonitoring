import cv2
import matplotlib.pyplot as plt
from PIL import Image
from matplotlib import image
import numpy as np
import skimage.io
import argparse
from skimage.color import rgb2gray, rgb2hsv
from skimage.filters import sobel
from skimage import morphology
import numpy as np
import matplotlib.pyplot as plt
import os
from os import listdir
from os.path import isfile, join
import glob
import uuid
from tqdm import tqdm

class Crop(object):
    def __init__(self):
        print("crop 들어옴")
    

    def order_points(self, pts):
        # initialzie a list of coordinates that will be ordered
        # such that the first entry in the list is the top-left,
        # the second entry is the top-right, the third is the
        # bottom-right, and the fourth is the bottom-left
        rect = np.zeros((4, 2), dtype = "float32")
        
        # the top-left point will have the smallest sum, whereas
        # the bottom-right point will have the largest sum
        s = pts.sum(axis = 1)
        rect[0] = pts[np.argmin(s)]
        rect[2] = pts[np.argmax(s)]
        
        # now, compute the difference between the points, the
        # top-right point will have the smallest difference,
        # whereas the bottom-left will have the largest difference
        diff = np.diff(pts, axis = 1)
        rect[1] = pts[np.argmin(diff)]
        rect[3] = pts[np.argmax(diff)]
        
        # return the ordered coordinates
        return rect
    

    def four_point_transform(self, image, pts):
        # obtain a consistent order of the points and unpack them
        # individually
        rect = self.order_points(pts)
        (tl, tr, br, bl) = rect
        
        # compute the width of the new image, which will be the
        # maximum distance between bottom-right and bottom-left
        # x-coordiates or the top-right and top-left x-coordinates
        widthA = np.sqrt(((br[0] - bl[0]) ** 2) + ((br[1] - bl[1]) ** 2))
        widthB = np.sqrt(((tr[0] - tl[0]) ** 2) + ((tr[1] - tl[1]) ** 2))
        maxWidth = max(int(widthA), int(widthB))
        
        # compute the height of the new image, which will be the
        # maximum distance between the top-right and bottom-right
        # y-coordinates or the top-left and bottom-left y-coordinates
        heightA = np.sqrt(((tr[0] - br[0]) ** 2) + ((tr[1] - br[1]) ** 2))
        heightB = np.sqrt(((tl[0] - bl[0]) ** 2) + ((tl[1] - bl[1]) ** 2))
        maxHeight = max(int(heightA), int(heightB))
        
        # now that we have the dimensions of the new image, construct
        # the set of destination points to obtain a "birds eye view",
        # (i.e. top-down view) of the image, again specifying points
        # in the top-left, top-right, bottom-right, and bottom-left
        # order
        dst = np.array([
            [0, 0],
            [maxWidth - 1, 0],
            [maxWidth - 1, maxHeight - 1],
            [0, maxHeight - 1]], dtype = "float32")
        
        # compute the perspective transform matrix and then apply it
        M = cv2.getPerspectiveTransform(rect, dst)
        warped = cv2.warpPerspective(image, M, (maxWidth, maxHeight))
        
        # return the warped image
        return warped

    def getFrame(self, frame, pt):
        # Read original image
        image = cv2.cvtColor(frame,
                            cv2.COLOR_BGR2RGB)
        # Cropping
        img = self.four_point_transform(image,pt)
        
        # Save cropped image
        return cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    def drawROI(self, img, corners):
        cpy = img.copy()

        c1 = (192, 192, 255)
        c2 = (128, 128, 255)

        for pt in corners:
            print(pt)
            cv2.circle(cpy, tuple(pt.astype(int)), 25, c1, -1, cv2.LINE_AA)
        
        # cv2.drawContours(cpy, [corners], -1, c2, 4)
        cv2.line(cpy, tuple(corners[0].astype(int)), tuple(corners[1].astype(int)), c2, 4, cv2.LINE_AA)
        cv2.line(cpy, tuple(corners[1].astype(int)), tuple(corners[2].astype(int)), c2, 4, cv2.LINE_AA)
        cv2.line(cpy, tuple(corners[2].astype(int)), tuple(corners[3].astype(int)), c2, 4, cv2.LINE_AA)
        cv2.line(cpy, tuple(corners[3].astype(int)), tuple(corners[0].astype(int)), c2, 4, cv2.LINE_AA)
        disp = cv2.addWeighted(img, 0.3, cpy, 0.7, 0)

        return disp