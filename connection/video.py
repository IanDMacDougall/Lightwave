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
        self.user_video_queue = queue.Queue(maxsize=20)

        self.sendFrameDuration = 0
        self.receiveFrameDuration = 0

        self.headerClass = header()

        self.sending = True
    


    """
    Records the video data from user and 
    """
    def get_video(self, cameraOn=True):

        while self.sending:

            # retrives image and saves it to frame
            #   if fails retval is false
            retval, frame = self.camera.read()
            
            if not retval:
                print("False")
                raise Exception("Could not retrieve from camera")


            # Adds frame to queue for user playback
            if self.user_video_queue.full():
                while not self.user_video_queue.empty():
                    try:
                        self.user_video_queue.get_nowait()
                    except queue.Empty:
                        break
            else:
                self.user_video_queue.put_nowait(frame)
                self.user_video_queue.put_nowait(frame)



    """
    Uses socket and cv2 to record video data and send it to the client
    """
    def send_video(self, socket, client_address):
        while self.sending:
            try:
                frame = self.user_video_queue.get_nowait()

                sendLastTime = time.time()

                retval, bufferSend = cv2.imencode('.jpg', frame, [cv2.IMWRITE_JPEG_QUALITY, 40] )
                self.headerClass.send_data(socket=socket, addr=client_address, data_type=1, seq_num=0, data_send=pickle.dump(bufferSend), timestamp=int(time.time()))
                
                self.sendFrameDuration = time.time() - sendLastTime()
            except Exception as E:
                print(f"Error in send_video: {E}")
                pass



    """
    Uses socket to receive a frame that will be displayed
    """
    def recieve_video(self, socket):
        while self.sending:
            try:
                recieveLastTime = time.time()

                header.receive_data(socket=socket)
                
                self.receiveFrameDuration = time.time() - recieveLastTime
            except Exception as E:
                print(f"Error in recieve_video: {E}")
                pass


    """
        Displays the frames of the client & the user.

    User:
        User frame is grabbed from same frame being sent to the other user

    Client:
        Client frame is recieved by the heaeder class and being inputed into the video_queue
    """
    def play_video(self):
        while self.sending:
            try:
                if not self.user_video_queue.empty():
                    cv2.imshow("my camera", self.user_video_queue.get_nowait())
                if not self.video_queue.empty():
                    cv2.imshow("Client camera", self.video_queue.get_nowait())
            except queue.Empty:
                pass

            if cv2.waitKey(1) & 0xFF == ord("q"):
                break



    """
    States threads for video
    Sends & Recieves video data
    Once over ends camera
    """
    def network_video(self, socket, client_address):
        self.headerClass.set_video_queue(video_queue=self.video_queue)

        get_thread = threading.Thread(target=self.get_video, args=(), name="getVideoThread")
        play_thread = threading.Thread(target=self.play_video, args=(), name="playVideoThread")
        get_thread.start()
        play_thread.start()


        try:
            get_thread.join()
            play_thread.join()
        except KeyboardInterrupt:
            print("Stopping network audio threads.")
            self.camera.release()
            cv2.destroyAllWindows()
            pass







        






