"""
Project: Lightwave Communications
Authors: Ian MacDougall, Gage Pavia
Date Created: 16 December 2025
Last Modified: 16 December 2025
File Description: Class of Lightwaves Comunications
Upadte Description:
Repository: https://github.com/IanDMacDougall/Lightwave
"""

import datetime as dt

from PySide6.QtCore import (QDate, QTime)
from PySide6.QtWidgets import (QVBoxLayout, QLabel, QCalendarWidget, QTimeEdit, QPushButton,
                               QMessageBox, QWidget)

from utilities import scheduled_calls, save_data, SCHEDULED_CALLS_FILE

class ScheduleCallTab(QWidget):
    def __init__(self, home_tab_instance, parent=None):
        super().__init__(parent)
        self.home_tab = home_tab_instance

        layout = QVBoxLayout()
        
        date_label = QLabel("Select Date:")
        self.calendar = QCalendarWidget()
        self.calendar.setMinimumDate(QDate.currentDate())

        time_label = QLabel("Select Time:")
        self.time_edit = QTimeEdit()
        self.time_edit.setTime(QTime.currentTime())

        schedule_button = QPushButton("Schedule Call")
        schedule_button.clicked.connect(self.schedule_call)

        layout.addWidget(date_label)
        layout.addWidget(self.calendar)
        layout.addWidget(time_label)
        layout.addWidget(self.time_edit)
        layout.addWidget(schedule_button)

        self.setLayout(layout)

    '''
    Schedules a call using time and date selected by user
    '''
    def schedule_call(self):
        selected_date = self.calendar.selectedDate()
        string_date = selected_date.toString("MM/dd/yyyy")
        selected_time = self.time_edit.time().toString("h:mm AP")
        now = dt.now()
        date_added = now.strftime("%m/%d/%Y")
        time_added = now.strftime("%I:%M %p")

        scheduled_calls.append({"date": string_date, "time": selected_time, "date_added": date_added, "time_added": time_added })
        QMessageBox.information(self, "Schedule Call", f"Call scheduled for {string_date} at {selected_time}.")

        # Save the updated list of scheduled calls
        self.home_tab.update_scheduled_calls()
        save_data(SCHEDULED_CALLS_FILE, scheduled_calls)
