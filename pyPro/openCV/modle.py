import cv2
print(cv2.__version__)
dispW=640
dispH=480
flip=2
#Uncomment These next Two Line for Pi Camera
#camSet='nvarguscamerasrc !  video/x-raw(memory:NVMM), width=3264, height=2464, format=NV12, framerate=21/1 ! nvvidconv flip-method='+str(flip)+' ! video/x-raw, width='+str(dispW)+', height='+str(dispH)+', format=BGRx ! videoconvert ! video/x-raw, format=BGR ! appsink'
#cam= cv2.VideoCapture(camSet)
 
#Or, if you have a WEB cam, uncomment the next line
#(If it does not work, try setting to '1' instead of '0')
webcam =  f"v4l2src device=/dev/video0 io-mode=2 " \
            f"! image/jpeg, width={dispW}, height={dispH}, framerate=30/1, format=MJPG " \
            f"! nvv4l2decoder mjpeg=1 " \
            f"! nvvidconv " \
            f"! video/x-raw, format=BGRx " \
            f"! videoconvert " \
            f"! video/x-raw, format=BGR " \
            f"! appsink drop=1"
cam=cv2.VideoCapture(webcam, cv2.CAP_GSTREAMER)
cam.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cam.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
while True:
    ret, frame = cam.read()
    cv2.imshow('cam',frame)
    cv2.moveWindow('cam', 0, 0)
    if cv2.waitKey(1)==ord('q'):
        break
cam.release()
cv2.destroyAllWindows()