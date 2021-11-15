# import the opencv library
import cv2
import numpy as np

filter_image = False

# Colour threshold
green_low_threshold = np.array([50,0,0])  
green_up_threshold = np.array([70,255,255])

img_ori = []
img_rgb = []

# Retrieve capture device (most likely webcam)
vid = cv2.VideoCapture(0)

cv2.namedWindow('SUTS OpenCV')

while(True):    
    # Capture the video frame by frame
    ret, img_ori = vid.read()
    
    img_rgb = cv2.cvtColor(img_ori, cv2.COLOR_BGR2HSV)
    
    if filter_image:
        # Masking / Colour Extraction
        mask = cv2.inRange(img_rgb, green_low_threshold, green_up_threshold)
        
        #find the biggest area of the contour
        contours,hierarchy = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
        c = max(contours, key = cv2.contourArea)
        x,y,w,h = cv2.boundingRect(c)
        
        if(w*h > 900): # minimum of 900 sq px
            # draw the bounding box
            cv2.rectangle(mask,(x,y),(x+w,y+h),(255,255,255),2)
            # draw largest contour
            cv2.drawContours(mask, c, -1, 255, 3)
                    
        cv2.imshow('SUTS OpenCV', mask)    
    else:
        # Display the resulting frame
        cv2.imshow('SUTS OpenCV', img_ori)    
    
    # User input to start , stop the filtering process or quit the program
    user_input = cv2.waitKey(1) & 0xFF
    
    if user_input == ord('e'):
        filter_image = True
    
    if user_input == ord('s'):
        filter_image = False
    
    # 'q' to shutdown program
    if user_input == ord('q'):
        break
  
# Release device
vid.release()
# Destroy all the windows
cv2.destroyAllWindows()