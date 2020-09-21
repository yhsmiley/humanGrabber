import cv2

class Drawer(object):
    def __init__(self, color=(255,0,0), font=cv2.FONT_HERSHEY_DUPLEX):
        self.color = color
        self.font = font
        self.fontScale = 0.7
        self.fontThickness = 2
        
    def draw_bbs(self, frame, bbs):
        if bbs is None or len(bbs) == 0:
            return

        for bb in bbs:
            l = int(bb['l'])
            t = int(bb['t'])
            r = int(bb['r'])
            b = int(bb['b'])
            text = str('{:.4}'.format(bb['confidence']))

            cv2.rectangle(frame, (l,t), (r,b), self.color, 3)
            cv2.putText(frame, 
                        text, 
                        (l+5, b-10),
                        self.font, self.fontScale, self.color, self.fontThickness)
