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

import datetime, json, os, sounddevice as sd, cv2

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
        "videoDevice": get_default_video_device(),
        "inputDevice": get_default_audio_input_device(),
        "outputDevice": get_default_audio_output_device(),
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
    return {"videoDevice":get_device_id(settings['videoDevice']), "inputDevice":get_device_id(settings['inputDevice']), "outputDevice":get_device_id(settings['outputDevice']), "inputVolume":settings["inputVolume"], "outputVolume":settings["outputVolume"]}


# 
# Text Functions
#

def copy_to_clipboard(text):
    clipboard = QApplication.clipboard()
    clipboard.setText(text)



#
# Input Device Checks
#

def get_video_devices(max_devices=10):
    devices = []

    for i in range(max_devices): # Causes warning when checking capture with bad index
        try: 
            cap = cv2.VideoCapture(i)

            if cap.isOpened():
                device = str(i)+": "+cap.getBackendName()
                devices.append(device)
                cap.release()
        except Exception as e:
            error = e
        except Warning as w:
            warm = w
    
    return devices


def get_audio_input_devices():
    devices = sd.query_devices()
    input_devices = []
    
    for x in devices:
        if x['max_input_channels'] != 0:
            device = str(x['index'])+": "+x['name']
            input_devices.append(device)
    return input_devices


def get_audio_output_devices():
    devices = sd.query_devices()
    output_devices = []
    
    for x in devices:
        if x['max_output_channels'] != 0:
            device = str(x['index'])+": "+x['name']
            output_devices.append(device)
    return output_devices


def get_default_video_device():
    return get_video_devices()[0]

def get_default_audio_input_device():
    index = sd.default.device[0] # 0 for input
    device = str(index)+": "+sd.query_devices(device=index)['name']
    return device

def get_default_audio_output_device():
    index = sd.default.device[1] # 1 for output
    device = str(index)+": "+sd.query_devices(device=index)['name']
    return device

def get_device_id(device):
    if device[1] == ":":
        return int(device[0])
    elif device[2] == ":":
        return int(device[0:2])
    else:
        return int(device[0:3])
