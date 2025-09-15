"""
Project: Lightwave Communications
Authors: Ian MacDougall, Gage Pavia
Date Created: 12 October 2023
Last Modified: 15 September 2025
File Description: Enables joining calls within the Lightwave Communications platform.
Repository: https://github.com/IanDMacDougall/Lightwave
"""

from audioConnect import audioConnect
from videoConnect import videoConnect
from chatConnect import chatConnect
from header import header
import joinKey

import socket 
import threading

audioConnectClass = audioConnect()
videoConnectClass = videoConnect()
chatConnectClass = chatConnect()
headerClass = header()

"""
run when joinning a peer
"""
def peer( key ): # run by peer
    host_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # UDP Socket Setup

    # waits for host's key
    host_key = key
    decompressed_key = joinKey.decompress_data( joinKey.decode_data( host_key ) )
    host, host_port = decompressed_key.split(":")
    host_port = int( host_port )

    host_address = ( host, host_port )

    print( "Looking for host..." )

    # initializes UDP connection
    message = "Hello from peer"
    host_socket.sendto( message.encode( 'utf-8' ), ( host, host_port ) )

    # initializes threads for user
    audio_thread = threading.Thread( target=audioConnectClass.network_audio, args=( host_socket, host_address ), name="peerAudioThread" )
    chat_thread = threading.Thread( target=chatConnectClass.network_chat, args=( host_socket, host_address ), name="peerChatThread" )
    video_thread = threading.Thread( target=videoConnectClass.network_video, args=( host_socket, host_address ), name="peerVideoThread" )
    received_thread = threading.Thread( target=headerClass.receive_data, args=( host_socket, ), name="receivedDataThread" )

    audio_thread.start()
    chat_thread.start()
    video_thread.start()
    received_thread.start()

    try:
        pass
    except KeyboardInterrupt:
        print("Stopping network audio threads.")
    finally:
        audio_thread.join()
        chat_thread.join()
        video_thread.join()
        received_thread.join()
        host_socket.close()