import cv2
import math
import numpy as np
from enum import Enum
 
__process_image = False
__debug_image = False

__deflector_half_width = 30
__deflector_half_height = 5

__ball_radius = 10

__green_low_threshold = np.array([50,0,0])  
__green_up_threshold = np.array([70,255,255])

__video_source = None

def __get_orientation(pts):
    sz = len(pts)
    data_pts = np.empty((sz, 2), dtype=np.float64)
    for i in range(data_pts.shape[0]):
        data_pts[i,0] = pts[i,0,0]
        data_pts[i,1] = pts[i,0,1]
    # Perform PCA analysis
    mean = np.empty((0))
    mean, eigenvectors, eigenvalues = cv2.PCACompute2(data_pts, mean)
    angle = math.atan2(eigenvectors[0,1], eigenvectors[0,0]) # orientation in radians
    return angle * 180 / math.pi


def cv_start():
    # Retrieve capture device (most likely webcam)
    global __video_source
    __video_source = cv2.VideoCapture(0)
    
def cv_draw_text(img,text):
    font                   = cv2.FONT_HERSHEY_SIMPLEX
    bottomLeftCornerOfText = (10,475)
    fontScale              = 0.5
    fontColor              = (255,255,255)
    lineType               = 1
    
    cv2.putText(img,text, 
        bottomLeftCornerOfText, 
        font, 
        fontScale,
        fontColor,
        lineType)

    return img

def cv_process_video():
    # Capture the video frame by frame
    global __video_source
    ret, img_ori = __video_source.read()
    
    img_rgb = cv2.cvtColor(img_ori, cv2.COLOR_BGR2HSV)
    img_blank = np.zeros(img_rgb.shape, dtype=np.uint8)
    
    if __process_image:
        mask = cv2.inRange(img_rgb, __green_low_threshold, __green_up_threshold)
        
        # Blob detection
        contours,hierarchy = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
        
        cX = 0
        cY = 0

        if len(contours) != 0:
            #find the biggest area of the contour
            c = max(contours, key = cv2.contourArea)
            x,y,w,h = cv2.boundingRect(c)
            
            if(w*h > 900): # minimum of 900 sq px
                if(__debug_image):  
                    # draw the bounding box
                    cv2.rectangle(img_blank,(x,y),(x+w,y+h),(255,255,255),2)
                    # draw largest contour
                    cv2.drawContours(img_blank, c, -1, 255, 3)
                
               	# compute the center of the contour
               	M = cv2.moments(c)
               	cX = int(M["m10"] / M["m00"])
               	cY = int(M["m01"] / M["m00"])
                
        if(__debug_image):
            img_blank = cv2.addWeighted(img_rgb, 0.3, img_blank, 0.7,0)
              
        
        return [True,cX,cY,img_blank]
    else:
        return [False,0,0,img_ori]

def cv_show_video(vid):
    cv2.namedWindow('Application')
    cv2.imshow('Application', vid) 

def cv_cleanup():
    global __video_source
    # Release device
    if __video_source:
        __video_source.release()
    # Destroy all the windows
    cv2.destroyAllWindows()
    
def cv_get_boundary(img):
    shape = img.shape
    return shape[1], shape[0]

#############################################################################

class PongCommand(Enum):
    MANUAL_EJECT = 1
    AUTO_EJECT = 2
    QUIT = 3
    NOTHING = 4

def pong_draw(vid, ball_x, ball_y):
    # Blue (BGR)
    color = (255, 0, 0)
    vid = cv2.circle(vid, (int(ball_x), int(ball_y)), __ball_radius, color, -1)
    return vid

def pong_deflector(vid, deflector_x, deflector_y):
    vid = cv2.rectangle(vid,
                        (deflector_x-__deflector_half_width,deflector_y-__deflector_half_height),
                        (deflector_x+__deflector_half_width,deflector_y+__deflector_half_height),
                        (255,255,255),-1)
    return vid

def hit_pong_deflector(ball_x,ball_y,deflector_x,deflector_y):
    # Primitive bound detection
    hit_y = ball_y + __ball_radius > deflector_y - __deflector_half_height \
        and  ball_y + __ball_radius < deflector_y + __deflector_half_height 
    hit_x = ball_x > deflector_x - __deflector_half_width \
        and ball_x < deflector_x + __deflector_half_width
    return hit_y and hit_x
    

def pong_keyboard():
    global __process_image
    global __debug_image
    
    user_input =  cv2.waitKey(1) & 0xFF
    
    # Space bar to manual eject
    if user_input == 32:
        return PongCommand.MANUAL_EJECT

    
    if user_input == ord('d'):
        __process_image  = True
        __debug_image = True
    
    if user_input == ord('e'):
        __process_image  = True

    
    if user_input == ord('s'):
        __process_image  = False
        __debug_image = False
    
    # 'q' to shutdown program
    if user_input == ord('q'):
        return PongCommand.QUIT
    
    return PongCommand.NOTHING

