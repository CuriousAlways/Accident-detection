class coordinate:
  def __init__(self,y,x):
    self.x = x
    self.y = y

class vehicle:
  id = 0
  #store information upto specified foi
  foi = 5
  def __init__(self,bounding_box):
    '''
      initialize a vehicle instance
    '''
    top_left = coordinate(bounding_box[0],bounding_box[1])
    bottom_right = coordinate(bounding_box[2],bounding_box[3])

    self.box = (top_left,bottom_right)
    self.centroid = [coordinate((top_left.y+bottom_right.y)/2,(top_left.x+bottom_right.x)/2)]
    self.v_id = vehicle.id
    self.undetected_for = 0
    vehicle.id+=1
  
  def update(self,bounding_box):
    '''
      update the object description
    '''
    top_left = coordinate(bounding_box[0],bounding_box[1])
    bottom_right = coordinate(bounding_box[2],bounding_box[3])

    self.box = (top_left,bottom_right)
    self.centroid.append(coordinate((top_left.y+bottom_right.y)/2,(top_left.x+bottom_right.x)/2))

    if len(self.centroid)>vehicle.foi:
      while len(self.centroid)>vehicle.foi:
        del(self.centroid[0])
    
    self.undetected_for = 0
    
      
    


