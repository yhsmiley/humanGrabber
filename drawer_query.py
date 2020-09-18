# from dlib import mmod_rectangle
import cv2
# import numpy as np
# import copy
# import dlib

class Drawer(object):
    def __init__(self, color = (255,0,0), ided_color = (0,0,255), font=cv2.FONT_HERSHEY_DUPLEX):
        self.color = color
        self.ided_color = ided_color
        self.font = font
        self.fontScale = 0.7
        self.fontThickness = 2
        self.frameHeight = None
        self.imageMode = False
        
    # def _resize(self, frame):
    #     height, width = frame.shape[:2]
    #     if height != self.frameHeight:
    #         scale = float(height) / self.frameHeight
    #         frame = cv2.resize(frame, (int(width / scale), int(self.frameHeight) ) )
    #     return frame
        # if self.firstHeight is None:
        #     self.firstHeight = float(height)
        #     print('first frame'+str(frame.shape))
        #     return frame
        # elif height == self.firstHeight:
        #     print('second but same height'+str(frame.shape))
        #     return frame
        # else:
        #     scale = height / self.firstHeight
        #     frame = cv2.resize(frame, (int(width / scale), int(self.firstHeight) ) )
        #     print('second resized'+str(frame.shape))
        #     return frame


    def draw_bbs(self, frame, bbs):
        if bbs is None or len(bbs) == 0:
            return
        for bb in bbs:
            l = int(bb['l'])
            t = int(bb['t'])
            r = int(bb['r'])
            b = int(bb['b'])
            text = str('{:.4}'.format(bb['confidence']))
            # l = int(bb['topleft']['x'])
            # t = int(bb['topleft']['y'])
            # r = int(bb['bottomright']['x'])
            # b = int(bb['bottomright']['y'])
            # text = str('{:.4}'.format(bb['confidence']))

            # cv2.rectangle(frameDC, (l, t), (r, b), self.color, 3)
            cv2.rectangle(frame, (l,t), (r,b), self.color, 3)
            cv2.putText(frame, 
                        text, 
                        (l+5, b-10),
                        self.font, self.fontScale, self.color, self.fontThickness)


    # def draw_bbs_haar(self, frame, bbs):
    #     if bbs is None or len(bbs) == 0:
    #         return frame
    #     assert isinstance(bbs[0],np.ndarray),'input bb is not a np.ndarray!'
    #     frameDC = copy.deepcopy(frame)
    #     for bb in bbs:
    #         x,y,w,h = bb
    #         l = x
    #         r = x + w
    #         t = y
    #         b = y + h
    #         # l,t,r,b = bb.left(), bb.top(), bb.right(), bb.bottom()
    #         # text = str(track.track_id)
    #         text = ''
    #         # text = str('{:.4}'.format(bb.confidence))
    #         # cv2.rectangle(frameDC, (l, t), (r, b), self.color, 3)
    #         cv2.rectangle(frameDC, (l, t), (r, b), (0,0,255), 3)
    #         cv2.putText(frameDC, 
    #                     text, 
    #                     (l+5, b-10),
    #                     self.font, self.fontScale, self.color, self.fontThickness)
    #     return frameDC

    # def draw_bbs_rect(self, frame, bbs_rects):
    #     if bbs_rects is None or len(bbs_rects) == 0:
    #         return frame
    #     assert isinstance(bbs_rects[0],dlib.rectangle),'input bb is not a dlib.rectangle object!'
    #     frameDC = copy.deepcopy(frame)
    #     for bb in bbs_rects:
    #         l,t,r,b = bb.left(), bb.top(), bb.right(), bb.bottom()
    #         # text = str(track.track_id)
    #         text = ''
    #         # text = str('{:.4}'.format(bb.confidence))
    #         cv2.rectangle(frameDC, (l, t), (r, b), self.color, 3)
    #         cv2.putText(frameDC, 
    #                     text, 
    #                     (l+5, b-10),
    #                     self.font, self.fontScale, self.color, self.fontThickness)
    #     return frameDC

    # def draw_bbs_mmod(self, frame, bbs):
    #     if bbs is None or len(bbs)==0:
    #         return frame
    #     frameDC = copy.deepcopy(frame)
    #     for bb in bbs:
    #         l,t,r,b = bb.rect.left(), bb.rect.top(), bb.rect.right(), bb.rect.bottom()
    #         # text = str(track.track_id)
    #         text = str('{:.4}'.format(bb.confidence))
    #         cv2.rectangle(frameDC, (l, t), (r, b), self.color, 3)
    #         cv2.putText(frameDC, 
    #                     text, 
    #                     (l+5, b-10),
    #                     self.font, self.fontScale, self.color, self.fontThickness)
    #     return frameDC

    # def draw_landmarks(self, frame, landmarks): #TODO CHANGE ACCORDINGLY
    #     if landmarks is None:
    #         return frame
    #     frameDC = copy.deepcopy(frame)
    #     for landmark in landmarks:
    #         text = ''
    #         cv2.circle(frameDC, landmark, 2, self.color, -1)
    #         # cv2.putText(frameDC, 
    #         #             text, 
    #         #             (l+5, b-10),
    #         #             self.font, self.fontScale, self.color, self.fontThickness)
    #     return frameDC


    # def draw_pred(self, frame, preds, bbs):
    #     if bbs is None or preds is None:
    #         return frame
    #     for i, bb in enumerate(bbs):
    #         l,t,r,b = [bb['rect'][x] for x in 'ltrb']
    #         # text = str(track.track_id)
    #         index,_ = preds[i]
    #         # suspect1 = pred[0]
    #         text = str(index)
    #         # text = str('{}:{:.2}'.format(suspect1[0], suspect1[1]))
    #         cv2.rectangle(frame, (l, t), (r, b), self.ided_color, 3)
    #         cv2.putText(frame, 
    #                     text, 
    #                     (l+5, b+20),
    #                     self.font, self.fontScale, self.ided_color, self.fontThickness)
    #     return frame

    # def _draw_track(self, frame, track):
    #     l,t,r,b = [int(x) for x in track.to_tlbr()]
    #     text = str(track.track_id)
    #     # cv2.rectangle(frame, (l, t), (r, b), self.color, 3)
    #     cv2.putText(frame, 
    #                 text, 
    #                 (l+5, b-10),
    #                 self.font, 1.5, self.color, 3)
    #     return frame

    # def draw_tracks(self, frame, tracks):
    #     for track in tracks:
    #         if not track.is_confirmed() or track.time_since_update > 1:
    #             continue
    #         frame = self._draw_track(frame, track)
    #     return frame

    # def draw_people(self, frame, people):
    #     for person in people.values():
    #         if person is None or not person['present']:
    #             continue
    #         l, t, r, b = [int(x) for x in person['latest_bb']]
    #         id_ = person['identity']
    #         if id_ is not None and id_ != 'Unknown':
    #             color = self.ided_color
    #             text = str('{}'.format(id_))
    #         else:
    #             color = self.color
    #             text = ''
    #         cv2.rectangle(frame, (l,t),(r,b), color, 3)
    #         cv2.putText(frame, text, (l+5, b+20),
    #                     self.font, self.fontScale, color, self.fontThickness)
    #     return frame

    # def draw_people_topK(self, frame, people, show_thres, topK):
    #     for person in people.values():
    #         if person is None or not person['present']:
    #             continue
    #         l, t, r, b = [int(x) for x in person['latest_bb']]
    #         if isinstance(person['top_ids'],list):
    #             ids = person['top_ids'][:topK]
    #             nextline = 0
    #             for id_ in ids:
    #                 if id_ is not None:
    #                     color = self.ided_color
    #                     # if topK == 1:
    #                     #    text = str('{}'.format(id_[0]))
    #                     # else:
    #                     text = ''
    #                     if id_[1] > show_thres:
    #                        # text = str('{}:{:.1f}'.format(id_[0],id_[1]))
    #                        text = str('{}:{:.4f}'.format(id_[0],id_[1]))
    #                     cv2.putText(frame, text, (l+5, b+20+nextline),
    #                     self.font, self.fontScale, color, self.fontThickness)
    #                     nextline += 20
    #                 # if id_ is not None and id_ != 'Unknown':
    #                 #     color = self.ided_color
    #                 #     text = str('{}'.format(id_))
    #         else:
    #             color = self.color
    #             text = ''
    #             # if person['top_ids'] is None:
    #             #     print('topids is none')
    #         cv2.rectangle(frame, (l,t),(r,b), color, 3)
    #         # cv2.putText(frame, text, (l+5, b+20),
    #         #             self.font, self.fontScale, color, self.fontThickness)
    #     return frame

    # def draw_people_batch(self, frames, status, all_people, show_thres=0.0, topK = 1):
    #     big_frame = None
    #     # for frame in frames:
    #     #     print(frame.shape)
    #     frames_dc = copy.deepcopy(frames)
    #     for i, frame in enumerate(frames_dc):
    #         if frame is None:
    #             continue
    #         # checks if this frame is real or blank, if blank, take the oldFrame
    #         if status[i]:
    #             # if topK is None:
    #             #     frame = self.draw_people(frame, all_people[i])
    #             frame = self.draw_people_topK(frame, all_people[i], show_thres, topK)
    #             self.oldFrames[i] = frame
    #         else:
    #             oldFrame = self.oldFrames[i]
    #             if oldFrame is not None:
    #                 frame = oldFrame
    #         if big_frame is None:
    #             # frame = self._resize(frame)
    #             big_frame = frame
    #         else:
    #             frame = self._resize(frame)
    #             big_frame = np.hstack((big_frame, frame))
    #     return big_frame