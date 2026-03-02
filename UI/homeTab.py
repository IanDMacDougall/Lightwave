"""
Project: Lightwave Communications
Authors: Ian MacDougall, Gage Pavia
Date Created: 16 December 2025
Last Modified: 16 December 2025
File Description: Class of Lightwaves Comunications
Upadte Description:
Repository: https://github.com/IanDMacDougall/Lightwave
"""


from PySide6.QtCore import Qt, QDateTime, QTimer
from PySide6.QtWidgets import (QVBoxLayout, QHBoxLayout, QPushButton, QDateTimeEdit, QListWidget,
                               QListWidgetItem, QDialog, QGridLayout, QLabel, QLineEdit, QInputDialog,  QWidget)

from utilities import SCHEDULED_CALLS_FILE, save_data, remove_past_scheduled_calls, scheduled_calls, get_call_settings

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
            callSettings = get_call_settings()

            print('Hosting Local')
            hostLocal(callSettings=callSettings)

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
            callSettings = get_call_settings()

            print('Host Public')
            hostPublic(callSettings=callSettings)


    def join_call(self):
        enteredKey, okPressed = QInputDialog.getText(self, "Join Call", "Enter call key: ", QLineEdit.Normal, "")
        if okPressed and len(enteredKey) > 2:
            from joinCall import peer
            callSettings = get_call_settings()
            peer(enteredKey, callSettings=callSettings)

    def update_clock(self):
        self.clock_widget.setDateTime(QDateTime.currentDateTime())

    def update_timeFormat(self, timeFormat):
        self.clock_widget.setDisplayFormat(timeFormat)
