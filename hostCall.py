"""
Project: Lightwave Communications
Authors: Ian MacDougall, Gage Pavia
Date Created: 12 October 2023
Last Modified: 15 September 2025
File Description: Enables hosting calls within the Lightwave Communications platform.
Repository: https://github.com/IanDMacDougall/Lightwave
"""

from connection.audio import audioConnect
from connection.video import videoConnect
from connection.chat import chatConnect
from connection.header import header
import joinKey

import socket 
import threading
import requests


audioConnectClass = audioConnect()
videoConnectClass = videoConnect()
chatConnectClass = chatConnect()
headerClass = header()


peer_key = ""
port = 5060

#
# IP functions
#

"""
Obtains local IP through short DNS connection
"""   
def get_local_ip():
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
            # Use Google's DNS server address and port
            # No actual connection is made
            sock.connect(("8.8.8.8", 80))
            return sock.getsockname()[0]
    except Exception as e:
        print(f"Error obtaining local IP address: {e}")
        return None


'''
Creates a peer 
'''
def get_key_local():
    hostIP = get_local_ip()
    data_to_compress = f'{hostIP}:{port}'

    # generate key for peer
    peer_key = joinKey.encode_data( joinKey.compress_data( data_to_compress ) )

    print
    return peer_key


"""
Obtains public IP through request from https://httpbin.org/ip
"""
def get_public_ip():
    try:
        response = requests.get('https://httpbin.org/ip')
        public_ip = response.json()['origin']
        return public_ip
    except Exception as e:
        return f"Error obtaining public IP address: {e}"


def get_key_public():
    hostIP = get_public_ip()
    data_to_compress = f'{hostIP}:{port}'

    # generate key for peer
    peer_key = joinKey.encode_data( joinKey.compress_data( data_to_compress ) )

    return peer_key

#
# Hosting functions
#

"""
runs when a local call is started
generates a key based off your local IP address
"""
def hostLocal():
    hostIP = get_local_ip()
    print("host local")
    host( hostIP )


"""
Runs when a online call is started
generates a key off your public IP address
"""
def hostPublic():
    hostIP = get_public_ip()
    print("Host public")
    host( hostIP )


"""
Creates a UDP connection from socket through your IP and port number 5060
"""
def host( hostIP ):
    # UDP Socket Setup
    host_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    host_socket.bind( (hostIP, port) )

    print(f"Listening on {hostIP}:{port}")

    message, client_address = host_socket.recvfrom( 8192 )
    print( message )
    print( "connected to %s", client_address )

    audio_thread = threading.Thread( target=audioConnectClass.network_audio, args=( host_socket, client_address ), name="hostAudioThread" )
    chat_thread = threading.Thread( target=chatConnectClass.network_chat, args=( host_socket, client_address ), name="hostChatThread" )
    video_thread = threading.Thread( target=videoConnectClass.network_video, args=( host_socket, client_address ), name="hostVideoThread" )
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
