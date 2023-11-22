import jetson.inference
import jetson.utils
import time
import cv2
import numpy as np

width = 1280
height = 720
dispW = width
dispH = height
webcam0 =  f"v4l2src device=/dev/video0 io-mode=2 " \
            f"! image/jpeg, width={dispW}, height={dispH}, framerate=30/1, format=MJPG " \
            f"! nvv4l2decoder mjpeg=1 " \
            f"! nvvidconv " \
            f"! video/x-raw, format=BGRx " \
            f"! videoconvert " \
            f"! video/x-raw, format=BGR " \
            f"! appsink drop=1"
# webcam1 =  f"v4l2src device=/dev/video0 io-mode=2 " \
#             f"! image/jpeg, width={dispW}, height={dispH}, framerate=30/1, format=MJPG " \
#             f"! nvv4l2decoder mjpeg=1 " \
#             f"! nvvidconv " \
#             f"! video/x-raw, format=BGRx " \
#             f"! videoconvert " \
#             f"! video/x-raw, format=BGR " \
#             f"! appsink drop=1"
cam0=cv2.VideoCapture(webcam0, cv2.CAP_GSTREAMER)
# cam1=cv2.VideoCapture(webcam1, cv2.CAP_GSTREAMER)

# cam = jetson.utils.gstCamera(width, height, '/dev/video0')

# display = jetson.utils.glDisplay()
# font = jetson.utils.cudaFont()

net = jetson.inference.imageNet('googlenet')
# net = jetson.inference.imageNet('alexnet')

font = cv2.FONT_HERSHEY_SIMPLEX
timeMark = time.time()
fpsFilter = 0

while True:
    _, frame = cam0.read()
    img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA).astype(np.float32)
    img = jetson.utils.cudaFromNumpy(img)

    # frame, width, height = cam.CaptureRGBA(zeroCopy = 1)
    classID, confidence = net.Classify(img, width, height)
    item = net.GetClassDesc(classID)
    dt = time.time() - timeMark
    fps = 1/dt
    fpsFilter = .95 * fpsFilter + .05 * fps
    timeMark = time.time()
    # font.OverlayText(frame, width, height, str(round(fpsFilter,1)) + ' fps ' + item, 5, 5, font.Magenta, font.Blue)
    # display.RenderOnce(frame, width, height)
    # frame = jetson.utils.cudaToNumpy(frame, width, height, 4)
    # frame = cv2.cvtColor(frame, cv2.COLOR_RGBA2BGR).astype(np.uint8)

    cv2.putText(frame, str(round(fpsFilter, 1)) + ' fps ' + item, (0, 30), font, 1, (0, 0, 255), 2)
    cv2.imshow('recCam', frame)
    cv2.moveWindow('recCam', 0, 0)
    if cv2.waitKey(1) == ord('q'):
        break
cam0.release()
# cam1.release()
cv2.destoryAllWindows()