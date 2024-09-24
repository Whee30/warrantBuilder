import sys
from PyQt6.QtWidgets import QApplication, QMessageBox, QStyleFactory, QCheckBox, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QGridLayout, QTabWidget, QLineEdit, QComboBox, QPushButton, QLabel, QTextEdit, QFrame, QCalendarWidget, QScrollArea, QDateEdit
from PyQt6.QtGui import QPalette, QColor
from PyQt6.QtCore import Qt, QDate
from pathlib import Path
from docxtpl import DocxTemplate
from qt_material import apply_stylesheet
import os

# This script functions. It can likely be cleaned up quite a bit, but it works.

# Variable definition time!
# Where the source template file lives
templatePath = "./sources/skeleton.docx"

# Output file variable
docOut = DocxTemplate(templatePath)

class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        # Establish the window geometry
        self.setWindowTitle("Warrant Builder v2.0")

        # Minimum size is proving problematic with spacing. Disabling until I figure it out.
        self.setFixedSize(810,800)
        #self.setMaximumHeight(400)

        # Establish the tab position and settings
        tabs = QTabWidget()
        tabs.setTabPosition(QTabWidget.TabPosition.North)
        tabs.setMovable(True)

        # Declare values dictionary
        self.v = {}

        # Establish individual widgets as dictionary entries
        self.v['CASENUM'] = QLineEdit()
        self.v['CASENUM'].setPlaceholderText("Enter Case number")
        self.v['CASENUM'].setFixedWidth(150)

        self.v['RANK'] = QComboBox()
        self.v['RANK'].addItems(["Ofc.","Det.","Sgt."])
        self.v['RANK'].setFixedWidth(100)

        self.v['NAME'] = QLineEdit()
        self.v['NAME'].setFixedWidth(150)
        self.v['NAME'].setPlaceholderText("Name: 'F. Cook'")
        
        self.v['BADGE'] = QLineEdit()
        self.v['BADGE'].setPlaceholderText("Badge: 'V208'")
        self.v['BADGE'].setMaxLength(6)
        self.v['BADGE'].setFixedWidth(100)

        self.v['COURT'] = QComboBox()
        self.v['COURT'].addItems([
            "Oro Valley Magistrate Court",
            "Pima County Justice Court",
            "Pima County Superior Court"])
        self.v['COURT'].setFixedWidth(200)

        self.v['JUDGE'] = QLineEdit()
        self.v['JUDGE'].setFixedWidth(200)
        self.v['JUDGE'].setPlaceholderText("Judge's Name")

        self.v['PERSON'] = QTextEdit()
        self.v['PERSON'].setPlaceholderText("Persons information including DOB etc.")
        self.v['PERSON'].setFixedSize(250,150)

        self.v['PLACE'] = QTextEdit()
        self.v['PLACE'].setPlaceholderText("Location, including description and characteristics.")
        self.v['PLACE'].setFixedSize(250,150)

        self.v['VEHICLE'] = QTextEdit()
        self.v['VEHICLE'].setPlaceholderText("Vehicle, including license plate and VIN")
        self.v['VEHICLE'].setFixedSize(250,150)

        self.v['PROPERTY'] = QTextEdit()
        self.v['PROPERTY'].setPlaceholderText("List specific property sought. Choose items from the 'common verbiage' tab, if relevant.")
        self.v['PROPERTY'].setFixedSize(763,200)

        self.v['CRIMES'] = QTextEdit()
        self.v['CRIMES'].setPlaceholderText("List crimes investigated, including statute")
        self.v['CRIMES'].setFixedSize(450,120)

        self.v['DATE1'] = QDateEdit()
        self.v['DATE1'].setCalendarPopup(True)
        self.v['DATE1'].setDate(QDate().currentDate())

        rangeCheck = QCheckBox("Enable Date Range?")
        rangeCheck.clicked.connect(self.date_range_enable)

        self.v['DATE2'] = QDateEdit()
        self.v['DATE2'].setCalendarPopup(True)
        self.v['DATE2'].setDate(QDate().currentDate())
        self.v['DATE2'].setDisabled(True)

        self.v['AFFIDAVIT'] = QTextEdit()
        self.v['AFFIDAVIT'].setPlaceholderText("Enter Affidavit details here")
        self.v['AFFIDAVIT'].setFixedSize(763,300)

        # r(0)-r(5), reasons for warrant
        self.r = [
            "Were stolen or embezzled",
            "Were used as a means for committing a public offense.",
            "Is being possessed with the intent to use it as a means of committing a public offense.",
            "Are in the possession of _______________, to whom it was delivered for the purpose of concealing it from being discovere.",
            "Consists of any item or constitutes any evidence which tends to show that a public offense has been committed,"
            " or tends to show that a particular person committed the public offense.",
            "The person sought is the subject of an outstanding warrant, which offense occurred on or about the ___ day of ______, ____"
        ]

        self.v['REASON0'] = QCheckBox()
        self.v['REASON1'] = QCheckBox()
        self.v['REASON2'] = QCheckBox()
        self.v['REASON3'] = QCheckBox()
        self.v['REASON4'] = QCheckBox()
        self.v['REASON5'] = QCheckBox()

        self.v['DAYTIME'] = QCheckBox()
        self.v['DAYTIME'].setText("In the Daytime, excluding the time period between 10pm and 6:30am.")
        
        self.v['NIGHTTIME'] = QCheckBox()
        self.v['NIGHTTIME'].setText("In the night time, for the following reason(s):")
        self.v['NIGHTTIME'].clicked.connect( self.night_time_click )

        self.v['NIGHTJUSTIFY'] = QTextEdit()
        self.v['NIGHTJUSTIFY'].setPlaceholderText("Enter night time justification")
        self.v['NIGHTJUSTIFY'].setFixedSize(300,120)
        self.v['NIGHTJUSTIFY'].setDisabled(True)


        divider = QFrame()
        divider.setFrameShape(QFrame.Shape.HLine)
        divider.setFrameShadow(QFrame.Shadow.Sunken)
        divider.setFixedWidth(763)

        submitButton = QPushButton()
        submitButton.setText("Submit")
        submitButton.setProperty('class', 'success')
        submitButton.clicked.connect( self.submitForm )

        clearButton = QPushButton()
        clearButton.setText("Reset Form")
        clearButton.setProperty('class', 'danger')
        clearButton.clicked.connect( self.clearForm )

        quitButton = QPushButton()
        quitButton.setText("Quit Program")
        quitButton.setProperty('class', 'danger')
        quitButton.clicked.connect( self.quitForm )



