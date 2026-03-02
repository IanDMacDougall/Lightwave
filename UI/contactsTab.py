"""
Project: Lightwave Communications
Authors: Ian MacDougall, Gage Pavia
Date Created: 16 December 2025
Last Modified: 16 December 2025
File Description: Class of Lightwaves Comunications
Upadte Description:
Repository: https://github.com/IanDMacDougall/Lightwave
"""

import csv

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (QVBoxLayout, QTableWidget, QHeaderView, QPushButton, QLineEdit, QDialog,
                               QFormLayout, QDialogButtonBox, QTableWidgetItem, QMessageBox, QFileDialog, QWidget)

from utilities import (CONTACTS_FILE, save_data, load_data)

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
