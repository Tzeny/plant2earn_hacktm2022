import math  
from detectron2.engine import DefaultTrainer
from detectron2.config import get_cfg
from detectron2 import model_zoo
from detectron2.engine import DefaultPredictor
from detectron2.config import get_cfg
from detectron2.utils.visualizer import Visualizer
from detectron2.data import MetadataCatalog
from PIL import Image
import cv2
import os
import torch

import numpy as np
#function to get the leaf image.

def get_cropped_leaf(img,predictor,return_mapping=False,resize=None):
    #convert to numpy    
    img = np.array(img)[:,:,::-1]
    img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
    
    #get prediction
    outputs = predictor(img)
    
    #get boxes and masks
    ins = outputs["instances"]
    pred_masks = ins.get_fields()["pred_masks"]
    boxes = ins.get_fields()["pred_boxes"]    
    
    #get main leaf mask if the area is >= the mean area of boxes and is closes to the centre 
    
    masker = pred_masks[np.argmin([calculateDistance(x[0], x[1], int(img.shape[1]/2), int(img.shape[0]/2)) for i,x in enumerate(boxes.get_centers()) if (boxes[i].area()>=torch.mean(boxes.area()).to("cpu")).item()])].to("cpu").numpy().astype(np.uint8)

    #mask image
    mask_out = cv2.bitwise_and(img, img, mask=masker) + np.array(((255 - masker), (255 - masker), (255 - masker))).reshape(img.shape)
    
    #find contours and boxes
    contours, hierarchy = cv2.findContours(masker.copy() ,cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    contour = contours[np.argmax([cv2.contourArea(x) for x in contours])]
    rotrect = cv2.minAreaRect(contour)
    box = cv2.boxPoints(rotrect)
    box = np.int0(box)
    

    #crop image
    # cropped = get_cropped(rotrect,box,mask_out)

    #resize
    # rotated = MakeLandscape()(Image.fromarray(cropped))
    
    # if not resize == None:
    #     resized = ResizeMe((resize[0],resize[1]))(rotated)
    # else:
    #     resized = rotated
        
    if return_mapping:
        # img = cv2.drawContours(img, [box], 0, (0,0,255), 10)
        img = cv2.drawContours(img, contours, -1, (255,150,), 10)
        # return resized, ResizeMe((int(resize[0]),int(resize[1])))(Image.fromarray(img))
        return Image.fromarray(mask_out), Image.fromarray(img)
    
    return resized

#function to crop the image to boxand rotate

def get_cropped(rotrect,box,image):
    
    width = int(rotrect[1][0])
    height = int(rotrect[1][1])

    src_pts = box.astype("float32")
    # corrdinate of the points in box points after the rectangle has been
    # straightened
    dst_pts = np.array([[0, height-1],
                        [0, 0],
                        [width-1, 0],
                        [width-1, height-1]], dtype="float32")

    # the perspective transformation matrix
    M = cv2.getPerspectiveTransform(src_pts, dst_pts)

    # directly warp the rotated rectangle to get the straightened rectangle
    warped = cv2.warpPerspective(image, M, (width, height))
    return warped

def calculateDistance(x1,y1,x2,y2):  
    dist = math.hypot(x2 - x1, y2 - y1)
    return dist  

class ResizeMe(object):
    #resize and center image in desired size 
    def __init__(self,desired_size):
        
        self.desired_size = desired_size
        
    def __call__(self,img):
    
        img = np.array(img).astype(np.uint8)
        
        desired_ratio = self.desired_size[1] / self.desired_size[0]
        actual_ratio = img.shape[0] / img.shape[1]

        desired_ratio1 = self.desired_size[0] / self.desired_size[1]
        actual_ratio1 = img.shape[1] / img.shape[0]

        if desired_ratio < actual_ratio:
            img = cv2.resize(img,(int(self.desired_size[1]*actual_ratio1),self.desired_size[1]),None,interpolation=cv2.INTER_AREA)
        elif desired_ratio > actual_ratio:
            img = cv2.resize(img,(self.desired_size[0],int(self.desired_size[0]*actual_ratio)),None,interpolation=cv2.INTER_AREA)
        else:
            img = cv2.resize(img,(self.desired_size[0], self.desired_size[1]),None, interpolation=cv2.INTER_AREA)
            
        h, w, _ = img.shape

        new_img = np.zeros((self.desired_size[1],self.desired_size[0],3))
        
        hh, ww, _ = new_img.shape

        yoff = int((hh-h)/2)
        xoff = int((ww-w)/2)
        
        new_img[yoff:yoff+h, xoff:xoff+w,:] = img

        
        return Image.fromarray(new_img.astype(np.uint8))

class MakeLandscape():
    #flip if needed
    def __init__(self):
        pass
    def __call__(self,img):
        
        if img.height> img.width:
            img = np.rot90(np.array(img))
            img = Image.fromarray(img)
        return img

class SegmentationHandler:
    def __init__(self, model_path):
        cfg = get_cfg()
        cfg.merge_from_file(model_zoo.get_config_file("COCO-InstanceSegmentation/mask_rcnn_R_50_FPN_3x.yaml"))
        cfg.DATASETS.TRAIN = ()
        cfg.DATALOADER.NUM_WORKERS = 4
        cfg.MODEL.DEVICE = "cpu"

        cfg.MODEL.ROI_HEADS.BATCH_SIZE_PER_IMAGE = (8)  # faster, and good enough for this toy dataset
        cfg.MODEL.ROI_HEADS.NUM_CLASSES = 2  # 3 classes (data, fig, hazelnut)

        os.makedirs(cfg.OUTPUT_DIR, exist_ok=True)
        
        cfg.MODEL.WEIGHTS = model_path
        cfg.MODEL.ROI_HEADS.SCORE_THRESH_TEST = 0.7   # set the testing threshold for this model
        self.predictor = DefaultPredictor(cfg)

    def segment_leaf(self, input_path, output_path_1, output_path_2):
        img, img1 = get_cropped_leaf(Image.open(input_path),self.predictor,return_mapping=True,resize = (512,int(512*.7)))

        img.save(output_path_1)
        img1.save(output_path_2)
