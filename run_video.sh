vid_path=testvideo.mp4
gpu_dev=0
od=yolov4_trt
output=outFrames

py_cmd="python3 humanGrabber.py --vid_path ${vid_path}"

if [ ${gpu_dev+x} ]
then
	py_cmd+=" --gpu_dev ${gpu_dev}"
fi

if [ ${od+x} ]
then
	py_cmd+=" --od ${od}"
fi

if [ ${output+x} ]
then
	py_cmd+=" --output ${output}"
fi

eval $py_cmd
