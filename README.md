# 一个jetson nano的学习笔记

# jetpack4.6.1、python3.6、cuda10.2
pyPro文件夹是用于Nano学习时，所使用的python文件，包含NVIDIA官方提供的“Hello AI world” Demo用的跑deep learning的例程、Open CV的例程（haarcascade人脸检测等） 
https://github.com/dusty-nv/jetson-inference#training

新手教程是我跟着YouTube上@paulmcwhorter老爷子一步步练习的，教的很好，只有一个问题就是视频出的较早，jetson版本跟现在不一致，中途会出现很多因为版本而导致的问题，尤其是调用控制舵机模块库的时候，很麻烦，但也能解决

# 部署Yolo v5-7.0
installation package for Jetson Nano

建议先换个国内的镜像源

部署的是官方提供的v7版本
 https://github.com/ultralytics/yolov5 

安装环境torch1.10.0 and torchvision0.11.1
安装的torch包一定要是英伟达jetson官网提供的_aarch66.whl安装包！！！

提供一个torch历史版本下载的网址：https://download.pytorch.org/whl/torch_stable.html （其中torch安装包.whl的名字cu117表示cuda版本、cp38表示python3.8）

torchvision对应torch版本的包下载就行
https://forums.developer.nvidia.com/t/pytorch-for-jetson/72048

其他包按照文件中提供的requirements.txt文件安装就行.

--source 0使用摄像头，跑推理detect.py文件时，遇到OpenCV相关的错误，需安装opencv-contrib-python（一个opencv的拓展库），其版本要跟opencv-python的版本一致，安装过程很慢！！

# 使用TensorRT进行推理加速
有两个方法：1.使用英伟达官方的tensorrt https://github.com/NVIDIA/TensorRT

参考CSDN一篇帖子 https://blog.csdn.net/weixin_46007139/article/details/129597153?ops_request_misc=&request_id=&biz_id=102&utm_term=jetson%20nano%20yolov5%20%20&utm_medium=distribute.pc_search_result.none-task-blog-2~all~sobaiduweb~default-1-129597153.142^v96^pc_search_result_base7&spm=1018.2226.3001.4187 

yolov5主目录里有export.py，可以直接调用tensorRT包实现把模型从xx.pt到xx.engine的转换，非常方便，不需要其他操作。并且jetson nano有自带的tensorRT包，只需要和conda环境里的包的安装目录建立软连接即可。
    
    然后安装ONNX：先安装onnx的环境依赖
    sudo apt-get install protobuf-compiler libprotoc-dev
    
    再安装onnx为1.9.0的版本
    pip install onnx==1.9.0

    安装好依赖后，即可运行export.py文件，将自己训练好的权重文件.pt转换成.engine文件，
    python export.py --weights yolov5s.pt --include engine --device 0 

    再用.engine文件作为权重文件进行推理即可

2.使用第三方大佬的tensorrtx https://github.com/wang-xinyu/tensorrtx 

先将.pt权重文件转换成.wts文件,然后再转换成.engine文件。由于这种方法生成的.engine文件不能直接用在官方文档下yolov5中的detect.py文件，必须使用他自己tensorrtx中的yolov5_det.py文件，并且该文件只能推理图片，想实时推理摄像头，还要改对应的c++文件，而且网上教程目前还没有yolov5_7.0版本的修改教程，所以就没有使用这种方法
