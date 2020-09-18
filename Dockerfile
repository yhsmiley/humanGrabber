# docker build -t human_grabber .

FROM nvcr.io/nvidia/cuda:10.2-cudnn8-devel-ubuntu18.04

ENV cwd="/home/"
WORKDIR $cwd

RUN apt-get -y update
# RUN apt-get -y upgrade

RUN apt-get install -y \
    software-properties-common \
    build-essential \
    checkinstall \
    cmake \
    pkg-config \
    yasm \
    git \
    vim \
    curl \
    wget \
    gfortran \
    libjpeg8-dev \
    libpng-dev \
    libtiff5-dev \
    libtiff-dev \
    libavcodec-dev \
    libavformat-dev \
    libswscale-dev \
    libdc1394-22-dev \
    libxine2-dev \
    sudo \
    apt-transport-https \
    libcanberra-gtk-module \
    libcanberra-gtk3-module \
    dbus-x11 \
    vlc \
    iputils-ping \
    python3-dev \
    python3-pip

# RUN apt-get install -y ffmpeg

RUN DEBIAN_FRONTEND=noninteractive apt-get install -y tzdata python3-tk
RUN apt-get clean && rm -rf /tmp/* /var/tmp/* /var/lib/apt/lists/* && apt-get -y autoremove

# INSTALL SUBLIME TEXT
RUN apt install -y ca-certificates
RUN curl -fsSL https://download.sublimetext.com/sublimehq-pub.gpg | apt-key add - && add-apt-repository "deb https://download.sublimetext.com/ apt/stable/"
RUN apt update && apt install -y sublime-text

RUN rm -rf /var/cache/apt/archives/

### APT END ###

ENV TZ=Asia/Singapore
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

RUN pip3 install --no-cache-dir --upgrade pip

COPY requirements.txt requirements.txt
RUN pip3 install --no-cache-dir --use-feature=2020-resolver -r requirements.txt

# INSTALL TENSORRT (download the trt deb first)
ARG TENSORRT=nv-tensorrt-repo-ubuntu1804-cuda10.2-trt7.0.0.11-ga-20191216_1-1_amd64.deb
COPY pytorch_YOLOv4/nv-tensorrt-repo-ubuntu1804-cuda10.2-trt7.0.0.11-ga-20191216_1-1_amd64.deb /tmp/$TENSORRT
# From Tensort installation instructions
ARG TENSORRT_KEY=/var/nv-tensorrt-repo-cuda10.2-trt7.0.0.11-ga-20191216/7fa2af80.pub
# Rename the ML repo to something else so apt doesn't see it
RUN mv /etc/apt/sources.list.d/nvidia-ml.list /etc/apt/sources.list.d/nvidia-ml.list.bkp && \
    dpkg -i /tmp/$TENSORRT && \
    apt-key add $TENSORRT_KEY && \
    apt-get update && \
    apt-get install -y tensorrt
RUN apt-get install -y python3-libnvinfer-dev uff-converter-tf

WORKDIR /humanGrabber
