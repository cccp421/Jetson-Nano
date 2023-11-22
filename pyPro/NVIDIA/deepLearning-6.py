import cv2
import jetson.inference
import jetson.utils
import time
import numpy as np

timeStamp = time.time()
fpsFilt = 0
net = jetson.inference.detectNet('ssd-mobilenet-v2', threshold = .5)
dispW = 1280
dispH = 720
font = cv2.FONT_HERSHEY_SIMPLEX

webcam =  f"v4l2src device=/dev/video0 io-mode=2 " \
            f"! image/jpeg, width={dispW}, height={dispH}, framerate=30/1, format=MJPG " \
            f"! nvv4l2decoder mjpeg=1 " \
            f"! nvvidconv " \
            f"! video/x-raw, format=BGRx " \
            f"! videoconvert " \
            f"! video/x-raw, format=BGR " \
            f"! appsink drop=1"
cam=cv2.VideoCapture(webcam, cv2.CAP_GSTREAMER)

# cam = cv2.VideoCapture('/dev/video0')
# cam.set(cv2.CAP_PROP_FRAME_WIDTH, dispW)
# cam.set(cv2.CAP_PROP_FRAME_HEIGHT, dispH)

# cam=jetson.utils.gstCamera(dispW, dispH,'/dev/video0')
# display = jetson.utils.glDisplay()

while True:
    _, img = cam.read()
    height = img.shape[0]
    width = img.shape[1]
    frame = cv2.cvtColor(img, cv2.COLOR_BGR2RGBA).astype(np.float32)
    frame = jetson.utils.cudaFromNumpy(frame)

    detections = net.Detect(frame, width, height)
    for detect in detections:
        # print(detect)
        ID = detect.ClassID
        top = int(detect.Top)
        left = int(detect.Left)
        bottom = int(detect.Bottom) 
        right = int(detect.Right)
        item = net.GetClassDesc(ID)
        tk = 3
        if item == 'mouse':
            tk = -1
        cv2.rectangle(img, (left, top), (right, bottom), (255, 0, 0), tk)
        cv2.putText(img, item, (left, top+20), font, .75, (255, 255, 0), 2)
    # print(detections)
    # display.RenderOnce(img, width, height)
    dt = time.time() - timeStamp
    timeStamp = time.time() 
    fps = 1 / dt
    fpsFilt =.9*fpsFilt+.1*fps
    # print(str(round(fps, 1))+' fps ')
    cv2.putText(img, str(round(fpsFilt, 1))+" fps ", (0, 30), font, 1, (0, 0, 255), 2)
    cv2.imshow('detCam', img)
    cv2.moveWindow('detCam', 0, 0)
    if cv2.waitKey(1) == ord('q'):
        break
cam.release()
cv2.destoryAllWindows()