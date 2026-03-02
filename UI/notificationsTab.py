"""
Project: Lightwave Communications
Authors: Ian MacDougall, Gage Pavia
Date Created: 16 December 2025
Last Modified: 16 December 2025
File Description: Class of Lightwaves Comunications
Upadte Description:
Repository: https://github.com/IanDMacDougall/Lightwave
"""

from PySide6.QtCore import QDate
from PySide6.QtWidgets import (QVBoxLayout, QListWidget, QPushButton, QWidget)

from utilities import scheduled_calls

class NotificationsTab(QWidget):
    def __init__(self, scheduled_calls):
        super().__init__()
        self.scheduled_calls = scheduled_calls

        # Main layout for tab
        layout = QVBoxLayout(self)

        # Notifications list
        self.notifications_list = QListWidget()
        layout.addWidget(self.notifications_list)

        # Clear notifications button
        self.clear_button = QPushButton("Clear Notifications")
        self.clear_button.clicked.connect(self.clear_notifications)
        layout.addWidget(self.clear_button)

        # Check for today's calls and notify
        self.notify_todays_calls()

    def add_notification(self, message):
        # Adds a new notification to the list
        self.notifications_list.addItem(message)

    def clear_notifications(self):
        # Clears all notifications
        self.notifications_list.clear()

    def add_system_alert(self, alert_message):
        # Adds a system alert to the notifications
        self.add_notification(f"System Alert: {alert_message}")
    
    def notify_todays_calls(self):
        today = QDate.currentDate().toString("MM/dd/yyyy")
        todays_calls = [call for call in scheduled_calls if call["date"] == today]
        if todays_calls:
            calls_times = "\n".join([f"Reminder: Call scheduled for {call['time']}." for call in todays_calls])
            self.add_notification(f"{calls_times}")
