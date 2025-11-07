"""
Project: Lightwave Communications
Authors: Ian MacDougall, Gage Pavia
Date Created: 12 October 2023
Last Modified: 15 September 2025
File Description: Contains utility functions and helpers used in ui.py.
Repository: https://github.com/IanDMacDougall/Lightwave
"""

#
# Imports
#

import datetime, json, os

from PySide6.QtWidgets import QApplication


#
# Constants
#

SCHEDULED_CALLS_FILE = "scheduled_calls.json"
CONTACTS_FILE = "contacts.json"
SETTING_FILE = "settings.json"
                        
#
# Call Scheduling
#

scheduled_calls = []

def get_scheduled_calls():
    global scheduled_calls
    return scheduled_calls

def remove_past_scheduled_calls():
    global scheduled_calls
    current_datetime = datetime.datetime.now()
    scheduled_calls = [call for call in scheduled_calls
                       if datetime.datetime.strptime(f"{call['date']} {call['time']}", "%m/%d/%Y %I:%M %p") > current_datetime]    
        
#
# Call History
#

call_history = [
    {"date": "11/17/2023", "start_time": "11:30 AM", "end_time": "12:30 PM", 
     "duration": "1:00:00"}  # Sample history call for debugging
]

#
# DateTime Functions
#

def calculate_duration(start_time, end_time):
    start = datetime.datetime.combine(datetime.date.today(), start_time)
    end = datetime.datetime.combine(datetime.date.today(), end_time)
    duration = end - start
    return str(duration)

#
# Call Functions
#

def on_call_end(date, start_time, end_time, participants, history_tab_instance):
    duration = calculate_duration(start_time, end_time)
    call_detail = {
        "date": date.toString("MM/dd/yyyy"),
        "start_time": start_time.toString("h:mm AP"),
        "end_time": end_time.toString("h:mm AP"),
        "duration": duration,
        "participants": ', '.join(participants)  
    }

    call_history.append(call_detail)

    history_tab_instance.updateHistory()

#
# Local Data Saving
#

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
app_data_dir = os.path.join(PROJECT_ROOT, 'data') # Set directory

def ensure_directory_exists(directory): # Creates directory if nonexistant
    if not os.path.exists(directory):
        os.makedirs(directory)

def save_data(file_name, data): 
    ensure_directory_exists(app_data_dir)
    file_path = os.path.join(app_data_dir, file_name)
    with open(file_path, 'w') as file:
        json.dump(data, file, indent=4)

def load_data(file_name):
    file_path = os.path.join(app_data_dir, file_name)
    try:
        with open(file_path, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return []
    

# Saving Settings

'''
Saves the default settings
'''
def save_default(): # consider check for settings integrity?
    DEFAULT_SETTINGS = {
        "resolution": "(640,480)",
        "language": "English",
        "dateFormat": "mm/dd/yyyy",
        "timeFormat": "h:mm AP",
        "notifications": "True",
        "videoDevice": "Device 1",
        "inputDevice": "Device 1",
        "outputDevice": "Device 1",
        "inputVolume": 100,
        "outputVolume": 100
    }
    with open(SETTING_FILE, "w", encoding="utf-8") as f:
        json.dump([DEFAULT_SETTINGS], f, indent=4)
    return DEFAULT_SETTINGS.copy()

'''
Loads settings once application is started
'''
def load_settings():
    try:
        with open(SETTING_FILE, "r", encoding="utf-8") as f:
            return json.load(f)[0]
    except (FileNotFoundError, json.JSONDecodeError):
        return save_default()
    
'''
Should update the desired setting
'''
def update_settings(settingName, settingNewValue):
    with open(SETTING_FILE, "r", encoding="utf-8") as f:
        settings = json.load(f)[0]

    settings[settingName] = settingNewValue

    with open(SETTING_FILE, 'w', encoding="utf-8") as f:
        json.dump(settings, f)
    
def get_call_settings():
    with open(SETTING_FILE, "r", encoding="utf-8") as f:
        settings = json.load(f)[0]
    return {"videoDevice":0, "inputDevice":0, "outputDevice":1, "inputVolume":settings["inputVolume"], "outputVolume":settings["outputVolume"]}


# 
# Text Functions
#

def copy_to_clipboard(text):
    clipboard = QApplication.clipboard()
    clipboard.setText(text)