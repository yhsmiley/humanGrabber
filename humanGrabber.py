import os 
import cv2
import sys
import copy
import time
import GPUtil
import argparse
import itertools
from pathlib import Path
from datetime import datetime

from utils.drawer import Drawer
from utils.misc import chipper, bb_to_xyminmax

from pytorch_YOLOv4.yolo import YOLOV4
from pytorch_YOLOv4.yolo_trt import YOLOV4 as YOLOV4_TRT

from utils.videoGet import VideoStream

parser = argparse.ArgumentParser()
parser.add_argument('--vid_path', help='Video filepaths/streams for \
                    all cameras, e.g.: 0')
parser.add_argument('--gpu_dev', help='Gpu device number to use. Default: 1', type=int, default=None)
parser.add_argument('--od', help='choose object detector to use', default='yolov4', choices=['det2', 'yolov4', 'yolov4_trt'], type=str)
parser.add_argument('--output', help='path of output directory', default='outFrames', type=str)
parser.add_argument('--record',help='Toggle to save original video',action='store_true')
args = parser.parse_args()

video_path = args.vid_path
which_od = args.od
record_tracks = args.record

gpu_device = args.gpu_dev
if gpu_device is None:
    gpus = GPUtil.getAvailable(order='first', maxLoad=1.0, maxMemory=1.0)
    GPU_DEV = gpus[-1]
    print('Setting CUDA_VISIBLE_DEVICES to ', str(GPU_DEV))
    os.environ['CUDA_VISIBLE_DEVICES'] = str(GPU_DEV)
else:
    print('Setting CUDA_VISIBLE_DEVICES to ', str(gpu_device))
    os.environ['CUDA_VISIBLE_DEVICES'] = str(gpu_device)

out_dir = Path(args.output)
Path.mkdir(out_dir, exist_ok=True)
assert Path(out_dir).is_dir(), 'out dir not a dir'

assert video_path is not None, 'video path not specified'
if video_path.isdigit():
    video_path = int(video_path)
    cam_name = 'Webcam{}'.format(video_path)
else:
    cam_name = Path(video_path).stem

print('Video name: {}'.format(cam_name))
print('Video path: {}'.format(video_path))

# check if input video is a videofile
if Path(video_path).is_file():
    videoFile = True
else:
    videoFile = False

if record_tracks:
    stream_fp = str(out_dir)
else:
    stream_fp = None

stream = VideoStream(
            cam_name,
            video_path,
            queueSize=2,
            writeDir=stream_fp,
            reconnectThreshold=1,
            videoFile=videoFile
        )
stream.start()
vidInfo = stream.init_src()
# print(f'vid info: {vidInfo}')

if which_od == 'yolov4':
    objDet = YOLOV4( 
        score=0.5,
        bgr=True,
        model_image_size=(608, 608),
        max_batch_size=4,
        half=True
        )
elif which_od == 'yolov4_trt':
    objDet = YOLOV4_TRT(
        score=0.5,
        bgr=True,
        engine_path='pytorch_YOLOv4/trt_weights/yolov4_1_608_608.trt'
        )

drawer = Drawer()
show_win_name = 'GRAB YOUR HUMAN'
cv2.namedWindow(show_win_name, cv2.WINDOW_NORMAL)

start_whole = time.time()
try:
    for frame_count in itertools.count():
        if stream.stopped:
            break

        frame = stream.read()
        frame_draw = copy.deepcopy(frame)

        dets = objDet.get_detections_dict([frame], classes=['person'])[0]
        # print(dets)
        drawer.draw_bbs(frame_draw, dets)
        cv2.imshow(show_win_name, frame_draw)

        k = cv2.waitKey(1) & 0xFF

        if k == ord('c'):
            print('capture')
            cv2.imwrite(str(out_dir/f'{cam_name}_fr{frame_count}_full.jpg'), frame)
            for i, bb in enumerate(dets):     
                cropped = chipper(frame, bb_to_xyminmax(bb))
                cv2.imwrite(str(out_dir/f'{cam_name}_fr{frame_count}_human{i}.jpg'), cropped)
        elif k == ord('q'):
            break

except KeyboardInterrupt:
    print('Avg FPS:', frame_count/(time.time()-start_whole))
    print('KeyboardInterrupt:')
    print('Killing FrameGrabber..')
    cv2.destroyAllWindows()
    stream.stop()
    time.sleep(0.5)
    sys.exit()

print('Avg FPS:', frame_count/(time.time()-start_whole))
print('Killing FrameGrabber..')
cv2.destroyAllWindows()
stream.stop()
time.sleep(0.5)
sys.exit()
