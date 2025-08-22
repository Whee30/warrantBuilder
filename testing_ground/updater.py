import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QTextEdit
from PyQt6.QtCore import Qt, QTimer
import os
#import pyi_splash
import hashlib
import json
import time
import requests

required_items = {
    "output":"./output",
    "sources":"./sources",
    "previousWarrants":"./sources/previousWarrants",
    "TandE":"./sources/TandE.txt",
    "program":"./warrantBuilder.py",
    "verbiage":"./sources/cv_sources.json",
    "template":"./sources/skeleton.docx",
    "settings":"./sources/settings.json",
}

no_cache_headers = {
    'Cache-Control': 'no-cache'
}

remote_hash_list = f"https://raw.githubusercontent.com/Whee30/warrantBuilder/refs/heads/main/sources/hash_list.json?nocache={int(time.time())}"

h_response = requests.get(remote_hash_list, headers=no_cache_headers)
hash_references = h_response.json()

# The files needing hash validation
remote_files = {
    "program":"https://raw.githubusercontent.com/Whee30/warrantBuilder/refs/heads/main/warrantBuilder.py",
    "verbiage":"https://raw.githubusercontent.com/Whee30/warrantBuilder/refs/heads/main/sources/cv_sources.json",
    "template":"https://github.com/Whee30/warrantBuilder/raw/refs/heads/main/sources/skeleton.docx",
    "settings":"https://raw.githubusercontent.com/Whee30/warrantBuilder/refs/heads/main/sources/settings.json"
}

local_files = {
    "program":"./warrantBuilder.py",
    "verbiage":"./sources/cv_sources.json",
    "template":"./sources/skeleton.docx",
    "settings":"./sources/settings.json"
}

class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Warrant Builder - Update Utility v0.1")
        self.setFixedWidth(500)

        #####################
        # ESTABLISH WIDGETS #
        #####################

        self.main_label = QLabel("Warrant Builder Update Utility")

        self.status_report = QTextEdit()

        self.submit_button = QPushButton()
        self.submit_button.setText("Upgrade!")
        self.submit_button.setFixedWidth(100)
        self.submit_button.clicked.connect(lambda: self.run_update())

        quit_button = QPushButton()
        quit_button.setText("Quit")
        quit_button.setFixedWidth(100)
        quit_button.clicked.connect(QApplication.instance().quit)

        ########################
        # Establish the layout #
        ########################

        self.main = QWidget()
        self.main_layout = QVBoxLayout()
        self.main_layout.setAlignment(Qt.AlignmentFlag.AlignCenter | Qt.AlignmentFlag.AlignTop)
        self.main.setLayout(self.main_layout)

        self.button_row = QWidget()
        self.button_row_layout = QHBoxLayout()
        self.button_row_layout.setAlignment(Qt.AlignmentFlag.AlignCenter | Qt.AlignmentFlag.AlignTop)
        self.button_row.setLayout(self.button_row_layout)
        self.button_row_layout.setSpacing(20)

        #######################
        # Add widgets to main #
        #######################

        self.main_layout.addWidget(self.main_label)

        self.main_layout.addWidget(self.status_report)

        self.main_layout.addWidget(self.button_row)

        self.button_row_layout.addWidget(self.submit_button)
        self.button_row_layout.addWidget(quit_button)

        self.setCentralWidget(self.main)

        #######################
        # Establish Functions #
        #######################

    def compare_hashes(self, k):
        hash_to_compare = hash_references[k]
        remote_sha256_hash = hashlib.sha256()
        response = requests.get(remote_files[k], headers=no_cache_headers)
        remote_sha256_hash.update(response.content)
        if remote_sha256_hash.hexdigest() == hash_to_compare:
            self.replace_file(k)
            print(f"The {k} file was updated.")
        elif remote_sha256_hash.hexdigest() != hash_to_compare:
            print(f"The hashes don't match! Something's wonky in dolphin-town. The {k} file was not replaced.")
            print(f"{k} calculated: {remote_sha256_hash.hexdigest()}")
            print(f"{k} Stored:     {hash_to_compare}")
            self.status_report.append(f"Something went wrong with the {k} file, it was not updated.")

    def replace_file(self, k):
        file_response = requests.get(remote_files[k], headers=no_cache_headers)
        with open(local_files[k], 'wb') as file:
            file.write(file_response.content)

    def run_update(self):
        self.status_report.append("Comparing file versions...")
        for k, v in local_files.items():
            hash_to_compare = hash_references[k]
            local_file_hash = hashlib.sha256()
            with open(v, "rb") as file:
                local_file_hash.update(file.read())
            if local_file_hash.hexdigest() != hash_to_compare:
                self.compare_hashes(k)
        self.status_report.append("All files are up to date!")

    def initial_processing(self):
        self.status_report.append("Checking for all required files...")
        # Check for required directories and files        
        if os.path.exists('./output') == False:
            os.mkdir('./output')
            self.status_report.append("Output directory missing, directory was created.")
        if os.path.exists('./sources') == False:
            os.mkdir("./sources")
            self.status_report.append("sources directory missing, directory was created.")
        if os.path.exists('./sources/previousWarrants') == False:
            os.mkdir('./sources/previousWarrants')
            self.status_report.append("Previous warrants directory missing, directory was created.")      
        if os.path.exists('./sources/TandE.txt') == False:
            with open("./sources/TandE.txt", "w") as file:
                file.write("This is where you include your relevant experience")
            self.status_report.append("Training file was missing, file was created.")
        for k, v in required_items.items():
            if os.path.exists(v) == False:
                self.compare_hashes(k)
                self.status_report.append(f"{k} file was missing, file was downloaded.")
        self.status_report.append("All files are present.")
        
app = QApplication(sys.argv)

#pyi_splash.close()
window = MainWindow()
window.show()
app.setStyle('Fusion')

QTimer.singleShot(0, window.initial_processing)

app.exec()