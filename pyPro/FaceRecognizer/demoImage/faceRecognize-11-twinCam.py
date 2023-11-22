from threading import Thread
import cv2
import time
import numpy as np

class vStream: 
    def __init__(self, src, width, height):
        self.width = width
        self.height = height
        self.capture = cv2.VideoCapture(src, cv2.CAP_GSTREAMER)
        self.thread = Thread(target=self.update, args=())
        self.thread.daemon = True
        self.thread.start()
    def update(self):
        while True:
            _, self.frame = self.capture.read()
            self.frame2 = cv2.resize(self.frame, (self.width, self.height))
    def getFrame(self):
        return self.frame2

dispW = 640
dispH = 360
webcam1 = f"v4l2src device=/dev/video0 io-mode=2 " \
            f"! image/jpeg, width={dispW}, height={dispH}, framerate=30/1, format=MJPG " \
            f"! nvv4l2decoder mjpeg=1 " \
            f"! nvvidconv " \
            f"! video/x-raw, format=BGRx " \
            f"! videoconvert " \
            f"! video/x-raw, format=BGR " \
            f"! appsink drop=1"
webcam2 =  f"v4l2src device=/dev/video1 io-mode=2 " \
            f"! image/jpeg, width={dispW}, height={dispH}, framerate=30/1, format=MJPG " \
            f"! nvv4l2decoder mjpeg=1 " \
            f"! nvvidconv " \
            f"! video/x-raw, format=BGRx " \
            f"! videoconvert " \
            f"! video/x-raw, format=BGR " \
            f"! appsink drop=1"

cam1 = vStream(webcam1, dispW, dispH)
cam2 = vStream(webcam2, dispW, dispH)
font = cv2.FONT_HERSHEY_SIMPLEX
startTime = time.time()
dtav = 0

# cam1.set(cv2.CAP_PROP_FRAME_WIDTH, dispW)
# cam1.set(cv2.CAP_PROP_FRAME_HEIGHT, dispH)
# cam2.set(cv2.CAP_PROP_FRAME_WIDTH, dispW)
# cam2.set(cv2.CAP_PROP_FRAME_HEIGHT, dispH)

while True:
    try:
        myFrame1 = cam1.getFrame()
        myFrame2 = cam2.getFrame()
        myFrame3 = np.hstack((myFrame1, myFrame2)) 

        dt = time.time()-startTime
        startTime = time.time()
        dtav = .9*dtav + .1*dt
        fps = 1/dtav
        cv2.rectangle(myFrame3, (0, 0), (100, 40), (0, 0, 255), -1)
        cv2.putText(myFrame3, str(round(fps, 1))+ 'fps', (0, 25), font, .75, (0, 255, 255), 2)
        cv2.imshow('myCam', myFrame3)
        # cv2.imshow('cam2', myFrame2)
        cv2.moveWindow('myCam', 0, 0)
        # print(fps)
    except:
        # pass
        print('frame not available')
    if cv2.waitKey(1) == ord('q'):
        cam1.capture.release()
        cam2.capture.release()
        cv2.destroyAllWindow()
        exit(1)
        break