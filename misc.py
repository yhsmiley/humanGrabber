import cv2


def wrap_in(frame, bb):
    min_x, min_y, max_x, max_y = bb
    bound_y, bound_x = frame.shape[:2]
    
    min_x = max(0, min_x)
    max_x = max(0, max_x)
    min_x = min(bound_x, min_x)
    max_x = min(bound_x, max_x)
    
    min_y = max(0, min_y)
    max_y = max(0, max_y)
    min_y = min(bound_y, min_y)
    max_y = min(bound_y, max_y)
    
    width = max_x - min_x
    height= max_y - min_y

    if width == 0 or height == 0:
        return None
    else:
        return [min_x, min_y, max_x, max_y]

def chipper(frame, bb, intended_height=None):
    bb = wrap_in(frame, bb)
    if bb is None or bb == []:
        return None
    min_x, min_y, max_x, max_y = bb
    cropped = frame[ min_y:max_y, min_x:max_x]
    if intended_height is not None:
        height, width = cropped.shape[:2]
        ratio = height / float(width)
        intended_width = intended_height / float(ratio)
        cropped = cv2.resize(cropped, (int(intended_width), int(intended_height)))
    return cropped

def bb_to_xyminmax(bb):
    xmin = bb['l']
    ymin = bb['t']
    xmax = bb['r']
    ymax = bb['b']
    return (xmin, ymin, xmax, ymax)
