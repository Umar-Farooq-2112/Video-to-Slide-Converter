import cv2 as cv
import os
import numpy as np
import time
import csv

def writeSlide(frame,count,result_directory):
    output_path = os.path.join(result_directory, f"{count}.jpg")
    cv.imwrite(output_path, frame)

def slideReader(videopath, result_directory="Output",starting_time=0,end_time=0,up=0,down=0,left=0,right=0):
    frame_count = 1
    prev_gray_frame = None
    slide_detected = False
    capture_time=0
    
    
    if not os.path.exists(result_directory):
        os.makedirs(result_directory)
    
    capture = cv.VideoCapture(videopath)
    if not capture.isOpened():
        print("Error: Unable to open video")
        return
    
    strt = time.time()
    while capture_time < starting_time:
        capture.read()
        capture_time += 1 / capture.get(cv.CAP_PROP_FPS)
    
    
    strt = time.time()
    status, curr = capture.read()
    width = curr.shape[1]
    height= curr.shape[0]
    if status:
        curr = curr[int(up*height):height-int(down*height),int(width*left):width-int(width*right)]    
        writeSlide(curr,frame_count,result_directory)
        prev_gray_frame = cv.cvtColor(curr, cv.COLOR_BGR2GRAY)       
        frame_count+=1
        capture_time += 1 / capture.get(cv.CAP_PROP_FPS)

    threshold = 100

    strt = time.time()
    
    
    while end_time == 0 or capture_time<end_time:
        
        status, curr = capture.read()
        
        if not status:
            break
        
        curr = curr[int(up*height):height-int(down*height),int(width*left):width-int(width*right)]    
        cur_gray_frame = cv.cvtColor(curr, cv.COLOR_BGR2GRAY)
        frame_diff = cv.absdiff(cur_gray_frame, prev_gray_frame)
        changed_pixels = np.count_nonzero(frame_diff > threshold)
        
        if changed_pixels > 10000:
            if not slide_detected:  
                slide_detected = True
                start_time = time.time()
        elif slide_detected:  
            if time.time() - start_time > 1:
                writeSlide(curr,frame_count,result_directory)
                frame_count+=1
                slide_detected = False 
                strt = time.time()
                
        prev_gray_frame = cur_gray_frame.copy()
        capture_time += 1 / capture.get(cv.CAP_PROP_FPS)
    
    capture.release()
    cv.destroyAllWindows()

