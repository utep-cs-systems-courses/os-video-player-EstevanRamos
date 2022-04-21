#!/usr/bin/env python3
import cv2 as cv
import threading
from BBQ import BBQ


def produce_frames(producer: BBQ):
    video_path= 'clip.mp4'
    
    #open video
    cap = cv.VideoCapture(video_path)
    
    #while video is open
    while cap.isOpened():
        #read frame
        ret , frame = cap.read()
        
        print('enqueue frame...')
        #enqueue frame
        producer.enqueue(frame)
    #end of video    
    producer.enqueue('END')
        
    
def grayscale_frames(producer: BBQ, consumer: BBQ):
    #convert frame and send to displayer thread
    while True:
        #get frame from producer
        frame = producer.dequeue()
        
        if frame == 'END':
            break
        
        #convert frame to grayscale
        gray_frame = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
        
        #enqueue gray frames
        print('enqueue gray frames...')
        consumer.enqueue(gray_frame)
    
    #end of gray frames
    consumer.enqueue('END')

def display_frames(consumer: BBQ):
    frame_delay = 42
    #starts displaying frames
    while True:
        
        #get frame
        frame = consumer.dequeue()
        print('consuming frame...')
        
        if frame == 'END':
            break
    
        #show image
        cv.imshow('grayscale' , frame)
        if cv.waitKey(frame_delay) & 0xFF == ord('q'):
            break
        
    cv.destroyAllWindows()


if __name__ == '__main__':
    #create Qs
    producer = BBQ()
    consumer = BBQ()
    
    print('Qs created')
    
    # Create threads that will extract frames, convert the frames, and display the frame
    producer_thread = threading.Thread(target=produce_frames, args=(producer,))
    grayscale_thread = threading.Thread(target=grayscale_frames, args=(producer, consumer))
    consumer_thread = threading.Thread(target=display_frames, args=(consumer,))
    
    print('threads created')

    # Start executing all threads
    producer_thread.start()
    grayscale_thread.start()
    consumer_thread.start()
    