# multi line rich text editing - QTextEdit

        # Establish the layouts of the tabs
        mainTab = QWidget()
        mainTabLayout = QVBoxLayout()
        mainTabLayout.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)
        mainTab.setLayout(mainTabLayout)
        mainScroll = QScrollArea()
        mainScroll.setWidget(mainTab)
        mainScroll.setWidgetResizable(True)

        infoWidget = QWidget()
        infoLayout = QHBoxLayout()
        infoLayout.setContentsMargins(0,0,0,0)
        infoLayout.setAlignment(Qt.AlignmentFlag.AlignLeft)
        infoWidget.setLayout(infoLayout)
        
        courtWidget = QWidget()
        courtLayout = QHBoxLayout()
        courtLayout.setContentsMargins(0,0,0,0)
        courtWidget.setLayout(courtLayout)
        courtLayout.setAlignment(Qt.AlignmentFlag.AlignLeft)
        
        locWidget = QWidget()
        locLayout = QGridLayout()
        locLayout.setContentsMargins(0,0,0,0)
        locLayout.setAlignment(Qt.AlignmentFlag.AlignLeft)
        locWidget.setLayout(locLayout)

        crimeWidget = QWidget()
        crimeLayout = QHBoxLayout()
        crimeLayout.setContentsMargins(0,0,0,0)
        crimeLayout.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)
        crimeWidget.setLayout(crimeLayout)

        crimeCol1 = QWidget()
        crimeCol1Layout = QVBoxLayout()
        crimeCol1Layout.setContentsMargins(0,0,0,0)
        crimeCol1Layout.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)
        crimeCol1.setLayout(crimeCol1Layout)
        crimeCol1.setFixedWidth(470)
        crimeCol2 = QWidget()
        crimeCol2Layout = QVBoxLayout()
        crimeCol2Layout.setContentsMargins(0,0,0,0)
        crimeCol2Layout.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)
        crimeCol2.setLayout(crimeCol2Layout)
        
        reasonWidget = QWidget()
        reasonLayout = QGridLayout()
        reasonLayout.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)
        reasonWidget.setLayout(reasonLayout)
        reasonWidget.setMaximumWidth(770)

        buttonWidget = QWidget()
        buttonLayout = QHBoxLayout()
        buttonWidget.setLayout(buttonLayout)

        verbiageTab = QWidget()
        verbiageTabLayout = QGridLayout()
        verbiageTab.setLayout(verbiageTabLayout) 

        # Add widgets to tabs
        mainTabLayout.addWidget(infoWidget)

        infoLayout.addWidget(QLabel("Rank:"))
        infoLayout.addWidget(self.v['RANK'])
        infoLayout.addWidget(QLabel("Name:"))
        infoLayout.addWidget(self.v['NAME'])
        infoLayout.addWidget(QLabel("Badge:"))
        infoLayout.addWidget(self.v['BADGE'])
        infoLayout.addWidget(QLabel("Case Number:"))
        infoLayout.addWidget(self.v['CASENUM'])
        infoLayout.addStretch()

        mainTabLayout.addWidget(courtWidget)

        courtLayout.addWidget(QLabel("Court:"))
        courtLayout.addWidget(self.v['COURT'])
        courtLayout.addWidget(QLabel("Judge's Name:"))
        courtLayout.addWidget(self.v['JUDGE'])
        courtLayout.addStretch()

        mainTabLayout.addWidget(locWidget)
        
        locLayout.addWidget(QLabel("In Possession Of:"), 0, 0)
        locLayout.addWidget(QLabel("On Premises:"), 0, 1)
        locLayout.addWidget(QLabel("In Vehicle(s):"), 0, 2)
        locLayout.addWidget(self.v['PERSON'], 1, 0)
        locLayout.addWidget(self.v['PLACE'], 1, 1)
        locLayout.addWidget(self.v['VEHICLE'], 1, 2)
        
        mainTabLayout.addWidget(QLabel("Property Sought:"))
        mainTabLayout.addWidget(self.v['PROPERTY'])

        mainTabLayout.addWidget(reasonWidget)

        reasonLayout.addWidget(self.v['REASON0'],0,0)
        reasonLayout.addWidget(QLabel(self.r[0]),0,1)
        reasonLayout.addWidget(self.v['REASON1'],1,0)
        reasonLayout.addWidget(QLabel(self.r[1]),1,1)
        reasonLayout.addWidget(self.v['REASON2'],2,0)
        reasonLayout.addWidget(QLabel(self.r[2]),2,1)
        reasonLayout.addWidget(self.v['REASON3'],3,0)
        reasonLayout.addWidget(QLabel(self.r[3]),3,1)
        reasonLayout.addWidget(self.v['REASON4'],4,0)
        reasonLayout.addWidget(QLabel(self.r[4]),4,1)
        reasonLayout.addWidget(self.v['REASON5'],5,0)
        reasonLayout.addWidget(QLabel(self.r[5]),5,1)

        mainTabLayout.addWidget(divider)

        mainTabLayout.addWidget(crimeWidget)

        crimeLayout.addWidget(crimeCol1)
        crimeCol1Layout.addWidget(QLabel("Crimes Investigated:"))
        crimeCol1Layout.addWidget(self.v['CRIMES'])

        crimeLayout.addWidget(crimeCol2)
        crimeCol2Layout.addWidget(QLabel("Occurred on:"))
        crimeCol2Layout.addStretch()
        crimeCol2Layout.addWidget(self.v['DATE1'])
        crimeCol2Layout.addWidget(rangeCheck)
        crimeCol2Layout.addWidget(QLabel("For a range, choose an end date:"))
        crimeCol2Layout.addWidget(self.v['DATE2'])
        crimeCol2Layout.addStretch()

        mainTabLayout.addWidget(QLabel("Affidavit/Probable Cause:"))
        mainTabLayout.addWidget(self.v['AFFIDAVIT'])    
    
        mainTabLayout.addWidget(QLabel("I am seeking to serve this warrant:"))

        mainTabLayout.addWidget(self.v['DAYTIME'])
        mainTabLayout.addWidget(self.v['NIGHTTIME'])
        mainTabLayout.addWidget(self.v['NIGHTJUSTIFY'])

        mainTabLayout.addWidget(buttonWidget)


        buttonLayout.addWidget(submitButton)
        buttonLayout.addWidget(clearButton)
        buttonLayout.addWidget(quitButton)

        mainTabLayout.addStretch()

        # Add tabs
        tabs.addTab(mainScroll, "Main Tab")
        tabs.addTab(verbiageTab, "Verbiage Tab")

        self.setCentralWidget(tabs)
    
    def date_range_enable(self, i):
        print(i)
        if i == True:
            self.v['DATE2'].setDisabled(False)
        elif i == False:
            self.v['DATE2'].setDisabled(True)
    
    def night_time_click(self, i):
        print(i)
        if i == True:
            self.v['NIGHTJUSTIFY'].setDisabled(False)
        elif i == False:
            self.v['NIGHTJUSTIFY'].setDisabled(True)

    def submitForm(self):
        confirmation_box = QMessageBox()
        confirmation_box.setIcon(QMessageBox.Icon.Question)
        confirmation_box.setWindowTitle("Confirm Submission?")
        confirmation_box.setText("Are you sure you want to build the warrant? You cannot go back if you click 'Yes'.")
        confirmation_box.setStandardButtons(QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.Cancel)

        result = confirmation_box.exec()

        
        if result == QMessageBox.StandardButton.Yes:
            # Gather the field input and build a dictionary
            context = {}
            for key, widget in self.v.items():
                if isinstance(self.v[key], QComboBox):
                    context[key] = widget.currentText()
                elif isinstance(self.v[key], QLineEdit | QCheckBox):
                    context[key] = widget.text()
                elif isinstance(self.v[key], QTextEdit):
                    context[key] = widget.toPlainText()
                elif isinstance(self.v[key], QDateEdit):
                    context[key] = widget.date().toString()
                else:
                    print("You haven't supported this type of widget yet")
            docOut.render(context, autoescape=True)
            output_path = f"./output/{self.v['CASENUM'].text()}-report.docx"
            docOut.save(output_path)
            window.close()
        else:
            print("Action Canceled")
    
    def clearForm(self):
        confirmation_box = QMessageBox()
        confirmation_box.setIcon(QMessageBox.Icon.Question)
        confirmation_box.setWindowTitle("Reset Form?")
        confirmation_box.setText("Are you sure you want to reset the form? You cannot go back if you click 'Yes'.")
        confirmation_box.setStandardButtons(QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.Cancel)

        result = confirmation_box.exec()

        if result == QMessageBox.StandardButton.Yes:
            for widget in window.findChildren(QWidget):
                if isinstance(widget, QLineEdit):
                    widget.clear()  # Clear text in QLineEdit
                elif isinstance(widget, QCheckBox):
                    widget.setChecked(False)  # Uncheck QCheckBox
                elif isinstance(widget, QComboBox):
                    widget.setCurrentIndex(0) 
        else:
            print("Action Canceled")
        
    def quitForm(self):
        confirmation_box = QMessageBox()
        confirmation_box.setIcon(QMessageBox.Icon.Question)
        confirmation_box.setWindowTitle("Quit Application?")
        confirmation_box.setText("Are you sure you want to quit the application? You cannot go back if you click 'Yes'.")
        confirmation_box.setStandardButtons(QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.Cancel)

        result = confirmation_box.exec()

        if result == QMessageBox.StandardButton.Yes:
            window.close()
        else:
            print("Action canceled")
        

class Color(QWidget):

    def __init__(self, color):
        super(Color, self).__init__()
        self.setAutoFillBackground(True)

        palette = self.palette()
        palette.setColor(QPalette.ColorRole.Window, QColor(color))
        self.setPalette(palette)


app = QApplication(sys.argv)
apply_stylesheet(app, theme='dark_purple.xml')

window = MainWindow()
window.show()

app.exec()