"""
Project: Lightwave Communications
Authors: Ian MacDougall, Gage Pavia
Date Created: 16 December 2025
Last Modified: 16 December 2025
File Description: Class of Lightwaves Comunications
Upadte Description:
Repository: https://github.com/IanDMacDougall/Lightwave
"""

from utilities import (get_scheduled_calls, load_settings)
from UI.homeTab import HomeTab
from UI.scheduleTab import ScheduleCallTab
from UI.settingsTab import SettingsTab
from UI.notificationsTab import NotificationsTab
from UI.contactsTab import ContactsTab
from UI.historyTab import HistoryTab, AnalyticsTab
from UI.aboutTab import AboutTab

from PySide6.QtWidgets import QTabWidget, QMainWindow

class LightwaveCommunications(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Lightwave Communications")
        settings = load_settings()
        resolutions = tuple(map(int, settings['resolution'].strip("()").split(",")))
        self.setGeometry(100, 100, resolutions[0], resolutions[1])

        # Main Tab widget
        self.tabs = QTabWidget(self)
        self.setCentralWidget(self.tabs)

        # Create instance of tabs
        self.home_tab = HomeTab()
        self.history_tab = HistoryTab()

        # Add tabs
        self.tabs.addTab(self.home_tab, "Home")
        self.tabs.addTab(ScheduleCallTab(self.home_tab), "Schedule Call")
        self.tabs.addTab(SettingsTab(HomeTab=self.home_tab, parent=self), "Settings")
        self.tabs.addTab(NotificationsTab(get_scheduled_calls()), "Notifications")
        self.tabs.addTab(ContactsTab(), "Contacts")
        self.tabs.addTab(self.history_tab, "History")
        self.tabs.addTab(AnalyticsTab(), "Analytics")
        self.tabs.addTab(AboutTab(), "About")

        # Input settigns for host / join

    def update_res(self, updatedResolution):
        resolutions = tuple(map(int, updatedResolution.strip("()").split(",")))
        self.resize(resolutions[0], resolutions[1])