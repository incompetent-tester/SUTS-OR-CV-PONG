# -*- coding: utf-8 -*-
"""
Created on Wed Nov  3 09:14:09 2021

@author: JHYong
"""

import cv_lib
import random

# Start Computer Vision and retrieve camera source
cv_lib.cv_start()

try:
    # Pong settings
    ball_away = False
    ball_deflected = False
    
    # Pong Ball State
    ball_x = 0
    ball_y = 0
    ball_dir_x = 0
    ball_dir_y = 0
    points = 0
    ball_velocity = 5 # 5 px/frame
            
    # Continously Process Incoming Video and Other Pong Related Actions
    while True:
        # Process Video
        [is_video_processed, deflector_x, deflector_y , processed_video] = cv_lib.cv_process_video()
        
        if(is_video_processed):
            ##########################################################################    
            # FILL IN THE FOLLOWING BLANK PART (......) 
        
            # Pong Physics And Logic
            if(ball_away):
                ##############################
                # Physics                    #
                ##############################
                ### The position of the ball is displacement of x = velocity * ???
                ### The position of the ball is displacement of y = velocity * ???
                ### FILL IN HERE :
                ball_x += ...............
                ball_y += ...............
                
                
                ##############################
                # Logics                     #
                ##############################
                # Pong Bound logic
                x_bounds, y_bounds = cv_lib.cv_get_boundary(processed_video)
                
                
                # Reflect ball
                if(cv_lib.hit_pong_deflector(ball_x, ball_y, deflector_x, deflector_y) and not ball_deflected):
                    ball_dir_y = ......................
                    ball_deflected = True
                
                # If ball touches side, change dir
                if ball_x > x_bounds or ball_x < 0 :
                    ### FILL IN : I would like it to hit the wall and deflect accordingly
                    ball_dir_x = .....................
                
                # If ball touches bottom, end
                if ball_y > y_bounds:
                   ball_away = False 
                   ball_deflected = False
                   ## FILL IN : IF BALL TOUCHES BOTTOM, DEDUCT 1 point
                   points = ......................
               
                # If ball touches top, add point, end
                if ball_y < 0:
                    ball_away = False
                    ball_deflected = False
                    ## IF THE BALL TOUCHES THE TOP, ADD 1 Point
                    ## FILL IN HERE
                    points = ......................
            
                ##########################
                # Graphic                #
                ##########################
                processed_video = cv_lib.pong_draw(processed_video,ball_x,ball_y)
                
                
            # Draw Deflector
            processed_video = cv_lib.pong_deflector(processed_video, deflector_x, deflector_y)
            
            # Draw Points Text
            processed_video = cv_lib.cv_draw_text(processed_video, f'Points : {points}')
            
            ##########################################################################
        
        # Retrieve User Command
        command = cv_lib.pong_keyboard()
        
        # Process User Command
        if command == cv_lib.PongCommand.QUIT:
            break
        elif command == cv_lib.PongCommand.MANUAL_EJECT:
            if not ball_away:
                ball_deflected = False
                ball_away = True
                ball_x = random.randint(0,processed_video.shape[1])
                ball_y = 0
                ball_dir_x = random.uniform(-1,1)
                ball_dir_y = random.uniform(0.5,1)
                ball_velocity = random.randint(5,15)
        
        ##########################################################################
        
        
        # Display Video to screen
        cv_lib.cv_show_video(processed_video)
        
finally:
    # Anything fails - Clean up code    
    cv_lib.cv_cleanup()
    
    

