import sys
import cv2
import detection
import time
from vehicle import vehicle
import vehicle_tracker as vt


image_locn = sys.argv[1]
source_vid = cv2.VideoCapture(image_locn)
TFC = int(source_vid.get(cv2.CAP_PROP_FRAME_COUNT))
FPS = int(source_vid.get(cv2.CAP_PROP_FPS))
WIDTH = int(source_vid.get(cv2.CAP_PROP_FRAME_WIDTH))
HEIGHT = int(source_vid.get(cv2.CAP_PROP_FRAME_HEIGHT))

fourcc = cv2.VideoWriter_fourcc(*'XVID')
output = sys.argv[2]
dest_vid = cv2.VideoWriter(output,fourcc,FPS,(WIDTH,HEIGHT))

vehicle_list = []
current_frame = 1

while source_vid.isOpened():
  status, frame = source_vid.read()
  if status:
    print('\n----------------------------------\n')
    print(f'total frame :{TFC},current_frame : {current_frame}')
    print('\n----------------------------------\n')
    bounding_box = detection.get_bounding_box(frame)

    vehicle_list = vt.tracker(vehicle_list,bounding_box)

    for v1 in vehicle_list:
        if v1.undetected_for == 0:
          y1,x1,y2,x2 = v1.box[0].y, v1.box[0].x, v1.box[1].y, v1.box[1].x
          xc,yc = int(v1.centroid[-1].x), int(v1.centroid[-1].y)
          cv2.rectangle(frame,pt1=(x1,y1),pt2=(x2,y2),color=(0,255,0),thickness=2)
          # cv2.circle(frame,center=(xc,yc),radius=5,color=(0,165,255),thickness=-1)
          font=cv2.FONT_HERSHEY_SIMPLEX
          text=str(v1.v_id)
          cv2.putText(frame,text=text,org=(xc,yc+3),fontFace=font,
                      fontScale=0.5,color=(0,255,0),thickness=1,lineType=cv2.LINE_AA
                    )

    dest_vid.write(frame)
    current_frame+=1
  else:
    source_vid.release()
    dest_vid.release()
    break