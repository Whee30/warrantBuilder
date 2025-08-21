import sys
from PyQt6.QtWidgets import QApplication, QListView, QFormLayout, QMessageBox, QSizePolicy, QCheckBox, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QGridLayout, QTabWidget, QLineEdit, QComboBox, QPushButton, QLabel, QTextEdit, QFrame, QScrollArea, QDateEdit
from PyQt6.QtCore import Qt, QDate, QDir, QModelIndex, QEvent
from PyQt6.QtGui import QFileSystemModel
from docxtpl import DocxTemplate
import os
from datetime import datetime
import json
import glob
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
    "program":"./warrantBuilder.exe",
    "verbiage":"./sources/cv_sources.json",
    "template":"./sources/skeleton.docx",
    "settings":"./sources/settings.json",
    "local_versions":"./sources/local_version.json"
}

no_cache_headers = {
    'Cache-Control': 'no-cache'
}

remote_hash_list = f"https://raw.githubusercontent.com/Whee30/warrantBuilder/refs/heads/main/sources/hash_list.json?nocache={int(time.time())}"
remote_version_list =f"https://raw.githubusercontent.com/Whee30/warrantBuilder/refs/heads/main/sources/remote_version.json?nocache={int(time.time())}"
local_version_list = "./sources/local_version.json"

h_response = requests.get(remote_hash_list, headers=no_cache_headers)
hash_references = h_response.json()

v_response = requests.get(remote_version_list, headers=no_cache_headers)
remote_versions = v_response.json()

# Load local version numbers
with open(local_version_list, 'r') as file:
    local_versions = json.load(file)

# The files needing hash validation
remote_files = {
    "program":"https://raw.githubusercontent.com/Whee30/warrantBuilder/refs/heads/main/warrantBuilder.py",
    "verbiage":"https://raw.githubusercontent.com/Whee30/warrantBuilder/refs/heads/main/sources/cv_sources.json",
    "template":"https://github.com/Whee30/warrantBuilder/raw/refs/heads/main/sources/skeleton.docx"
    "settings":"./sources/settings.json",
    "local_versions":"./sources/local_version.json"
}

local_files = {
    "program":"./warrantBuilder.exe",
    "verbiage":"./sources/cv_sources.json",
    "template":"./sources/skeleton.docx",
    "settings":"./sources/settings.json",
    "local_versions":"./sources/local_versions.json"
}

class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Warrant Builder - Update Utility v0.1")
        self.setFixedWidth(500)

        #####################
        # ESTABLISH WIDGETS #
        #####################

        main_label = QLabel("Warrant Builder Update Utility 0.1")

        self.current_program = QLineEdit()
        self.current_program.setReadOnly(True)

        self.current_verbiage = QLineEdit()
        self.current_verbiage.setReadOnly(True)

        self.current_template = QLineEdit()
        self.current_template.setReadOnly(True)

        self.remote_program = QLineEdit()
        self.remote_program.setReadOnly(True)

        self.remote_verbiage = QLineEdit()
        self.remote_verbiage.setReadOnly(True)

        self.remote_template = QLineEdit()
        self.remote_template.setReadOnly(True)

        self.submit_button = QPushButton()
        self.submit_button.setText("Upgrade!")
        self.submit_button.setFixedWidth(100)
        self.submit_button.clicked.connect(lambda: run_update())

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

        self.content = QWidget()
        self.content_layout = QHBoxLayout()
        self.content_layout.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)
        self.content.setLayout(self.content_layout)

        self.left_side = QWidget()
        self.left_side_layout = QVBoxLayout()
        self.left_side_layout.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)
        self.left_side.setLayout(self.left_side_layout)

        self.right_side = QWidget()
        self.right_side_layout = QVBoxLayout()
        self.right_side_layout.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)
        self.right_side.setLayout(self.right_side_layout)

        self.button_row = QWidget()
        self.button_row_layout = QHBoxLayout()
        self.button_row_layout.setAlignment(Qt.AlignmentFlag.AlignCenter | Qt.AlignmentFlag.AlignTop)
        self.button_row.setLayout(self.button_row_layout)
        self.button_row_layout.setSpacing(20)

        #######################
        # Add widgets to main #
        #######################

        self.main_layout.addWidget(self.content)

        self.content_layout.addWidget(self.left_side)
        self.content_layout.addWidget(self.right_side)

        self.main_layout.addWidget(self.button_row)

        self.left_side_layout.addWidget(self.current_program)
        self.left_side_layout.addWidget(self.current_verbiage)
        self.left_side_layout.addWidget(self.current_template)

        self.right_side_layout.addWidget(self.remote_program)
        self.right_side_layout.addWidget(self.remote_verbiage)
        self.right_side_layout.addWidget(self.remote_template)

        self.button_row_layout.addWidget(self.submit_button)
        self.button_row_layout.addWidget(quit_button)

        self.setCentralWidget(self.main)

        #######################
        # Establish Functions #
        #######################

        def compare_version(k):
            if local_versions[k] >= remote_versions[k]:
                print("The versions are equal or the local version is newer")
            elif local_versions[k] < remote_versions[k]:
                print("The remote version is newer")
                compare_hashes(k)
            #print(f"Local: {local_versions[k]} - Remote: {remote_versions[k]}")

        def compare_hashes(k):
            hash_to_compare = hash_references[k]
            remote_sha256_hash = hashlib.sha256()
            response = requests.get(remote_files[k], headers=no_cache_headers)
            remote_sha256_hash.update(response.content)
            if remote_sha256_hash.hexdigest() == hash_to_compare:
                replace_file(k)
                print(f"The calculated hash and the comparison hash for {k} matched, it was replaced")
            elif remote_sha256_hash.hexdigest() != hash_to_compare:
                print(f"The hashes don't match! The {k} file was not replaced.")
                print(f"{k} calculated: {remote_sha256_hash.hexdigest()}")
                print(f"{k} Stored:     {hash_to_compare}")

        def replace_file(k):
            file_response = requests.get(remote_files[k], headers=no_cache_headers)
            with open(local_files[k], 'wb') as file:
                file.write(file_response.content)
            # update the version number now
            local_versions[k] = remote_versions[k]
            with open(local_version_list, 'w') as file:
                json.dump(local_versions, file, indent=4)
            print(f"{k} was updated.")

        def run_update():
            for k, v in local_versions.items():
                if v < remote_versions[k]:
                    compare_hashes(k)

        def initial_processing():
            # Check for required directories and files        
            if os.path.exists('./output') == False:
                os.mkdir('./output')
            if os.path.exists('./sources') == False:
                os.mkdir("./sources")
            if os.path.exists('./sources/previousWarrants') == False:
                os.mkdir('./sources/previousWarrants')        
            if os.path.exists('./sources/TandE.txt') == False:
                with open("./sources/TandE.txt", "w") as file:
                    file.write("This is where you include your relevant experience")
            for k, v in required_items.items():
                if os.path.exists(v) == False:
                    compare_hashes(k)

            for k in local_versions.keys():
                current_widget = getattr(self, f"current_{k}")
                remote_widget = getattr(self, f"remote_{k}")
                current_widget.setText(f"Current {k} version: {str(local_versions[k])}")
                remote_widget.setText(f"Remote {k} version: {str(remote_versions[k])}")


        initial_processing()
app = QApplication(sys.argv)

#pyi_splash.close()
window = MainWindow()
window.show()
app.setStyle('Fusion')
app.exec()