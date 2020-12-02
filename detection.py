import sys
import os
import cv2
import numpy as np
from mrcnn.config import Config
import mrcnn.model as rcnn

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

CLASS_NAMES = ['BG', 'person', 'bicycle', 'car', 'motorcycle', 'airplane', 'bus', 'train',
 'truck', 'boat', 'traffic light', 'fire hydrant', 'stop sign', 'parking meter', 'bench', 'bird', 'cat', 'dog', 'horse', 'sheep', 'cow', 'elephant', 'bear', 'zebra', 'giraffe', 'backpack', 'umbrella', 'handbag', 'tie', 'suitcase', 'frisbee', 'skis', 'snowboard', 'sports ball', 'kite', 'baseball bat', 'baseball glove', 'skateboard', 'surfboard', 'tennis racket', 'bottle', 'wine glass', 'cup', 'fork', 'knife', 'spoon', 'bowl', 'banana', 'apple', 'sandwich', 'orange', 'broccoli', 'carrot', 'hot dog', 'pizza', 'donut', 'cake', 'chair', 'couch', 'potted plant', 'bed', 'dining table', 'toilet', 'tv', 'laptop', 'mouse', 'remote', 'keyboard', 'cell phone', 'microwave', 'oven', 'toaster', 'sink', 'refrigerator', 'book', 'clock', 'vase', 'scissors', 'teddy bear', 'hair drier', 'toothbrush']

ID_ACCEPTABLE=[3,6,8] #[car,bus,truck]
SCORE_ACCEPTABLE =0.75


class SimpleConfig(Config):
  '''Overiding default configuration'''
  NAME = 'vehicle_detection'
  GPU_COUNT = 1
  IMAGES_PER_GPU = 1
  # BACKBONE = "resnet50"
  #Using weights pretrained on coco dataset which has 81 classes 
  NUM_CLASSES = 81 


model = rcnn.MaskRCNN(mode='inference',
                            config=SimpleConfig(),
                            model_dir=os.getcwd()
                          )

model.load_weights(filepath='mask_rcnn_coco.h5',by_name=True)


def get_bounding_box(image,accepted_ids=ID_ACCEPTABLE, accepted_score=SCORE_ACCEPTABLE):
  '''
    parmeters:
    image -> image for detection
    accepted_ids -> ids of object to be detected in image
    accepted_score -> threshold probability for valid detection
    returns:
    ndarray of bounding boxes of detected objects
  '''
  image_modified = cv2.cvtColor(image,cv2.COLOR_BGR2RGB)
  detected = model.detect(images=[image_modified],verbose=1)
  #filter for only requested ids and score
  score_mask = detected[0]['scores']>=SCORE_ACCEPTABLE
  temp = np.zeros(detected[0]['class_ids'].shape,dtype=int)!=0
  for acceptable_id in ID_ACCEPTABLE:
    temp = temp | (detected[0]['class_ids'] == acceptable_id)

  detected_rois = detected[0]['rois'][(temp)&(score_mask)] 

  return detected_rois
