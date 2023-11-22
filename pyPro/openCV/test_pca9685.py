import time  #引入time库
from adafruit_servokit import ServoKit  #引入PCA9685库

kit = ServoKit(channels=16)  #明确PCA9685的舵机控制数
kit.servo[0].angle = 75  #channel0上的舵机旋转。
time.sleep(1)  #休眠一秒
kit.servo[0].angle = 150  #channel0上的舵机旋转。

