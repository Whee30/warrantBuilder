import sys
from PyQt6.QtWidgets import QApplication, QAbstractItemView, QListWidgetItem, QStatusBar, QListWidget, QToolBar, QListView, QFormLayout, QMessageBox, QSizePolicy, QCheckBox, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QGridLayout, QTabWidget, QLineEdit, QComboBox, QPushButton, QLabel, QTextEdit, QFrame, QScrollArea, QDateEdit
from PyQt6.QtCore import Qt, QDate, QDir, QEvent, QSize
from PyQt6.QtGui import QFileSystemModel, QAction, QIcon, QKeySequence, QDragMoveEvent
from docxtpl import DocxTemplate
import os
from datetime import datetime
import json
import glob
import requests
import time
import subprocess
import minisign
import shutil
import tempfile
#import pyi_splash

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Establish the tab position and settings
        self.main = QWidget()
        self.ml = QVBoxLayout(self.main)
        self.setCentralWidget(self.main)     

        self.list_widget = QListWidget()
        self.list_widget.setDragDropMode(QAbstractItemView.DragDropMode.InternalMove)
        self.list_widget.setDragEnabled(True)
        self.list_widget.setAcceptDrops(True)
        self.list_widget.setDropIndicatorShown(True)

        listicle = {'One':"Item One",
                    'Two':"Item Two",
                    'Three':"Item Three",
                    'Four':"Item Four",
                    'Five':"Item Five"}

        for k, v in listicle.items():
            temp_card = QWidget()
            temp_layout = QVBoxLayout(temp_card)
            temp_layout.addWidget(QLabel(f"Task {k}"))
            temp_layout.addWidget(QLabel(f"Description {v}"))

            k = QListWidgetItem()
            k.setSizeHint(temp_card.sizeHint())

            self.list_widget.addItem(k)
            self.list_widget.setItemWidget(k, temp_card)

        self.ml.addWidget(self.list_widget)

        self.button_order = QPushButton("What order?")
        self.button_order.clicked.connect(self.declare_order)

        self.ml.addWidget(self.button_order)

    def declare_order(self):
        for i in range(self.list_widget.count()):
            print(self.list_widget.item(i).text())



         
app = QApplication(sys.argv)

#pyi_splash.close()
window = MainWindow()
window.show()
app.setStyle('Fusion')

app.exec()
