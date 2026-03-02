"""
Project: Lightwave Communications
Authors: Ian MacDougall, Gage Pavia
Date Created: 16 December 2025
Last Modified: 16 December 2025
File Description: Class of Lightwaves Comunications
Upadte Description:
Repository: https://github.com/IanDMacDougall/Lightwave
"""

from PySide6.QtCore import (QTimer, Slot)
from PySide6.QtWidgets import (QTableWidgetItem, QVBoxLayout, QTableWidget, QHeaderView, QPushButton,
                               QLabel, QWidget)

from utilities import call_history
from connection.header import header

class HistoryTab(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        layout = QVBoxLayout()

        self.history_table = QTableWidget(0, 4)
        self.history_table.setHorizontalHeaderLabels(["Date", "Start Time", "End Time", "Duration"])
        self.history_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        clear_history_button = QPushButton("Clear History")
        clear_history_button.clicked.connect(self.clear_history)

        layout.addWidget(self.history_table)
        layout.addWidget(clear_history_button)
        
        self.update_history()

        self.setLayout(layout)

    def update_history(self):
        self.history_table.setRowCount(len(call_history))
        for row, call in enumerate(call_history):
            self.history_table.setItem(row, 0, QTableWidgetItem(call["date"]))
            self.history_table.setItem(row, 1, QTableWidgetItem(call["start_time"]))
            self.history_table.setItem(row, 2, QTableWidgetItem(call["end_time"]))
            self.history_table.setItem(row, 3, QTableWidgetItem(call["duration"]))

    def clear_history(self):
        global call_history
        call_history.clear()
        self.update_history()




'''
Analytics Tab ~~~~~~~~~~ ~~~~~~~~~~ ~~~~~~~~~~ ~~~~~~~~~~ ~~~~~~~~~~
'''
class AnalyticsTab(QWidget):
    
    def __init__(self, parent=None):
        super().__init__(parent)

        # Main layout for tab
        layout = QVBoxLayout()
        

        # Create labels for each metric
        self.audio_latency_label = QLabel("Audio Latency: N/A")
        self.audio_packet_loss_label = QLabel("Audio Packet Loss: N/A")
        self.video_frame_rate_label = QLabel("Video Frame Rate: N/A")
        self.video_packet_loss_label = QLabel("Video Packet Loss: N/A")

        # Add labels to layout
        layout.addWidget(self.audio_latency_label)
        layout.addWidget(self.audio_packet_loss_label)
        layout.addWidget(self.video_frame_rate_label)
        layout.addWidget(self.video_packet_loss_label)

        # Start a timer to refresh analytics data
        self.analytics_timer = QTimer(self)
        self.analytics_timer.timeout.connect(self.update_analytics)
        self.analytics_timer.start(1000)  # Update every second

        # Set layout on tab
        self.setLayout(layout)

    @Slot()
    def update_analytics(self):
        audio_latency = header.getAudioLatency(self=self)
        audio_packet_loss = header.getAudioPacketLoss(self=self)
        video_frame_rate = header.getVideoLatency(self=self)
        video_latency = header.getVideoLatency(self=self)
        video_packet_loss = header.getVideoPacketLoss(self=self)

        # Updating labels with data
        self.audio_latency_label.setText(f"Audio Latency: {audio_latency}")
        self.audio_packet_loss_label.setText(f"Audio Packet Loss: {audio_packet_loss}")
        self.video_frame_rate_label.setText(f"Video Frame Rate: {video_frame_rate}")
        self.video_packet_loss_label.setText(f"Video Packet Loss: {video_packet_loss}")