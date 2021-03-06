import sys
import cv2
import detection
import time
from vehicle import vehicle

#image1
image_locn = sys.argv[1]
source_vid = cv2.VideoCapture(image_locn)
TFC = int(source_vid.get(cv2.CAP_PROP_FRAME_COUNT))
FPS = int(source_vid.get(cv2.CAP_PROP_FPS))
WIDTH = int(source_vid.get(cv2.CAP_PROP_FRAME_WIDTH))
HEIGHT = int(source_vid.get(cv2.CAP_PROP_FRAME_HEIGHT))

fourcc = cv2.VideoWriter_fourcc(*'XVID')
dest_vid = cv2.VideoWriter('ouptput.mp4',fourcc,FPS,(WIDTH,HEIGHT))

curr_frame = 1
while source_vid.isOpened():
  status, frame = source_vid.read()
  if status:
    print(f'total frame : {TFC}, curr_frame : {curr_frame}\n----------------------------------\n')
    bounding_box = detection.get_bounding_box(frame)
    #let's create a vehicle instance
    if len(bounding_box)>0:
      v = [ vehicle(box) for box in bounding_box ]

      for v1 in v:
        y1,x1,y2,x2 = v1.box[0].y, v1.box[0].x, v1.box[1].y, v1.box[1].x
        xc,yc = int(v1.centroid[0].x), int(v1.centroid[0].y)
        cv2.rectangle(frame,pt1=(x1,y1),pt2=(x2,y2),color=(0,255,0),thickness=2)
        cv2.circle(frame,center=(xc,yc),radius=5,color=(0,165,255),thickness=-1)
        font=cv2.FONT_HERSHEY_SIMPLEX
        text=str(v1.v_id)
        cv2.putText(frame,text=text,org=(xc,yc+3),fontFace=font,
                    fontScale=1,color=(0,255,0),thickness=3,lineType=cv2.LINE_AA
                  )
    dest_vid.write(frame)
    curr_frame+=1
  else:
    source_vid.release()
    dest_vid.release()
    break
