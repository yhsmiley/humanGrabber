xhost +local:docker
docker run -it --gpus all \
	--net=host \
	--ipc host \
	-e DISPLAY=unix$DISPLAY  \
	--privileged \
	-v /dev/:/dev/ \
	-v /media/data/humanGrabber:/humanGrabber \
	human_grabber

	# --user "$(id -u):$(id -g)" \