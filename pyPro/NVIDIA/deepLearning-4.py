import cv2
import jetson.inference
import jetson.utils
import time

timeStamp = time.time()
fpsFilt = 0

dispW = 1280
dispH = 720

cam=jetson.utils.gstCamera(dispW, dispH,'/dev/video0')
# webcam0 =  f"v4l2src device=/dev/video0 io-mode=2 " \
#             f"! image/jpeg, width={dispW}, height={dispH}, framerate=30/1, format=MJPG " \
#             f"! nvv4l2decoder mjpeg=1 " \
#             f"! nvvidconv " \
#             f"! video/x-raw, format=BGRx " \
#             f"! videoconvert " \
#             f"! video/x-raw, format=BGR " \
#             f"! appsink drop=1"
# cam=cv2.VideoCapture(webcam0, cv2.CAP_GSTREAMER)
display = jetson.utils.glDisplay()
net = jetson.inference.detectNet('ssd-mobilenet-v2', threshold = .5)

while display.IsOpen():
    img, width, height = cam.CaptureRGBA()
    detections = net.Detect(img, width, height)
    display.RenderOnce(img, width, height)
    dt = time.time() - timeStamp
    timeStamp = time.time() 
    fps = 1 / dt
    fpsFilt =.9*fpsFilt+.1*fps
    print(str(round(fps, 1))+' fps ')