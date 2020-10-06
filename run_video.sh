# vid_path=testvideo.mp4
vid_path=rtsp://wowzaec2demo.streamlock.net/vod/mp4:BigBuckBunny_115k.mov
gpu_dev=0
od=yolov4_trt
output=outFrames
# record=True # comment out for no recording

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

if [ ${record+x} ]
then
	py_cmd+=" --record"
fi

eval $py_cmd
