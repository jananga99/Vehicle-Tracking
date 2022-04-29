import cv2
from object_detection import ObjectDetection
import math
import time

#if p2==0:
#    p1=newlocation
#else
#   p1=old location
#   p2=new location
def Danger(frame,cv2,p1,p2=0):
    danger_x_l = 400
    danger_x_r = 1100
    danger_y = 600
    
    if(p2==0):
        after_2s_x = p1[0]
        after_2s_y = p1[1]
        p2 = p1
    else:
        dx = p2[0]-p1[0]
        dy = p2[1]-p1[1]
        dt = p2[2]-p1[2]
        vx = dx/dt
        vy = dy/dt
        after_2s_x = p2[0]+vx*10
        after_2s_y = p2[1]+vy*10
    #print(after_2s_x,after_2s_y)            
    if(danger_x_l<=after_2s_x<=danger_x_r and after_2s_y>=danger_y):
        cv2.putText(frame,"WARNING",(p2[0],p2[1]), 0, 1, (0,0,255), 2)
    else:
        cv2.putText(frame,"GOOD",(p2[0],p2[1]), 0, 1, (0,0,255), 2)

# Initilize object detection
od = ObjectDetection()

cap = cv2.VideoCapture("los_angeles.mp4")
fps =  cap.get(cv2.CAP_PROP_FPS);
frame_time_diffrence =1/fps

#Initialize count
count = 0
centre_points_prev_frame = []

tracking_objects = {}
prev_tracking_objects = {}

track_id = 0
while True:
    ret, frame = cap.read()
    cv2.line(frame,(400,600),(1100,600),(0,0,255))
    count+=1

    #IF there are no objects, break
    if not ret:
        break

    centre_points_cur_frame = []
    (class_ids, scores,boxes)  = od.detect(frame)

    for box in boxes:

        (x, y, w, h) = box
        cx = int ((x + x + w)/2 )
        cy = int ((y + y + h)/2 )
        centre_points_cur_frame.append((cx,cy))
        #print("FRAME N",count, " ", x, y,w,h)

        cv2.rectangle(frame, (x,y), (x+w, y+h), (0, 255, 0), 2)
    
    # Only at the beginign we compare previous and curret frames.
    if count <= 2:
        for pt in centre_points_cur_frame:
            for pt2 in centre_points_prev_frame:
                distance = math.hypot(pt2[0]-pt[0],pt2[1]-pt[1])
                if distance < 20:
                    tracking_objects[track_id] = (pt[0],pt[1],time.time())
                    Danger(frame,cv2,(pt[0],pt[1],time.time()))
                    track_id+=1
    else:
        tracking_objects_copy = tracking_objects.copy()
        centre_points_cur_frame_copy = centre_points_cur_frame.copy()
        for object_id, pt2 in tracking_objects.copy().items():
            object_exists = False
            for pt in centre_points_cur_frame_copy:
                distance = math.hypot(pt2[0]-pt[0],pt2[1]-pt[1])
                if distance < 20:
                    tracking_objects[object_id] = (pt[0],pt[1],time.time())
                    Danger(frame,cv2,(pt[0],pt[1],time.time()),prev_tracking_objects[object_id])
                    object_exists = True
                    if pt in centre_points_cur_frame:
                        centre_points_cur_frame.remove(pt)
                    continue
            
            #Remove the id
            if not object_exists:
                tracking_objects.pop(object_id)

        #Add new Ids found
        for pt in centre_points_cur_frame:
            tracking_objects[track_id] = (pt[0],pt[1],time.time())
            Danger(frame,cv2,(pt[0],pt[1],time.time()))
            track_id += 1

    prev_tracking_objects = tracking_objects.copy()

    for object_id, pt in tracking_objects.items():
        cv2.circle(frame, (cx,cy), 5, (0,0,255), -1)

        #frame, text, point, font type, _, colour, thickness
       # cv2.putText(frame, str(object_id), (pt[0],pt[1]-7), 0, 1, (0,0,255), 2)

    cv2.imshow("Frame",frame)
    
    # Make a copy of the points
    centre_points_prev_frame = centre_points_cur_frame.copy()

    key = cv2.waitKey(1)
    if key==27:
        break

cap.release()
cv2.destroyAllWindows()