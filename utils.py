import cv2
import numpy as np
import math

def create_mask(height, width, origin_x, origin_y, mask_height, mask_width, mask_angle):
    mask = np.zeros((height, width), dtype=np.float32)

    #Since the canvas origin is at top left corner, we need to flip the y-axis
    center_x = origin_x
    center_y = -origin_y

    # Convert the angle from degrees to radians
    angle_rad = math.radians(360-mask_angle)  # Convert the angle to radians

    # We create the points of the rectangle by considering the top left corner of rectangel as origin
    pts = np.array([
        [0, -mask_height],
        [mask_width , -mask_height ],
        [mask_width, 0],
        [0 , 0]
    ], dtype=np.float32)
    print(pts)
    # Rotate each corner of the rectangle around the center
    rotated_pts = np.zeros_like(pts)
    for i in range(4):
        x = pts[i, 0] * 1*math.cos(angle_rad) - pts[i, 1] * 1*math.sin(angle_rad)
        y = pts[i, 0] * 1*math.sin(angle_rad) + pts[i, 1] * math.cos(angle_rad)
        print(x,y)
        x = x + center_x
        y = y + center_y
        # if x<0:
        #     x = 0
        y = -y    
            
        rotated_pts[i] = [x , y ]


    print(rotated_pts)
    # Draw a filled polygon (the mask) on the array
    cv2.fillPoly(mask, [rotated_pts.astype(np.int32)], 1)

    return mask