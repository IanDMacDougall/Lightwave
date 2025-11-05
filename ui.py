"""
Project: Lightwave Communications
Authors: Ian MacDougall, Gage Pavia
Date Created: 12 October 2023
Last Modified: 5 November 2025
File Description: Manages the user interface components for the application.
Upadte Description: Updated to PySide6
Repository: https://github.com/IanDMacDougall/Lightwave
"""

#
# Imports
#

import csv
import json
from datetime import datetime as dt

from PySide6.QtCore import QDateTime, QDate, Qt, QTime, QTimer, Slot
from PySide6.QtGui import QPixmap, QImage
from PySide6.QtWidgets import (QApplication, QCalendarWidget, QCheckBox, QComboBox,
                                QDialog, QDialogButtonBox, QDateTimeEdit, QFileDialog,
                                QFormLayout, QGridLayout, QHBoxLayout, QLabel, QLineEdit,
                                QListWidget, QListWidgetItem, QMainWindow, QMessageBox,
                                QPushButton, QSlider, QSplashScreen, QTableWidget,
                                QTableWidgetItem, QTextEdit, QTimeEdit, QVBoxLayout,
                                QWidget, QHeaderView, QInputDialog, QTabWidget)

from connection.header import header
from connection.video import videoConnect
from connection.audio import audioConnect
from connection.chat import chatConnect


from utilities import (SCHEDULED_CALLS_FILE, CONTACTS_FILE, SETTING_FILE, 
                       app_data_dir, call_history,
                       get_scheduled_calls, remove_past_scheduled_calls,
                       ensure_directory_exists, save_data, load_data)


import os

#
# Set up
#

headerClass = header()


print(os.name + " - OS name")
os.environ["QT_QPA_PLATFORM_PLUGIN_PATH"] = "/usr/lib/qt/plugins/platforms"

'''
Main Class
'''

