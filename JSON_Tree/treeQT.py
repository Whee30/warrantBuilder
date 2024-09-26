import sys
from PyQt6.QtWidgets import QApplication, QTreeWidget, QTreeWidgetItem, QTreeView
from cvSources import General, ICAC, Electronics
import json

import sys
from PyQt6.QtWidgets import QApplication, QFormLayout, QMessageBox, QStyleFactory, QCheckBox, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QGridLayout, QTabWidget, QLineEdit, QComboBox, QPushButton, QLabel, QTextEdit, QFrame, QCalendarWidget, QScrollArea, QDateEdit
from PyQt6.QtGui import QPalette, QColor, QFileSystemModel
from PyQt6.QtCore import Qt, QDate
from pathlib import Path
from docxtpl import DocxTemplate
from qt_material import apply_stylesheet
import os
from datetime import datetime

# This script functions. It can likely be cleaned up quite a bit, but it works.

class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        # Establish the window geometry
        self.setWindowTitle("JSON load into Tree View")
        self.setFixedSize(810,800)

        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)
        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)

        self.topicLabel = QPushButton()
        self.topicLabel.setText("ICAC")
        self.topicLabel.setCheckable(True)
        self.topicLabel.clicked.connect( self.expandTopic )

        self.topic2Label = QPushButton()
        self.topic2Label.setText("General")
        self.topic2Label.setCheckable(True)
        self.topic2Label.clicked.connect( self.expandTopic2 )

        self.hLayout = QFormLayout()
        self.hWidget = QWidget()
        self.hWidget.hide()
        self.hWidget.setLayout(self.hLayout)

        self.h2Layout = QFormLayout()
        self.h2Widget = QWidget()
        self.h2Widget.hide()
        self.h2Widget.setLayout(self.hLayout)

        self.cb1 = QCheckBox()
        self.cb1L = QLabel("Checkbox label")
        self.cb2 = QCheckBox()
        self.cb2L = QLabel("Checkbox label 2")
        self.cb3 = QCheckBox()
        self.cb3L = QLabel("Checkbox label 3")

        self.c2b1 = QCheckBox()
        self.c2b1L = QLabel("Checkbox label")
        self.c2b2 = QCheckBox()
        self.c2b2L = QLabel("Checkbox label 2")
        self.c2b3 = QCheckBox()
        self.c2b3L = QLabel("Checkbox label 3")

        self.checkTopic = QCheckBox()
        self.checkTopic.setText("This is the checkbox text")

        layout.addWidget(QLabel("This will test loading a JSON file into lists."))
        layout.addWidget(self.topicLabel)
        
        layout.addWidget(self.hWidget)
        self.hLayout.addRow(self.cb1, self.cb1L)
        self.hLayout.addRow(self.cb2, self.cb2L)
        self.hLayout.addRow(self.cb3, self.cb3L)

        layout.addWidget(self.topic2Label)

        layout.addWidget(self.h2Widget)
        self.h2Layout.addRow(self.c2b1, self.c2b1L)
        self.h2Layout.addRow(self.c2b2, self.c2b2L)
        self.h2Layout.addRow(self.c2b3, self.c2b3L)

    def expandTopic(self, checked):
        if checked == True:
            self.hWidget.show()
        elif checked == False:
            self.hWidget.hide()

    def expandTopic2(self, checked):
        if checked == True:
            self.h2Widget.show()
        elif checked == False:
            self.h2Widget.hide()



app = QApplication(sys.argv)

window = MainWindow()
window.show()

app.exec()