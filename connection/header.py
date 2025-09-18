"""
Project: Lightwave Communications
Authors: Ian MacDougall, Gage Pavia
Date Created: 15 September 2025
Last Modified: 15 September 2025
File Description: Manages video connection aspects.
Repository: https://github.com/IanDMacDougall/lightwave
"""

import struct
import pickle
import cv2
import numpy as np
import time

class header:
    def __init__(self):    
        # variables
        self.width = 640
        self.height = 480

        # Header structure: [data type (1 byte) | length (4 bytes) | timestamp (8 bytes)]
        # Using struct format: B = unsigned char, I = unsigned int, Q = unsigned long long
        self.HEADER_FORMAT = 'B I I Q'  
        self.header_size = struct.calcsize( self.HEADER_FORMAT )

        # Types of data being sent & recieved
        self.AUDIO_TYPE = 0
        self.VIDEO_TYPE = 1
        self.CHAT_TYPE = 2

        self.audio_queue = None
        self.video_queue = None
        self.chat_queue = None



    """
    constructs header with the type of data being sent, sequence number, data length, and timestamp
    """
    def create_header( self, data_type, seq_num, data_length, timestamp ):
        return struct.pack( self.HEADER_FORMAT, data_type, seq_num, data_length, timestamp )


    """
    makes data header and connects data to header 
    Then sends this completed data to the given address ( addr ) through socket
    """    
    def send_data( self, socket, addr, data_type, seq_num, data_send, timestamp ):
        header = self.create_header(data_type, seq_num, len(data_send), timestamp)
        messsage = header + data_send
        socket.sendto(messsage, addr)


    """
    takes user's socket and receives data ( max UDP from socket due to audio and video being large sets of data )
    depending on the data, it is process and this processed data is played or displayed for the user
    """    
    def receive_data(self, socket):
        data_receive, addr = socket.recvfrom( 65527 )   # receives video
        header_data = data_receive[ :self.header_size ]       # takes header
        data_payload = data_receive[ self.header_size: ]      # 

        data_type, seq_num, data_len, timestamp = struct.unpack( self.HEADER_FORMAT, header_data )

        data_lenCheck = len( data_payload )
        self.packetLossPercent = ( ( data_len - data_lenCheck ) / data_lenCheck ) * 100

        # data for audio
        if data_type == self.AUDIO_TYPE:   
            self.audio_latency = time.time() - timestamp 
            if( self.audio_queue != None ):
                self.audio_queue.put( np.frombuffer( data_payload, dtype=np.float32 ) )

        # data for video
        elif data_type == self.VIDEO_TYPE:   
            self.video_latency = time.time() - timestamp
            if( self.video_queue != None ):
                try:
                    while self.video_queue.full():
                        self.video_queue.get_nowait()
                    self.video_queue.put( cv2.resize( cv2.imdecode( pickle.loads( data_payload ), cv2.IMREAD_COLOR ), ( self.width, self.height ) ) )
                except Exception as E:
                    print( " ", E )
            
        
        # data for chat
        elif data_type == self.CHAT_TYPE:   
            self.chat_latency = time.time() - timestamp
            if( self.chatConnectClass != None ):
                self.chatConnectClass.receive_chat( str( data_payload ), addr )


    #
    # util functions
    #


    # Sets the queue
    def set_audio_queue(self, audio_queue):
        self.audio_queue = audio_queue

    def set_video_queue(self,video_queue):
        self.video_queue = video_queue

    def set_chat_queue(self, chat_queue):
        self.chat_queue = chat_queue


    # Get
    def getAudioLatency(self):
        return 0

    def getChatLatency(self):
        return 0

    def getVideoLatency(self):
        return 0

    def getAudioPacketLoss(self):
        return 0
    
    def getVideoPacketLoss(self):
        return 0



