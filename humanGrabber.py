import os 
import cv2
import sys
import copy
import time
import GPUtil
import argparse
import itertools
from pathlib import Path

from drawer_query import Drawer
from misc import chipper, bb_to_xyminmax

from pytorch_YOLOv4.yolo import YOLOV4
from pytorch_YOLOv4.yolo_trt import YOLOV4 as YOLOV4_TRT

parser = argparse.ArgumentParser()
parser.add_argument('--vid_path', help='Video filepaths/streams for \
                    all cameras, e.g.: 0')
parser.add_argument('--gpu_dev', help='Gpu device number to use. Default: 0', type=int, default=None)
parser.add_argument('--od', help='choose object detector to use', default='yolov4', choices=['det2', 'yolov4', 'yolov4_trt'], type=str)
args = parser.parse_args()

video_path = args.vid_path
which_od = args.od

if args.gpu_dev is None:
    gpus = GPUtil.getAvailable(order='first', maxLoad=1.0, maxMemory=1.0)
    GPU_DEV = gpus[0]
    print('Setting CUDA_VISIBLE_DEVICES to ', str(GPU_DEV))
    os.environ['CUDA_VISIBLE_DEVICES'] = str(GPU_DEV)

out_dir = Path('./outFrames')
Path.mkdir(out_dir, exist_ok=True)
assert Path(out_dir).is_dir(), 'out dir not a dir'

if video_path is not None:
    if video_path.isdigit():
        video_path = int(video_path)
        cam_name = 'Webcam{}'.format(video_path)
    else:
        cam_name = os.path.basename(video_path)

print('Video name: {}'.format(cam_name))
print('Video path: {}'.format(video_path))

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
elif which_od == 'det2':
    objDet = Det2(
        bgr=True,
        weights= "f2b/det2/weights/faster-rcnn/faster_rcnn_R_50_FPN_3x/model_final_280758.pkl",
        config= "f2b/det2/configs/COCO-Detection/faster_rcnn_R_50_FPN_3x.yaml",
        classes_path= 'f2b/det2/configs/coco80.names',
        thresh=0.5,
        max_batch_size=4,
        )

drawer = Drawer()
stream = cv2.VideoCapture(video_path)
show_win_name = 'GRAB YOUR HUMAN'
# cv2.namedWindow(show_win_name, cv2.WINDOW_NORMAL)

time.sleep(1.0)
try:
    for frame_count in itertools.count():
        ret, frame = stream.read()
        frame_draw = copy.deepcopy(frame)
        if not ret:
            break

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
    # print('Avg FPS:', frame_count/(time.time()-start_whole))
    print('KeyboardInterrupt:')
    print('Killing FrameGrabber..')
    sys.exit()

cv2.destroyAllWindows()
print('Killing FrameGrabber..')
sys.exit()
