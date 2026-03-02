"""
Project: Lightwave Communications
Authors: Ian MacDougall, Gage Pavia
Date Created: 16 December 2025
Last Modified: 16 December 2025
File Description: Class of Lightwaves Comunications
Upadte Description:
Repository: https://github.com/IanDMacDougall/Lightwave
"""

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (QVBoxLayout, QGroupBox, QComboBox, QFormLayout, QLabel, QCheckBox, QSlider, QWidget, QPushButton, QMessageBox)

from utilities import load_settings, get_audio_input_devices, get_audio_output_devices, get_video_devices, SETTING_FILE

import json

class SettingsTab(QWidget):    
    def __init__(self, HomeTab=None, parent=None):
        super().__init__(parent)
        self.main_window = parent
        self.home_tab = HomeTab


        settings = load_settings()
        
        # Main layout for tab
        layout = QVBoxLayout()

        ### General Settings Section
        general_group = QGroupBox("General Settings")
        general_layout = QFormLayout()
        # Resolution      
        resolution_label = QLabel("Resolution:")
        resolution_list = ["(640,360)","(640,480)","(800,600)","(1024,768)","(1280,720)","(1360,768)","(1440,900)","(1920,1080)","(2560,1440)","(3440,1440)","(3840,2160)"]
        resolution_combobox = QComboBox()
        self.resolution_combobox = resolution_combobox
        self.resolution_combobox.addItems(resolution_list)
        self.resolution_combobox.setCurrentIndex(resolution_list.index(settings['resolution']))
        # Language
        language_label = QLabel("Language")
        language_list = ["English"]
        language_combobox = QComboBox()
        self.language_combobox = language_combobox
        self.language_combobox.addItems(language_list)
        self.language_combobox.setCurrentIndex(language_list.index(settings['language']))
        # Date Format
        dateFormat_label = QLabel("Date Format")
        dateFormat_list = ["mm/dd/yyyy", "dd/mm/yyyy", "mm-dd-yyyy", "dd-mm-yyyy", "mm.dd.yyyy", "dd.mm.yyyy","yyyy/mm/dd", "yyyy/dd/mm", "yyyy-mm-dd", "yyyy-dd-mm", "yyyy.mm.dd", "yyyy.dd.mm"]
        dateFormat_combobox = QComboBox()
        self.dateFormat_combobox = dateFormat_combobox
        self.dateFormat_combobox.addItems(dateFormat_list)
        self.dateFormat_combobox.setCurrentIndex(dateFormat_list.index(settings['dateFormat']))
        # Time Format
        timeFormat_label = QLabel("Time Format")
        timeFormat_list = ["h:mm AP", "hh:mm AP", "h:mm", "hh:mm", "HH:mm"]
        timeFormat_combobox = QComboBox()
        self.timeFormat_combobox = timeFormat_combobox
        self.timeFormat_combobox.addItems(timeFormat_list)
        self.timeFormat_combobox.setCurrentIndex(timeFormat_list.index(settings['timeFormat']))
        # Notification settings
        notifications_label = QLabel("Notifications:")
        notifications_checkbox = QCheckBox("Enable Notifications")
        self.notifications_checkbox = notifications_checkbox
        self.notifications_checkbox.setChecked(settings['notifications'] == "True")
        # General Layout
        general_layout.addRow(resolution_label, self.resolution_combobox)
        general_layout.addRow(language_label, self.language_combobox)
        general_layout.addRow(dateFormat_label, self.dateFormat_combobox)
        general_layout.addRow(timeFormat_label, self.timeFormat_combobox)
        general_layout.addRow(notifications_label, notifications_checkbox)
        general_group.setLayout(general_layout)


        ### Video Settings Section
        videoSettings_group = QGroupBox("Video Settings")
        videoSettings_layout = QFormLayout()
        # Camera Device
        videoDevice_label = QLabel("Camera Device: ")
        videoDevice_list = get_video_devices() # //Needs to be the device accessable on the device
        videoDevice_combobox = QComboBox()
        self.videoDevice_combobox = videoDevice_combobox
        self.videoDevice_combobox.addItems(videoDevice_list)
        self.videoDevice_combobox.setCurrentIndex(videoDevice_list.index(settings['videoDevice']))
        # Connection Camera Resolution ?
        # User Camera Resolution ?
        # Video Settings Layout
        videoSettings_layout.addRow(videoDevice_label, self.videoDevice_combobox)
        videoSettings_group.setLayout(videoSettings_layout)


        ### Audio Settings Section
        audioSettings_group = QGroupBox("Audio Settings")
        audioSettings_layout = QFormLayout()
        # Input Device
        inputDevice_label = QLabel("Input Device:")
        inputDevice_list = get_audio_input_devices()
        inputDevice_combobox = QComboBox()
        self.inputDevice_combobox = inputDevice_combobox
        self.inputDevice_combobox.addItems(inputDevice_list)
        self.inputDevice_combobox.setCurrentIndex(inputDevice_list.index(settings['inputDevice']))
        # output Device
        outputDevice_label = QLabel("Output Device:")
        outputDevice_list = get_audio_output_devices()
        outputDevice_combobox = QComboBox()
        self.outputDevice_combobox = outputDevice_combobox
        self.outputDevice_combobox.addItems(outputDevice_list)
        self.outputDevice_combobox.setCurrentIndex(outputDevice_list.index(settings['outputDevice']))
        # Device Input Volume
        inputVolume_label = QLabel("Input Device Volume:")
        inputVolume_slider = QSlider(Qt.Horizontal)
        self.inputVolume_slider = inputVolume_slider
        self.inputVolume_slider.setMinimum(0)
        self.inputVolume_slider.setMaximum(100)
        self.inputVolume_slider.setValue(settings['inputVolume'])
        # Output Volume
        outputVolume_label = QLabel("Output Volume:")
        outputVolume_slider = QSlider(Qt.Horizontal)
        self.outputVolume_slider = outputVolume_slider
        self.outputVolume_slider.setMinimum(0)
        self.outputVolume_slider.setMaximum(100)
        self.outputVolume_slider.setValue(settings['outputVolume'])
        # Playback ?
        # Playback Volume ?
        # Audio Settings Layout
        audioSettings_layout.addRow(inputDevice_label, self.inputDevice_combobox)
        audioSettings_layout.addRow(outputDevice_label, self.outputDevice_combobox)
        audioSettings_layout.addRow(inputVolume_label, inputVolume_slider)
        audioSettings_layout.addRow(outputVolume_label, outputVolume_slider)
        audioSettings_group.setLayout(audioSettings_layout)

        
        ### Advanced Settings Section
        # File Location


        # Save settings button 
        save_button = QPushButton("Save Settings")
        save_button.clicked.connect(self.save_settings)

        # Layout
        layout.addWidget(general_group)
        layout.addWidget(videoSettings_group)
        layout.addWidget(audioSettings_group)
        layout.addWidget(save_button)
        
        # Set layout
        self.setLayout(layout)  
           
    '''
    Runs when you click Save Settings button
    '''
    def save_settings(self):
        # get inputed values
        resolution = self.resolution_combobox.currentText()
        language = self.language_combobox.currentText()
        dateFormat = self.dateFormat_combobox.currentText()
        timeFormat = self.timeFormat_combobox.currentText()
        notifications = self.notifications_checkbox.isChecked()
        videoDevice = self.videoDevice_combobox.currentText()
        inputDevice = self.inputDevice_combobox.currentText()
        outputDevice = self.outputDevice_combobox.currentText()
        inputVolume = self.inputVolume_slider.value()
        outputVolume = self.outputVolume_slider.value()

        # Compare old and new values to see what needs to be updated
        with open(SETTING_FILE, "r", encoding="utf-8") as f:
            settings = json.load(f)[0]

        if settings['resolution'] != resolution:
            settings["resolution"] = resolution
            self.main_window.update_res(resolution)
        if settings["language"] != language:
            settings["language"] = language
            # not yet implemented 
        if settings["dateFormat"] != dateFormat:
            settings["dateFormat"] = dateFormat
            # awaiting time
        if settings["timeFormat"] != timeFormat:
            settings["timeFormat"] = timeFormat
            self.home_tab.update_timeFormat(timeFormat)
        if settings["notifications"] != notifications:
            settings["notifications"] = notifications
            # not yet implemented
        if settings["videoDevice"] != videoDevice:
            settings["videoDevice"] = videoDevice
        if settings["inputDevice"] != inputDevice:
            settings["inputDevice"] = inputDevice # Devices need to be corresponded to device index
        if settings["outputDevice"] != outputDevice:
            settings["outputDevice"] = outputDevice
        if settings["inputVolume"] != inputVolume:
            settings["inputVolume"] = inputVolume
        if settings["outputVolume"] != outputVolume:
            settings["outputVolume"] = outputVolume

        with open(SETTING_FILE, "w", encoding="utf-8") as f:
            json.dump([settings], f, indent=4)

        QMessageBox.information(self, "Settings", f"Settings saved.")
