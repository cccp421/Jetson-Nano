from threading import Thread
import cv2
import time
import numpy as np
import face_recognition
import pickle

with open('train.pkl', 'rb') as f:
    Names = pickle.load(f)
    Encodings = pickle.load(f)

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

dispW = 320
dispH = 240
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
scaleFactor = .5

while True:
    try:
        myFrame1 = cam1.getFrame()
        myFrame2 = cam2.getFrame()
        myFrame3 = np.hstack((myFrame1, myFrame2)) 
        frameRGB = cv2.cvtColor(myFrame3, cv2.COLOR_BGR2RGB)
        frameRGBsmall = cv2.resize(frameRGB, (0, 0), fx=scaleFactor, fy=scaleFactor)

        # facePositions = face_recognition.face_locations(frameRGBsmall, model='cnn')
        facePositions = face_recognition.face_locations(frameRGBsmall)
        
        allEncodings = face_recognition.face_encodings(frameRGBsmall, facePositions)
        for (top, right, bottom, left), face_encoding in zip(facePositions, allEncodings):
            name = 'Unkown Person'
            matches = face_recognition.compare_faces(Encodings, face_encoding)
            if True in matches:
                first_match_index = matches.index(True)
                name = Names[first_match_index]
                # print(name)
            top = int(top/scaleFactor)
            right = int(right/scaleFactor)
            bottom = int(bottom/scaleFactor)
            left = int(left/scaleFactor)
            cv2.rectangle(myFrame3, (left, top), (right, bottom), (0, 0, 255), 3)
            cv2.putText(myFrame3, name, (left, top-6), font, .75, (0, 0, 255), 2)
            
        dt = time.time()-startTime
        startTime = time.time()
        dtav = .9*dtav + .1*dt
        fps = 1/dtav
        cv2.rectangle(myFrame3, (0, 0), (100, 40), (0, 0, 255), -1)
        cv2.putText(myFrame3, str(round(fps, 1))+ 'fps', (0, 25), font, .75, (0, 255, 255), 2)
        cv2.imshow('myCam', myFrame3)
        cv2.moveWindow('myCam', 0, 0)
    except:
        print('frame not available')
        # pass
    if cv2.waitKey(1) == ord('q'):
        cam1.capture.release()
        cam2.capture.release()
        cv2.destroyAllWindow()
        exit(1)
        break