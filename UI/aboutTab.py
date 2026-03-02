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
from PySide6.QtWidgets import (QTextEdit, QLabel, QVBoxLayout, QWidget)

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