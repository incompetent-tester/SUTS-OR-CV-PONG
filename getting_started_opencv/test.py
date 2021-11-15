# import the opencv library
import cv2
  
# Retrieve capture device (most likely webcam)
vid = cv2.VideoCapture(0)
  
while(True):    
    # Capture the video frame by frame
    ret, frame = vid.read()
    # Display the resulting frame
    cv2.imshow('Application', frame)
    # 'q' to shutdown program
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
  
# Release device
vid.release()
# Destroy all the windows
cv2.destroyAllWindows()