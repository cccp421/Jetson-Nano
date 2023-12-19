一个jetson nano的学习笔记

# jetpack4.6.1、python3.6、cuda10.2
pyPro文件夹是用于Nano学习时，所使用的python文件，包含NVIDIA官方提供的“Hello AI world” Demo用的跑deep learning的例程、Open CV的例程（haarcascade人脸检测等） 
https://github.com/dusty-nv/jetson-inference#training


# Yolo v5-7.0
installation package for Jetson Nano

https://github.com/ultralytics/yolov5 
部署的是官方提供的v7版本

安装环境torch1.10.0 and torchvision0.11.1
安装的torch包一定要是英伟达jetson官网提供的_aarch66.whl安装包！！！

torchvision对应torch版本的包下载就行
https://forums.developer.nvidia.com/t/pytorch-for-jetson/72048

其他包按照文件中提供的requirements.txt文件安装就行.

--source 0使用摄像头，跑推理detect.py文件时，遇到OpenCV相关的错误，需安装opencv-contrib-python（一个opencv的拓展库），其版本要跟opencv-python的版本一致，安装过程很慢！！
