xhost +local:docker
docker run -it --gpus all \
	--net=host \
	--ipc host \
	-e DISPLAY=unix$DISPLAY  \
	--privileged \
	-v /dev/:/dev/ \
	-v /media/data/humanGrabber:/humanGrabber \
	--user "$(id -u):$(id -g)" \
	human_grabber
