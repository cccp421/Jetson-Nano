import cv2
print(cv2.__version__)
dispW=640
dispH=480
flip=2
from adafruit_servokit import ServoKit
kit = ServoKit(channels=16)
pan = 90
tilt = 90
kit.servo[0].angle=pan
kit.servo[1].angle=tilt
 

# webcam =  f"v4l2src device=/dev/video0 io-mode=2 " \
#             f"! image/jpeg, width={dispW}, height={dispH}, framerate=30/1, format=MJPG " \
#             f"! nvv4l2decoder mjpeg=1 " \
#             f"! nvvidconv " \
#             f"! video/x-raw, format=BGRx " \
#             f"! videoconvert " \
#             f"! video/x-raw, format=BGR " \
#             f"! appsink drop=1"
# cam=cv2.VideoCapture(webcam, cv2.CAP_GSTREAMER)
#Or, if you have a WEB cam, uncomment the next line
#(If it does not work, try setting to '1' instead of '0')
        
cam=cv2.VideoCapture(1)
# width=cam.get(cv2.CAP_PROP_FRAME_WIDTH)
# height=cam.get(cv2.CAP_PROP_FRAME_HEIGHT)

face_cascade = cv2.CascadeClassifier('/home/cccp/Desktop/pyPro/cascade/haarcascade_frontalface_alt.xml')
eye_cascade = cv2.CascadeClassifier('/home/cccp/Desktop/pyPro/cascade/haarcascade_eye.xml')
while True:
    ret, frame = cam.read()

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)

    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 4)
        objX=x+w/2
        objY=y+h/2
        errorPan=objX-dispW/2
        errorTilt=objY-dispH/2
        if abs(errorPan)>15:
            pan=pan-errorPan/50
        if abs(errorTilt)>15:
            tilt=tilt-errorTilt/50

        if pan>180:
            pan=180
            print("Pan Out of  Range")   
        if pan<0:
            pan=0
            print("Pan Out of  Range") 
        if tilt>180:
            tilt=180
            print("Tilt Out of  Range") 
        if tilt<0:
            tilt=0
            print("Tilt Out of  Range")                 
 
        kit.servo[1].angle=pan
        kit.servo[0].angle=tilt

        roi_gray = gray[y:y+h, x:x+w]
        roi_color = frame[y:y+h, x:x+w]
        eyes = eye_cascade.detectMultiScale(roi_gray)

        for (xe, ye, we, he) in eyes:
            cv2.rectangle(roi_color, (xe, ye), (xe+we, ye+he), (0, 255, 0), 3)

    cv2.imshow('cam',frame)
    cv2.moveWindow('cam', 0, 0)
    if cv2.waitKey(1)==ord('q'):
        break

cam.release()
cv2.destroyAllWindows()