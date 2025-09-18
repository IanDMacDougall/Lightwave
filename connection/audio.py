"""
Project: Lightwave Communications
Authors: Ian MacDougall, Gage Pavia
Date Created: 15 September 2025
Last Modified: 15 September 2025
File Description: Manages video connection aspects.
Repository: https://github.com/IanDMacDougall/lightwave
"""

from header import header

import threading
import queue
import sounddevice as sd
import numpy as np
import time as t

class audioConnect:
    def __init__(self, volume=100, inputIndex=0, outputIndex=1):
        self.headerClass = header()

        self.samplerate = 48000
        self.channels = 2
        self.dtype =  np.float32

        self.audio_volume = volume

        self.inputDevice = sd.default.device[inputIndex]
        self.outputDevice = sd.default.device[outputIndex]

        self.audio_queue = queue.Queue()

        self.sending = True
        self.mute = False

    
    """
    Uses socket to send data
     - Runs by using InputStream to have a callback that sends data through header
    """
    def stream_audio(self, socket, client_address):
        # turns users audio input data, then sends input via header
        def input_audio_callback(indata, frames, time, status):
            if status:
                print(f"stream_audio status: {status}")
                pass
            audioData = indata.tobytes()
            self.headerClass.send_data(socket=socket, addr=client_address, data_type=0, seq_num=0, data_send=audioData, timestamp=int(t.time()))

        with sd.InputStream(callback=input_audio_callback, samplerate=self.samplerate, channels=self.channels, dtype=self.dtype, device=self.inputDevice) as in_stream:
            try:
                in_stream.start()
                while self.sending and not self.mute:
                    t.sleep(0.2)
            except KeyboardInterrupt:
                print("Stopped stream_audio...")
            finally:
                in_stream.stop()


    """
    Uses Socket to receive audio
     - OutputStream proccess the data through a callback
    """
    def play_audio(self, socket):
        # gets audio from header then places it into a queue to be played
        def out_audio_callback(outdata, frames, time, status):
            if status:
                print(f"play_audio status: {status}")
                pass
            try:
                outputData = self.audio_queue.get_nowait()
                outputData = outputData.reshape(-1, self.channels)

                if outputData is None:
                    # no data is received, nothing is outputed
                    outdata[:] = 0
                elif len( outputData ) < len( outdata ):
                    # the received data is insufficient, fill the rest with zeros
                    new_len = len( outputData )
                    outdata[:new_len ] = outputData[:len(outputData) ] 
                    outdata[ new_len:] = outputData[ len(outputData):]
                else:
                    # the correct ammount of data is received
                    min_len = min(len(outputData), len(outdata))
                    outdata[ :min_len] = outputData[ :min_len]
                    outdata[min_len: ] = outputData[min_len: ]
            except queue.Empty:
                print("Audio buffer is empty")
                pass
            except Exception as E:
                print(f"Audio Callback error : {E}")
                pass
        with sd.OutputStream(callback=out_audio_callback, samplerate=self.samplerate, channels=self.channels, dtype=self.dtype, device=self.outputDevice) as out_stream:
            try:
                out_stream.start()
                while self.sending:
                    self.headerClass.receive_data(socket=socket)
                    
            except KeyboardInterrupt:
                print("Stopped play_audio...")
            finally:
                out_stream.stop()

    """
    Starts threads for audio sending & receiving 
    """
    def network_audio(self, socket, client_address):
        self.headerClass.set_audio_queue(audio_queue=self.audio_queue)

        send_thread = threading.Thread(target=self.stream_audio, args=(socket, client_address), name="micThread")
        receive_thread = threading.Thread(target=self.play_audio, args=(socket,), name="audioThread")
        send_thread.start()
        receive_thread.start()

        try:
            send_thread.join()
            receive_thread.join()
        except KeyboardInterrupt:
            print("Stopping network audio threads")
    
    # util

    def set_volume_level(self, volume_level):
        self.audio_volume = volume_level