class LightwaveCommunications(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Lightwave Communications")
        self.setGeometry(100, 100, 800, 600) # Sets Widnow Size
        self.setFixedSize(800, 600) # Enforce a fixed size for window

        # Main Tab widget
        self.tabs = QTabWidget(self)
        self.setCentralWidget(self.tabs)

        # Create instance of tabs
        self.home_tab = HomeTab()
        self.history_tab = HistoryTab()

        # Add tabs
        self.tabs.addTab(self.home_tab, "Home")
        self.tabs.addTab(ScheduleCallTab(self.home_tab), "Schedule Call")
        self.tabs.addTab(SettingsTab(), "Settings")
        self.tabs.addTab(NotificationsTab(get_scheduled_calls()), "Notifications")
        self.tabs.addTab(ContactsTab(), "Contacts")
        self.tabs.addTab(self.history_tab, "History")
        self.tabs.addTab(AnalyticsTab(), "Analytics")
        self.tabs.addTab(AboutTab(), "About")


#
# Tab Classes
#


'''
Home Tab ~~~~~~~~~~ ~~~~~~~~~~ ~~~~~~~~~~ ~~~~~~~~~~ ~~~~~~~~~~
'''
class HomeTab(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        # Main layout for tab
        layout = QVBoxLayout()

        # Top layout for buttons, clock and scheduled calls list
        top_layout = QHBoxLayout()
        top_layout.setAlignment(Qt.AlignCenter)

        # Call buttons
        join_button = QPushButton("Join Call", self)
        join_button.clicked.connect(self.join_call) # initiates join call
        host_button = QPushButton("Host Call", self)
        host_button.clicked.connect(self.host_call)

        join_button.setFixedSize(100, 40)
        host_button.setFixedSize(100, 40)

        # Clock Widget
        self.clock_widget = QDateTimeEdit(QDateTime.currentDateTime(), self)
        self.clock_widget.setReadOnly(True)
        self.clock_widget.setDisplayFormat("h:mm AP")
        self.clock_widget.setStyleSheet("""
                background-color: #00000000;
                border: none;
                font-size: 32px;
                padding: 20px;
                border-radius: 15px;
        """)
        self.clock_widget.setFixedWidth(200)

        # Timer to update clock every second
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_clock)
        self.timer.start(1000)

        # Create list of schedule calls
        self.schedule_calls_list = QListWidget()
        self.schedule_calls_list.setFixedWidth(150)
        self.schedule_calls_list.setFixedHeight(200)

        # Ensure the scheduled calls list can be focused to recieve key events
        self.schedule_calls_list.setFocusPolicy(Qt.StrongFocus)

        # Add widgets to layout
        top_layout.addWidget(join_button)
        top_layout.addWidget(host_button)
        top_layout.addWidget(self.clock_widget)
        top_layout.addWidget(self.schedule_calls_list)

        # Display Layout
        layout.addLayout(top_layout)
        self.setLayout(layout)

    def keyPressEvent(self, event):
        if self.schedule_calls_list.hasFocus():
            if event.key() in [Qt.Key_Backspace, Qt.Key_Delete]:
                selected_items = self.schedule_calls_list.selectedItems()
                if selected_items:
                    item_text = selected_items[0].text()
                    for call in scheduled_calls:
                        scheduled_calls.remove(call) # Remove the matched call from the scheduled calls list
                        save_data(SCHEDULED_CALLS_FILE, scheduled_calls)
                        self.update_scheduled_calls()
                        break
    
    def update_scheduled_calls(self):
        remove_past_scheduled_calls()
        self.schedule_calls_list.clear()

        global scheduled_calls

        # Creates scheduled calls list header
        list_header = QListWidgetItem(f"Scheuled Calls")
        list_header.setFlags(Qt.NoItemFlags)  # Make the header non-selectable and non-interactive
        self.schedule_calls_list.addItem(list_header)

        # Sort scheduled calls by date
        sorted_calls = sorted(scheduled_calls, key=lambda x: x["date"])

        current_date = None
        for call in sorted_calls:
            
            # Check if the date is different
            if call["date"] != current_date:
                current_date = call["date"]
                
                # Add a header for the different date
                date_header = QListWidgetItem(f"\nDate: {current_date}")
                date_header.setFlags(Qt.NoItemFlags)  # Make the header non-selectable and non-interactive
                self.schedule_calls_list.addItem(date_header)

            # Add calls to list
            item_text = f"Time: {call['time']}"
            self.schedule_calls_list.addItem(item_text)

    '''
    Runs once Host Call button is clicked
    '''
    def host_call(self):
        dialog = QDialog(self)
        dialog.setWindowTitle("Host Call")
        layout = QGridLayout(dialog)

        label = QLabel("Choose how you want to host.")
        layout.addWidget(label, 0, 0, 1, 2)

        local_button = QPushButton("Local Host")
        local_button.clicked.connect(dialog.accept)
        layout.addWidget(local_button, 1, 0)

        public_button = QPushButton("Public Host")
        public_button.clicked.connect(dialog.reject)
        layout.addWidget(public_button, 1, 1)

        response = dialog.exec_()
        if response == 1: # dialog accepted
            print('Local')
            self.host_local()
        else: # dialog rejected
            print('Public')
            self.host_public()
        

    '''
    Runs once Host Local is clicked

    posts the key for the other user, using a local key
    '''
    def host_local(self):
        from utilities import copy_to_clipboard
        from hostCall import hostLocal, get_key_local
        peer_key = get_key_local()
        self.setWindowTitle("Local Host")
        
        dialog = QDialog(self)
        layout = QGridLayout(dialog)

        label = QLabel(f"Call Key: {peer_key}")
        layout.addWidget(label, 0, 0, 1, 2)

        copy_button = QPushButton("Copy Key")
        copy_button.clicked.connect(lambda: copy_to_clipboard(peer_key))
        layout.addWidget(copy_button, 1, 0)

        ok_button = QPushButton("OK")
        ok_button.clicked.connect(dialog.accept)
        layout.addWidget(ok_button, 1, 1)

        response = dialog.exec()
        if response == 1: # dialog accepted
            print('Hosting Local')
            hostLocal()

    '''
    Runs once Host Public is clicked

    posts the key for the other user, using a public key
    '''
    def host_public(self):
        from utilities import copy_to_clipboard
        from hostCall import hostPublic, get_key_public
        peer_key = get_key_public()
        self.setWindowTitle("Public Host")
        
        dialog = QDialog(self)
        layout = QGridLayout(dialog)

        label = QLabel(f"Call Key: {peer_key}")
        layout.addWidget(label, 0, 0, 1, 2)

        copy_button = QPushButton("Copy Key")
        copy_button.clicked.connect(lambda: copy_to_clipboard(peer_key))
        layout.addWidget(copy_button, 1, 0)

        ok_button = QPushButton("OK")
        ok_button.clicked.connect(dialog.accept)
        layout.addWidget(ok_button, 1, 1)

        response = dialog.exec()
        if response == 1: # dialog accepted
            print('Host Public')
            hostPublic()


    def join_call(self):
        enteredKey, okPressed = QInputDialog.getText(self, "Join Call", "Enter call key: ", QLineEdit.Normal, "")
        if okPressed:
            from joinCall import peer
            peer(enteredKey)

    def update_clock(self):
        self.clock_widget.setDateTime(QDateTime.currentDateTime())


'''
Schedule Call Tab ~~~~~~~~~~ ~~~~~~~~~~ ~~~~~~~~~~ ~~~~~~~~~~ ~~~~~~~~~~
'''
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

'''
Settings Tab ~~~~~~~~~~ ~~~~~~~~~~ ~~~~~~~~~~ ~~~~~~~~~~ ~~~~~~~~~~
'''
class SettingsTab(QWidget):    
    def __init__(self, parent=None):
        super().__init__(parent)

        global DEFAULT_SETTINGS
        DEFAULT_SETTINGS = {
            "volume": 100,
            "notifications": "True",
            "resolution": "(640,480)"
        }
        settings = self.load_settings()
        
        # Main layout for tab
        layout = QFormLayout()
        
        # change audio to slider, 0 -> 100 actual 0.0 -> 1.0 
        # Audio Volume settings
        audio_volume_label = QLabel("Audio Volume:")
        global audio_volume_slider
        audio_volume_slider = QSlider(Qt.Horizontal)
        audio_volume_slider.setMinimum(0)
        audio_volume_slider.setMaximum(100)
        audio_volume_slider.setValue(settings['volume'])  # Default value

        # Notification settings
        notifications_label = QLabel("Notifications:")
        global notifications_checkbox
        notifications_checkbox = QCheckBox("Enable Notifications")
        notifications_checkbox.setChecked(settings['notifications'] == "True")
        
        # resolution       
        resolution_label = QLabel("Resolution:")
        global resolution_combobox
        resolution_list = ["(640,360)","(640,480)","(800,600)","(1024,768)","(1280,720)","(1360,768)","(1440,900)","(1920,1080)","(2560,1440)","(3440,1440)","(3840,2160)"]
        resolution_combobox = QComboBox()
        self.resolution_combobox = resolution_combobox
        self.resolution_combobox.addItems(resolution_list)
        self.resolution_combobox.setCurrentIndex(resolution_list.index(settings['resolution']))

        # Save settings button 
        save_button = QPushButton("Save Settings")
        save_button.clicked.connect(self.save_settings)

        # Layout
        layout.addRow(audio_volume_label, audio_volume_slider)
        layout.addRow(notifications_label, notifications_checkbox)
        layout.addRow(resolution_label, self.resolution_combobox)
        layout.addWidget(save_button)
        
        # Set layout
        self.setLayout(layout)  
    
    '''
    Saves the default settings
    '''
    def save_default(self):
        with open(SETTING_FILE, "w", encoding="utf-8") as f:
            json.dump([DEFAULT_SETTINGS], f, indent=4)

    '''
    Loads settings once application is started
    '''
    def load_settings(self):
        try:
            with open(SETTING_FILE, "r", encoding="utf-8") as f:
                return json.load(f)[0]
        except (FileNotFoundError, json.JSONDecodeError):
            self.save_default()
            return DEFAULT_SETTINGS.copy()
            
    '''
    Runs when you click Save Settings button
    '''
    def save_settings(self):
        #audioConnectClass.set_volume_level(audio_volume_slider.value())
        #videoConnectClass.set_resolution(eval(self.resolution_combobox.currentText()))

        volume = audio_volume_slider.value()
        notification = notifications_checkbox.isChecked()
        resolution = resolution_combobox.currentText()

        settings = {}
        settings["volume"] = volume
        settings["notifications"] = str(notification)
        settings["resolution"] = resolution

        with open(SETTING_FILE, "w", encoding="utf-8") as f:
            json.dump([settings], f, indent=4)

        QMessageBox.information(self, "Settings", f"Settings saved.")
        
    
'''
Notifications Tab ~~~~~~~~~~ ~~~~~~~~~~ ~~~~~~~~~~ ~~~~~~~~~~ ~~~~~~~~~~
'''
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
        audio_latency = headerClass.getAudioLatency()
        audio_packet_loss = headerClass.getAudioPacketLoss()
        video_frame_rate = headerClass.getVideoLatency()
        video_latency = headerClass.getVideoLatency()
        video_packet_loss = headerClass.getVideoPacketLoss()

        # Updating labels with data
        self.audio_latency_label.setText(f"Audio Latency: {audio_latency}")
        self.audio_packet_loss_label.setText(f"Audio Packet Loss: {audio_packet_loss}")
        self.video_frame_rate_label.setText(f"Video Frame Rate: {video_frame_rate}")
        self.video_packet_loss_label.setText(f"Video Packet Loss: {video_packet_loss}")

'''
Contacts Tab ~~~~~~~~~~ ~~~~~~~~~~ ~~~~~~~~~~ ~~~~~~~~~~ ~~~~~~~~~~
'''
class ContactsTab(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        
        layout = QVBoxLayout()

        self.contact_table = QTableWidget(0, 4)
        self.contact_table.setHorizontalHeaderLabels(["First Name", "Last Name", "Email", "Group"])
        self.contact_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        add_contact_button = QPushButton("Add Contact")
        add_contact_button.clicked.connect(self.show_add_contact_dialog)

        remove_contact_button = QPushButton("Remove Selected Contact")
        remove_contact_button.clicked.connect(self.remove_contact)

        search_bar = QLineEdit()
        search_bar.setPlaceholderText("Search Contacts")
        search_bar.textChanged.connect(self.search_contacts)

        import_button = QPushButton("Import Contacts")
        export_button = QPushButton("Export Contacts")
        import_button.clicked.connect(self.import_contacts)
        export_button.clicked.connect(self.export_contacts)

        layout.addWidget(search_bar)
        layout.addWidget(self.contact_table)
        layout.addWidget(add_contact_button)
        layout.addWidget(remove_contact_button)
        layout.addWidget(import_button)
        layout.addWidget(export_button)

        self.load_contacts()

        self.setLayout(layout)  

    def show_add_contact_dialog(self):
        dialog = QDialog(self)
        dialog.setWindowTitle("Add Contact")
        layout = QFormLayout(dialog)

        firstNameLineEdit = QLineEdit(dialog)
        lastNameLineEdit = QLineEdit(dialog)
        emailLineEdit = QLineEdit(dialog)
        groupLineEdit = QLineEdit(dialog)

        layout.addRow("First Name:", firstNameLineEdit)
        layout.addRow("Last Name:", lastNameLineEdit)
        layout.addRow("Email:", emailLineEdit)
        layout.addRow("Group:", groupLineEdit)

        buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel, Qt.Horizontal, dialog)
        
        layout.addWidget(buttons)

        buttons.accepted.connect(lambda: self.add_contact(dialog, firstNameLineEdit, lastNameLineEdit, emailLineEdit, groupLineEdit))
        buttons.rejected.connect(dialog.reject)

        dialog.exec_()

    def add_contact(self, dialog, firstNameLineEdit, lastNameLineEdit, emailLineEdit, groupLineEdit):
        row_position = self.contact_table.rowCount()
        self.contact_table.insertRow(row_position)
        self.contact_table.setItem(row_position, 0, QTableWidgetItem(firstNameLineEdit.text()))
        self.contact_table.setItem(row_position, 1, QTableWidgetItem(lastNameLineEdit.text()))
        self.contact_table.setItem(row_position, 2, QTableWidgetItem(emailLineEdit.text()))
        self.contact_table.setItem(row_position, 3, QTableWidgetItem(groupLineEdit.text()))
        dialog.accept()
        save_data(CONTACTS_FILE, self.get_contacts_data())

    def remove_contact(self):
        selected_items = self.contact_table.selectedItems()
        if selected_items:
            selected_row = selected_items[0].row()
            self.contact_table.removeRow(selected_row)
        else:
            QMessageBox.warning(self, "No Selection", "Please select a contact to remove.")
        save_data(CONTACTS_FILE, self.get_contacts_data())

    def search_contacts(self, text):
        for row in range(self.contact_table.rowCount()):
            row_matches = False
            for column in range(self.contact_table.columnCount()):
                item = self.contact_table.item(row, column)
                if item and text.lower() in item.text().lower():
                    row_matches = True
                    break

            self.contact_table.setRowHidden(row, not row_matches)

    def import_contacts(self):
        options = QFileDialog.Options()
        fileName, _ = QFileDialog.getOpenFileName(self, "Import Contacts", "", "CSV Files (*.csv);;All Files (*)", options=options)
        if fileName:
            with open(fileName, mode="r", newline="", encoding="utf-8") as file:
                reader = csv.reader(file)

                for row in reader:
                    if len(row) == 4:  # Ensure that each row has exactly 4 columns
                        self.add_contact_from_str(row)
                    else:
                        QMessageBox.warning(self, "Import Error", f"Row format error: {row}")

            QMessageBox.information(self, "Import Complete", "Contacts successfully imported.")

    def export_contacts(self):
        options = QFileDialog.Options()
        fileName, _ = QFileDialog.getSaveFileName(self, "Export Contacts", "", "CSV Files (*.csv);;All Files (*)", options=options)
        if fileName:
            with open(fileName, mode="w", newline="", encoding="utf-8") as file:
                writer = csv.writer(file)
                for row in range(self.contact_table.rowCount()):
                    rowData = [self.contact_table.item(row, i).text() for i in range(self.contact_table.columnCount())]
                    writer.writerow(rowData)
            QMessageBox.information(self, "Export Successful", f"Contacts successfully exported to {fileName}.")

    def add_contact_from_str(self, contact_data):
        row_position = self.contact_table.rowCount()
        self.contact_table.insertRow(row_position)

        for i, data in enumerate(contact_data):
            self.contact_table.setItem(row_position, i, QTableWidgetItem(data))

    def load_contacts(self):
        contacts = load_data(CONTACTS_FILE)
        for contact in contacts:
            self.add_contact_from_str(contact)

    def get_contacts_data(self):
        contacts = []
        for row in range(self.contact_table.rowCount()):
            row_data = []
            for column in range(self.contact_table.columnCount()):
                item = self.contact_table.item(row, column)
                row_data.append(item.text() if item is not None else "")
            contacts.append(row_data)
        return contacts

'''
History Tab ~~~~~~~~~~ ~~~~~~~~~~ ~~~~~~~~~~ ~~~~~~~~~~ ~~~~~~~~~~
'''
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
About Tab ~~~~~~~~~~ ~~~~~~~~~~ ~~~~~~~~~~ ~~~~~~~~~~ ~~~~~~~~~~
'''
class AboutTab(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        
        about_label = QLabel("Lightwave Communications\nVersion 1.0.0\nDeveloped by the Lightwave Team")
        about_label.setAlignment(Qt.AlignCenter)

        version_history_label = QLabel("Version History:")
        version_history_text = QTextEdit()
        version_history_text.setReadOnly(True)
        version_history_label = QLabel("Version History:")
        version_history_text = QTextEdit()
        version_history_text.setReadOnly(True)

        version_history_text.append("Version 1.0.0 - Initial Release - Pending")
        version_history_text.append("- Initial release with full features.")
        version_history_text.append("\n")

        version_history_text.append("Version 0.1.1 - Beta 2 - Released 11/27/2023")
        version_history_text.append("- Added new user interface elements.")
        version_history_text.append("\n")

        version_history_text.append("Version 0.1.0 - Beta 1 - Released 11/21/2023")
        version_history_text.append("- Initial beta release for testing.")
        version_history_text.append("- Core functionalities introduced.")

        credits_label = QLabel("Credits:")
        credits_text = QTextEdit()
        credits_text.setReadOnly(True)
        credits_text.setPlainText("Developed by the Lightwave Team\nContributors: Ian MacDougall, Gage Pavia")

        layout = QVBoxLayout()
        layout.addWidget(about_label)
        layout.addWidget(version_history_label)
        layout.addWidget(version_history_text)
        layout.addWidget(credits_label)
        layout.addWidget(credits_text)
        
        self.setLayout(layout)  


'''
Client active window
'''
class ClientWindow(QWidget):
    def __init__(self, parent = None):
        super().__init__(parent)
        self.setWindowTitle("Client Communications")

        self.setGeometry(100, 100, 800, 600)  # Set window size
        self.setFixedSize(100, 800)  # Enforce a fixed size for window










'''
Application launch
'''

if __name__ == "__main__":
    app = QApplication([])
    
    
    # Ensure directory
    ensure_directory_exists(app_data_dir)  
    
    # Update scheduled calls from local files 
    scheduled_calls = load_data(SCHEDULED_CALLS_FILE)
    remove_past_scheduled_calls()  
    save_data(SCHEDULED_CALLS_FILE, scheduled_calls)
    window = LightwaveCommunications()  
    
    # Logo display ("splash screen")
    splash_pix = QPixmap('logo.png')  
    
    splash = QSplashScreen(splash_pix)
    splash.show()
    
    app.processEvents()
    
    QTimer.singleShot(3000, splash.close)
    QTimer.singleShot(3000, window.show)
    
    # Execute
    app.exec()