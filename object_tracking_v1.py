import cv2
from object_detection import ObjectDetection
import math


# Initilize object detection
od = ObjectDetection()

#Load sample.mp4 to OpenCV
cap = cv2.VideoCapture("sample.mp4")

#Initialize count
count = 0

#Initialize to store centre points in previous frame to compare them later.
centre_points_prev_frame = []

#All tracked objects
tracking_objects = {}

#track_id for the detected object
track_id = 0

#Iterating through frames
while True:

    #Reads the frame
    ret, frame = cap.read()
    count+=1
    #IF there are no objects, break
    if not ret:
        break

    # Centre ponts in current frame
    centre_points_cur_frame = []

    #Detect object detection on frame
    (class_ids, scores,boxes)  = od.detect(frame)

    for box in boxes:

        #w=width    h=height
        (x, y, w, h) = box
        
        cx = int ((x + x + w)/2 )
        cy = int ((y + y + h)/2 )
        centre_points_cur_frame.append((cx,cy))
        print("FRAME N",count, " ", x, y,w,h)

        # frame,  top left corner, bottom right corner, colour  , thickness
        cv2.rectangle(frame, (x,y), (x+w, y+h), (0, 255, 0), 2)
    
    # Only at the beginign we compare previous and curret frames.
    if count <= 2:
        for pt in centre_points_cur_frame:
            for pt2 in centre_points_prev_frame:
                distance = math.hypot(pt2[0]-pt[0],pt2[1]-pt[1])
                #If distance<20, we idntify it as a single object
                if distance < 20:
                    tracking_objects[track_id] = pt
                    track_id+=1
    else:
        tracking_objects_copy = tracking_objects.copy()
        centre_points_cur_frame_copy = centre_points_cur_frame.copy()
        for object_id, pt2 in tracking_objects.copy().items():
            object_exists = False
            for pt in centre_points_cur_frame_copy:
                distance = math.hypot(pt2[0]-pt[0],pt2[1]-pt[1])
                
                # Update the object position
                if distance < 20:
                    tracking_objects[object_id] = pt
                    object_exists = True
                    if pt in centre_points_cur_frame:
                        centre_points_cur_frame.remove(pt)
                    continue
            
            #Remove the id
            if not object_exists:
                tracking_objects.pop(object_id)

        #Add new Ids found
        for pt in centre_points_cur_frame:
            tracking_objects[track_id] = pt
            track_id += 1

    #Put Ids on the objects.
    for object_id, pt in tracking_objects.items():
      #  cv2.circle(frame, (cx,cy), 5, (0,0,255), -1)

        #frame, text, point, font type, _, colour, thickness
        cv2.putText(frame, str(object_id), (pt[0],pt[1]-7), 0, 1, (0,0,255), 2)

    cv2.imshow("Frame",frame)
    
    # Make a copy of the points
    centre_points_prev_frame = centre_points_cur_frame.copy()

    #Set program to exit when Esc is pressed.
    key = cv2.waitKey(1)
    if key==27:
        break

cap.release()
cv2.destroyAllWindows()