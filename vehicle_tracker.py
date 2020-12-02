import numpy as np
from vehicle import vehicle

MAX_MOVE = 0.3
MAX_UNDETECTION = 10

def euclidean_distance(vehicle_obj, bounding_box):
  '''
    parameters:
    vehicle_obj -> instance of vehicle object
    bounding_box -> array representing a bounding box

    returns:
    euclidean distance or -1
  '''

  #centroid of current bounding box
  ty,tx,by,bx = bounding_box
  cx = (tx+bx)/2
  cy = (ty+by)/2
  #centroid of vehicle
  v_centroid = vehicle_obj.centroid[-1]
  vcy,vcx = v_centroid.y, v_centroid.x
  #distance b/w the centroids
  distance = ((vcx-cx)**2 + (vcy-cy)**2)**0.5
  #finding diagonal of vehicle bounding box
  tl,br = vehicle_obj.box
  tbx,tby = tl.x, tl.y
  bbx,bby = br.x, br.y
  diagonal = ((tbx-bbx)**2 + (tby-bby)**2)**0.5
  
  if distance <= MAX_MOVE*diagonal:
    return distance

  return -1


def tracker(vehicle_list, new_bounding_box):
  '''
    parameters :
    vehicle_list -> list of previously detected vehicle
    new_bounding_box -> currently detected bounding box
  '''
  #DEBUG INFO
  print(f'no of current detection : {len(new_bounding_box)}')
  print(f'no of previous detection : {len(vehicle_list)}')
  #END

  unassigned = [i for i in range(len(new_bounding_box))]
  updated_list = []

  #assigning new coordinates to previously detected vehicle
  for index, bounding_box in enumerate(new_bounding_box):
    nearest =(None,None) #(vehicle index, distance)
    for v_index, vehicle_obj in enumerate(vehicle_list):
      distance = euclidean_distance(vehicle_obj, bounding_box)
      if(distance>=0):
        if nearest[1] is None : 
          nearest=(v_index,distance)
        else:
          if(distance<nearest[1]):
            nearest=(v_index,distance)

    #update previously detected vehicle
    if nearest[0] is not None:
      vehicle_obj = vehicle_list[nearest[0]]
      vehicle_obj.update(new_bounding_box[index])

      del(vehicle_list[nearest[0]])
      updated_list.append(vehicle_obj)
      unassigned.remove(index)

  #unassigned bounding box
  new_bounding_box = new_bounding_box[unassigned]
  for box in new_bounding_box:
    updated_list.append(vehicle(box))

  #undetected vehicle
  for vehicle_obj in vehicle_list:
    vehicle_obj.undetected_for += 1
    if  vehicle_obj.undetected_for <= MAX_UNDETECTION : 
      updated_list.append(vehicle_obj)
  
  #DEBUG INFO
  print(f'total assigned : {len(updated_list)}')
  #END

  #return updated vehicle object list
  return updated_list
  

  

