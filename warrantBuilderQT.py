import sys
from PyQt6.QtWidgets import QApplication, QMessageBox, QStyleFactory, QCheckBox, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QGridLayout, QTabWidget, QLineEdit, QComboBox, QPushButton, QLabel, QTextEdit, QFrame, QCalendarWidget, QScrollArea, QDateEdit
from PyQt6.QtGui import QPalette, QColor
from PyQt6.QtCore import Qt, QDate
from pathlib import Path
from docxtpl import DocxTemplate
from qt_material import apply_stylesheet
import os

# This script functions. It can likely be cleaned up quite a bit, but it works.

class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()


        
        self.TandESrc = open('./sources/TandE.txt').read()

        # Where the source template file lives
        self.templatePath = "./sources/skeleton.docx"

        # Output file variable
        self.docOut = DocxTemplate(self.templatePath)

        # The default county for the warrants
        self.county = 'Pima'

        # Establish the "On or Between" verbiage for offense date
        self.onOrBetween = ''

        # Day or night warrant service
        self.serviceTime = (
            "in the daytime (excluding the time period between 10:00 p.m and 6:30 a.m)",
            "in the nighttime, good cause having been shown."
        )

        self.serviceIndex = 0

        # This variable holds the common verbiage additions
        self.vHolder = ''''''
            
        # Hidden values from previous form that need addressing
        
        #key='PROPERTY_REASONS'
        #key='TRAININGEXPERIENCE'
        #key='SERVICETIME'
        #key='COMMON_VERBIAGE'
        #key='ON_OR_BETWEEN'
        #key='DAY_NUMBER'
        #key='MONTH'
        #key='YEAR'
        

        # Check for required directories
        '''
        if os.path.exists('./output') == False:
            os.mkdir('./output')
            Sg.popup("Output directory was missing, created new output directory at warrantBuilder/output/")
        if os.path.exists('./sources') == False:
            Sg.popup("You are missing the WarrantBuilder/sources/ directory! You need to re-download the package or run the update program if you have it. This program will now exit.")        
        '''
            
        # Establish the window geometry
        self.setWindowTitle("Warrant Builder v2.0")

        # Minimum size is proving problematic with spacing. Disabling until I figure it out.
        self.setFixedSize(810,800)
        #self.setMaximumHeight(400)

        # This variable will hold the property reason checkbox values
        self.rHolder = ''''''

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
        self.v['DATE1'].setButtonSymbols(self.v['DATE1'].ButtonSymbols.NoButtons)

        self.rangeCheck = QCheckBox("Enable Date Range?")
        self.rangeCheck.clicked.connect(self.date_range_enable)

        self.v['DATE2'] = QDateEdit()
        self.v['DATE2'].setCalendarPopup(True)
        self.v['DATE2'].setDate(QDate().currentDate())
        self.v['DATE2'].setButtonSymbols(self.v['DATE2'].ButtonSymbols.NoButtons)
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

        for index, item in enumerate(self.r):
            self.v[f'REASON{index}'] = QCheckBox()
            self.v[f'REASON{index}'].setText(item)

        #self.v['REASON0'] = QCheckBox()
        #self.v['REASON0'].setText(self.r[0])
        #self.v['REASON1'] = QCheckBox()
        #self.v['REASON2'] = QCheckBox()
        #self.v['REASON3'] = QCheckBox()
        #self.v['REASON4'] = QCheckBox()
        #self.v['REASON5'] = QCheckBox()

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
        clearButton.setProperty('class', 'warning')
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

        #mainTabLayout.addWidget(reasonWidget)

        mainTabLayout.addWidget(self.v['REASON0'])
        #reasonLayout.addWidget(QLabel(self.r[0]),0,1)
        mainTabLayout.addWidget(self.v['REASON1'])
        #reasonLayout.addWidget(QLabel(self.r[1]),1,1)
        mainTabLayout.addWidget(self.v['REASON2'])
        #reasonLayout.addWidget(QLabel(self.r[2]),2,1)
        mainTabLayout.addWidget(self.v['REASON3'])
        #reasonLayout.addWidget(QLabel(self.r[3]),3,1)
        mainTabLayout.addWidget(self.v['REASON4'])
        #reasonLayout.addWidget(QLabel(self.r[4]),4,1)
        mainTabLayout.addWidget(self.v['REASON5'])
        #reasonLayout.addWidget(QLabel(self.r[5]),5,1)

        mainTabLayout.addWidget(divider)

        mainTabLayout.addWidget(crimeWidget)

        crimeLayout.addWidget(crimeCol1)
        crimeCol1Layout.addWidget(QLabel("Crimes Investigated:"))
        crimeCol1Layout.addWidget(self.v['CRIMES'])

        crimeLayout.addWidget(crimeCol2)
        crimeCol2Layout.addWidget(QLabel("Occurred on:"))
        crimeCol2Layout.addStretch()
        crimeCol2Layout.addWidget(self.v['DATE1'])
        crimeCol2Layout.addWidget(self.rangeCheck)
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

    # This function will apply the appropriate date suffix "1st", "2nd", "3rd", "4th" etc.
    def dateSuffix(self, day):
        if 4 <= day <= 20 or 24 <= day <=30:
            return str(day) + 'th'
        elif day == 1 or day == 21 or day == 31:
            return str(day) + 'st'
        elif day == 2 or day == 22:
            return str(day) + 'nd'
        elif day == 3 or day == 23:
            return str(day) + 'rd'

    def submitForm(self):
        confirmation_box = QMessageBox()
        confirmation_box.setIcon(QMessageBox.Icon.Question)
        confirmation_box.setWindowTitle("Confirm Submission?")
        confirmation_box.setText("Are you sure you want to build the warrant? You cannot go back if you click 'Yes'.")
        confirmation_box.setStandardButtons(QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.Cancel)

        result = confirmation_box.exec()

        
        if result == QMessageBox.StandardButton.Yes:
            
            ''' Old block needs adapting
            # One date or a date range
            if values['START_TIME'] == values['END_TIME']:
                values['ON_OR_BETWEEN'] = f"on {values['START_TIME']}"
            elif values['START_TIME'] != "From" and values['END_TIME'] == "To":
                values['ON_OR_BETWEEN'] = f"on {values['START_TIME']}"
            elif values['START_TIME'] == "From" and values['END_TIME'] != "To":
                values['ON_OR_BETWEEN'] = f"on {values['END_TIME']}"
            elif values['START_TIME'] == "From" and values['END_TIME'] == "To":
                values['ON_OR_BETWEEN'] = "OFFENSE DATE NEEDED"
            else:
                values['ON_OR_BETWEEN'] = f"between {values['START_TIME']} and {values['END_TIME']}"
            
            '''
            
            # Gather the field input and build a dictionary
            context = {}
            for key, widget in self.v.items():
                if isinstance(self.v[key], QComboBox):
                    context[key] = widget.currentText()
                elif isinstance(self.v[key], QLineEdit):
                    context[key] = widget.text()
                elif isinstance(self.v[key], QCheckBox):
                    context[key] = widget.text()
                elif isinstance(self.v[key], QTextEdit):
                    context[key] = widget.toPlainText()
                elif isinstance(self.v[key], QDateEdit):
                    # Not needed?
                    context[key] = widget.date().toString() 
                    context[f'{key}DAY_NUMBER'] = self.dateSuffix(widget.date().day())
                    context[f'{key}MONTH'] = widget.date().toString('MMMM')
                    context[f'{key}YEAR'] = widget.date().year()
                    # Prints the formatted date to check the above function
                    #print("The date you entered was " + context[f'{key}MONTH'] + ' ' + context[f'{key}DAY_NUMBER'] + ', ' + str(context[f'{key}YEAR']))
                else:
                    print("You haven't supported this type of widget yet")

                ''' This block will establish if checkboxes are checked. This is where distinguising daytime and nighttime from reasons and verbiage is important.
                if self.v[key].isChecked() == True:
                    self.rHolder = self.rHolder + widget.text() + '\n\n'
                '''

            #self.docOut.render(context, autoescape=True)
            #self.output_path = f"./output/{self.v['CASENUM'].text()}-warrant.docx"
            #self.docOut.save(self.output_path)

            # Confirmation QMessageBox()
            #messageComplete = QMessageBox()
            #messageComplete.setIcon(QMessageBox.Icon.Information)
            #messageComplete.setWindowTitle("Warrant Generated Successfully!")
            #messageComplete.setText(f"The warrant was built successfully! It has been saved to warrantBuilder/output/{self.v['CASENUM'].text()}-warrant.docx. Don't forget to proofread!")
            #messageComplete.setStandardButtons(QMessageBox.StandardButton.Ok)
            #messageComplete.exec()

            print(self.rHolder)
            # Is the date range box checked?
            outputVar = ''
            if self.rangeCheck.isChecked() == True:
                if self.v['DATE1'].date().toString() == self.v['DATE2'].date().toString():
                    outputVar = f"On "


            # Close window - comment out if second shot at generation is wanted?
            # If keeping window open, consider checking filename to see if exists and iterate by 1 to avoid crashes
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