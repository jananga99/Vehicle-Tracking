# Vehicle-Tracking
Processes a video stream from a vehicle dash cam and track the movement of vehicles in the video stream. Predicts the movement of tracked vehicles for two seconds ahead. Users can mark an area as danger area. If a vehicle is predictedto enter the danger area in the next two seconds, a warnng should be generated.


# Steps for project execute

(1) Install Opencv <br />
        pip install opencv-python

(2) Set 'dnn_model' folder as follows. <br />
    (Download needed resources). <br />
    dnn_model <br />
    |-- yolov4.cfg <br />
    |-- yolov4.weights <br />
    |-- classes.txt <br />
       
(4) Run object_tracking_v1.py <br />
