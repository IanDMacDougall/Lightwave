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
import time

class chatConnect:
    def __init__(self):
        self.headerClass = header()
        self.maxText = 125
        self.chat_queue = queue.Queue()
        
        self.sending = True
    

    """
    Takes input and sends data over socket
    """
    def send_chat(self, socket, client_address):
        while self.sending:
            send_message = "Testing"
            self.headerClass.send_data(socket=socket, addr=client_address, data_type=2, seq_num=0, data_send=send_message.encode(), timestamp=int(time.time()))

    """
    Prints the chat in the queu
    """
    def print_chat(self):
        while self.sending:
            try:
                received_message = self.chat_queue.get_nowait()
                print(received_message)
            except queue.Empty:
                pass
            except Exception as E:
                print(f"print_chat error: {E}")
    

    """
    Starts threads for chat sending & receiving
    """
    def network_chat(self, socket, client_address):
        self.headerClass.set_chat_queue(chat_queue=self.chat_queue)

        send_thread = threading.Thread(target=self.send_chat, args=(socket, client_address), name="sendChatThread")
        receive_thread = threading.Thread(target=self.print_chat, args=(), name="receiveChatThread")
        