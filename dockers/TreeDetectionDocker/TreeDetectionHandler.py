import math
from detectron2.engine import DefaultTrainer
from detectron2.config import get_cfg
from detectron2 import model_zoo
from detectron2.engine import DefaultPredictor
from detectron2.config import get_cfg
from detectron2.utils.visualizer import Visualizer
from detectron2.data import MetadataCatalog
from PIL import Image, ImageDraw
import cv2
import os
import torch

import argparse
import glob
import multiprocessing as mp
import numpy as np
import os
import tempfile
import time
import warnings
import cv2
import tqdm

from detectron2.config import get_cfg
from detectron2.data.detection_utils import read_image
from detectron2.utils.logger import setup_logger

from predictor import VisualizationDemo

import numpy as np
# function to get the leaf image.


class TreeDetectionHandler:
    def __init__(self, model_path):
        confidence_t = 0.1

        cfg = get_cfg()
        cfg.merge_from_file(model_zoo.get_config_file(
            "COCO-Detection/faster_rcnn_R_50_FPN_3x.yaml"))
        cfg.DATASETS.TRAIN = ()
        cfg.DATALOADER.NUM_WORKERS = 4
        cfg.MODEL.DEVICE = "cpu"
        # initialize from model zoo
        cfg.MODEL.WEIGHTS = "/TreeDetection/models/model_final_280758.pkl"

        # cfg.MODEL.ROI_HEADS.BATCH_SIZE_PER_IMAGE = (8)  # faster, and good enough for this toy dataset
        # cfg.MODEL.ROI_HEADS.NUM_CLASSES = 2  # 3 classes (data, fig, hazelnut)

        os.makedirs(cfg.OUTPUT_DIR, exist_ok=True)

        # cfg.MODEL.WEIGHTS = model_path
        # cfg.MODEL.ROI_HEADS.SCORE_THRESH_TEST = 0.7   # set the testing threshold for this model
        cfg.MODEL.RETINANET.SCORE_THRESH_TEST = confidence_t
        cfg.MODEL.ROI_HEADS.SCORE_THRESH_TEST = confidence_t
        cfg.MODEL.PANOPTIC_FPN.COMBINE.INSTANCES_CONFIDENCE_THRESH = confidence_t
        self.predictor = VisualizationDemo(cfg)

    def detect_tree(self, input_path, bbox_path):
        img = np.array(Image.open(input_path))[:, :, ::-1]
        img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)

        predictions, _ = self.predictor.run_on_image(img)

        class_id_dict = {
            58: 'coord_copac',
            0: 'coord_om'
        }
        resulting_bboxes = {
            'coord_om': np.array([0, 0, 0, 0]),
            'coord_copac': np.array([0, 0, 0, 0])
        }

        def get_area(bbox):
            return abs(bbox[0] - bbox[2]) * abs(bbox[1] - bbox[3])

        for bbox, score, class_id in zip(predictions['instances'].pred_boxes.tensor.numpy(), predictions['instances'].scores.numpy(), predictions['instances'].pred_classes.numpy()): 
            if class_id not in class_id_dict.keys():
                continue

            if class_id == 0 and score < 0.5:
                continue
                
            if get_area(bbox) > get_area(resulting_bboxes[class_id_dict[class_id]]):
                resulting_bboxes[class_id_dict[class_id]] = bbox
                
        resulting_bboxes['coord_om'] = resulting_bboxes['coord_om'].tolist()
        resulting_bboxes['coord_copac'] = resulting_bboxes['coord_copac'].tolist()

        pred_img = Image.open(input_path)

        draw = ImageDraw.Draw(pred_img)
        draw.rectangle(resulting_bboxes['coord_om'], outline='blue', width=5)
        draw.rectangle(resulting_bboxes['coord_copac'], outline='green', width=5)

        # write to stdout
        pred_img.save(bbox_path)

        return resulting_bboxes
