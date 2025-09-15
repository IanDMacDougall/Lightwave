"""
Project: Lightwave Communications
Authors: Ian MacDougall, Gage Pavia
Date Created: 15 September 2025
Last Modified: 15 September 2025
File Description: Manages video connection aspects.
Repository: https://github.com/IanDMacDougall/lightwave
"""

from .header import header

import cv2
import pickle
import queue
import threading
import numpy as np
import time

class videoConnect:
    def __init__(self, deviceIndex, height, width):
        self.camera = cv2.VideoCapture(deviceIndex)

        self.resolution = [height, width]
        self.camera.set(3, width)
        self.camera.set(4, height)

        self.video_queue = queue.Queue(maxsize=10)
        self.user_video_queue = queue.Queue(maxsize=10)

        self.sendFrameDuration = 0
        self.receiveFrameDuration = 0

        self.headerClass = header()

        self.sending = True
    


    """
    Records the video data from user and 
    """
    def get_video(self, cameraOn=True, sending=True):

        while sending:

            # retrives image and saves it to frame
            #   if fails retval is false
            retval, frame = self.camera.read()
            
            if not retval:
                print("False")
                raise Exception("Could not retrieve from camera")
            else:
                print(self.camera.isOpened())


            # Adds frame to queue for user playback
            if self.user_video_queue.full():
                while not self.user_video_queue.empty():
                    try:
                        self.user_video_queue.get_nowait()
                    except queue.Empty:
                        break
            else:
                self.user_video_queue.put(frame)





    """
    Uses socket and cv2 to record video data and send it to the client
    """
    def send_video(self, socket, client_address):
        send_last_time = time.time()








    """
    Uses socket to receive a frame that will be displayed
    """
    def play_client_video(self, socket, client_address):
        recieve_last_time = time.time()






    """
    Uses socket to receive a frame that will be displayed
    """
    def play_user_video(self):
        while True:
            try:
                cv2.imshow("my camera", self.user_video_queue.get_nowait())
                cv2.waitKey(1)
            except queue.Empty:
                pass














    """
    States threads for video
    Sends & Recieves video data
    Once over ends camera
    """
    def network_video(self, socket, client_address):
        self.headerClass.setVideoQueue(video_queue=self.video_queue)

        get_thread = threading.Thread(target=self.get_video, args=(), name="getVideoThread")
        send_thread = threading.Thread(target=self.send_video, args=(), name="sendVideoThread")
        recieve_thread = threading.Thread(target=self.play_client_video, args=(), name="receiveVideoThread")
        play_thread = threading.Thread(target=self.play_user_video, args=(), name="playVideoThread")

        try:
            get_thread.join()
            send_thread.join()
            recieve_thread.join()
            play_thread.join()
        except KeyboardInterrupt:
            print("Stopping network audio threads.")
            pass







    def test(self):
        
        get = threading.Thread(target=self.get_video, args=(), name="getVideoThread")
        play = threading.Thread(target=self.play_user_video, args=(), name="playVideoThread")
        get.start()
        play.start()

        try:
            get.join()
            play.join()
        except KeyboardInterrupt:
            print("Stopping network audio threads.")
            pass




