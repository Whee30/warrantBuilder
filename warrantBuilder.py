import sys
from PyQt6.QtWidgets import QApplication, QFormLayout, QMessageBox, QSizePolicy, QCheckBox, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QGridLayout, QTabWidget, QLineEdit, QComboBox, QPushButton, QLabel, QTextEdit, QFrame, QScrollArea, QDateEdit
from PyQt6.QtCore import Qt, QDate
from pathlib import Path
from docxtpl import DocxTemplate
import os
from datetime import datetime
import importlib.util

#from sources.cvSources import General, ICAC, Electronics, Drugs, Guns

def load_module_from_path(module_name, module_path):
    spec = importlib.util.spec_from_file_location(module_name, module_path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    spec.loader.exec_module(module)
    return module

# Get the path to the cvSources.py file (relative to the executable)
file_path = './sources/cvSources.py'

sourceList = importlib.util.spec_from_file_location('secondary_script', file_path)
secondary_script = importlib.util.module_from_spec(sourceList)
sourceList.loader.exec_module(secondary_script)

# Access the list
my_list = secondary_script.cvDict

# This script functions. It can likely be cleaned up quite a bit, but it works.
# TO DO:

class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        # Check for required directories and files        
        if os.path.exists('./output') == False:
            os.mkdir('./output')
        if os.path.exists('./sources') == False:
            self.errorOut("sources folder")        
        if os.path.exists('./sources/TandE.txt') == False:
            self.errorOut("TandE.txt")
        if os.path.exists('./sources/skeleton.docx') == False:
            self.errorOut("skeleton.docx")
        if os.path.exists('./sources/cvSources.py') == False:
            self.errorOut("cvSources.py")

        # Training and Experience textfile
        self.TandESrc = open('./sources/TandE.txt', 'r').read()

        # Where the source template file lives
        self.templatePath = "./sources/skeleton.docx"

        # Output file variable
        self.docOut = DocxTemplate(self.templatePath)

        # Declare values dictionary
        self.v = {}

        # This variable will hold the property reason checkbox values
        self.rHolder = ''''''

        # This variable holds the common verbiage additions
        self.vHolder = ''''''    

        # Establish the tab position and settings

        self.setWindowTitle("Warrant Builder v2.0")
        self.setFixedWidth(810)
        self.tabs = QTabWidget()
        self.tabs.setTabPosition(QTabWidget.TabPosition.North)
        self.tabs.setMovable(True)

        
        ##################################################################
        # Establish individual widgets to correspond to template entries #
        ##################################################################

        self.v['CASENUM'] = QLineEdit()
        self.v['CASENUM'].setPlaceholderText("V#####")
        self.v['CASENUM'].setFixedWidth(100)

        self.v['RANK'] = QComboBox()
        self.v['RANK'].addItems(["Ofc.","Det.","Sgt."])
        self.v['RANK'].setFixedWidth(100)

        self.v['NAME'] = QLineEdit()
        self.v['NAME'].setFixedWidth(150)
        self.v['NAME'].setPlaceholderText("'J. Doe'")
        
        self.v['BADGE'] = QLineEdit()
        self.v['BADGE'].setPlaceholderText("V###")
        self.v['BADGE'].setMaxLength(6)
        self.v['BADGE'].setFixedWidth(100)

        self.v['YEARS'] = QLineEdit()
        self.v['YEARS'].setMaxLength(2)
        self.v['YEARS'].setFixedWidth(100)

        self.v['COUNTY'] = QComboBox()
        self.v['COUNTY'].addItems([
            "Pima",
            "Pinal",
            "Maricopa",
            "Apache",
            "Cochise",
            "Coconino",
            "Gila",
            "Graham",
            "Greenlee",
            "La Paz",
            "Mohave",
            "Navajo",
            "Santa Cruz",
            "Yavapai",
            "Yuma"
        ])

        self.v['COURT'] = QComboBox()
        self.v['COURT'].addItems([
            "Oro Valley Magistrate Court",
            "Pima County Justice Court",
            "Pima County Superior Court"])
        self.v['COURT'].setEditable(True)
        self.v['COURT'].setFixedWidth(200)

        self.v['JUDGE'] = QLineEdit()
        self.v['JUDGE'].setFixedWidth(200)
        self.v['JUDGE'].setPlaceholderText("'Hazel'")

        self.v['SUSPECT'] = QTextEdit()
        self.v['SUSPECT'].setPlaceholderText("Person information including DOB etc.")
        self.v['SUSPECT'].setFixedSize(250,150)

        self.v['PREMISES'] = QTextEdit()
        self.v['PREMISES'].setPlaceholderText("Location, including description and characteristics.")
        self.v['PREMISES'].setFixedSize(250,150)

        self.v['VEHICLE'] = QTextEdit()
        self.v['VEHICLE'].setPlaceholderText("Vehicle, including license plate and VIN")
        self.v['VEHICLE'].setFixedSize(250,150)

        self.v['PROPERTY'] = QTextEdit()
        self.v['PROPERTY'].setPlaceholderText("List specific property sought. Choose items from the 'common verbiage' tab, if relevant.")
        self.v['PROPERTY'].setFixedSize(763,200)

        self.v['CRIMES'] = QTextEdit()
        self.v['CRIMES'].setPlaceholderText("List statutes and descriptions")
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
            "Are in the possession of _______________, to whom it was delivered for the purpose of concealing it from being discovered.",
            "Consists of any item or constitutes any evidence which tends to show that a public offense has been committed,"
            " or tends to show that a particular person committed the public offense.",
            "The person sought is the subject of an outstanding warrant, which offense occurred on or about the ___ day of ______, ____"
        ]
        
        self.rCB = []

        # loop the self.r values and build checkboxes for each
        for index, item in enumerate(self.r):
            self.v[f'REASON{index}'] = QCheckBox()
            self.v[f'REASON{index}'].setText(item)

        self.v['TELEPHONIC'] = QCheckBox()
        self.v['TELEPHONIC'].setText("Telephonic Warrant")

        self.v['DAYTIME'] = QCheckBox()
        self.v['DAYTIME'].setText("In the Daytime, excluding the time period between 10pm and 6:30am")
        
        self.v['NIGHTTIME'] = QCheckBox()
        self.v['NIGHTTIME'].setText("In the night time")
        self.v['NIGHTTIME'].clicked.connect( self.night_time_click )

        self.v['NIGHTJUSTIFY'] = QTextEdit()
        self.v['NIGHTJUSTIFY'].setPlaceholderText("Enter night time justification")
        self.v['NIGHTJUSTIFY'].setFixedSize(300,120)
        self.v['NIGHTJUSTIFY'].setHidden(True)

        divider = QFrame()
        divider.setFrameShape(QFrame.Shape.HLine)
        divider.setFrameShadow(QFrame.Shadow.Sunken)
        divider.setFixedWidth(763)

        self.cvCB = []

        submitButton = QPushButton()
        submitButton.setText("Submit")
        submitButton.clicked.connect( self.submitForm )

        clearButton = QPushButton()
        clearButton.setText("Reset Form")
        clearButton.clicked.connect( self.clearForm )

        quitButton = QPushButton()
        quitButton.setText("Quit Program")
        quitButton.clicked.connect( self.quitForm )

        #########################################
        # Establish the layouts of the main tab #
        #########################################

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
        
        caseWidget = QWidget()
        caseLayout = QHBoxLayout()
        caseLayout.setContentsMargins(0,0,0,0)
        caseWidget.setLayout(caseLayout)
        caseLayout.setAlignment(Qt.AlignmentFlag.AlignLeft)

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

        self.rForm = QWidget()
        self.rForm_l = QFormLayout()
        self.rForm_l.setContentsMargins(5,5,5,5)
        self.rForm_l.setVerticalSpacing(10)
        self.rForm_l.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)
        self.rForm.setFixedWidth(770)
        self.rForm.setLayout(self.rForm_l)

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

        buttonWidget = QWidget()
        buttonLayout = QHBoxLayout()
        buttonLayout.setContentsMargins(0,0,0,0)
        buttonLayout.setAlignment(Qt.AlignmentFlag.AlignJustify)
        buttonWidget.setLayout(buttonLayout)
        buttonWidget.setFixedWidth(763)

        self.verbiageTab = QWidget()
        self.verbiageTabLayout = QGridLayout()
        self.verbiageTabLayout.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft)
        self.verbiageTab.setLayout(self.verbiageTabLayout) 
        self.verbiageTab.setMaximumWidth(770)

        ###########################
        # Add widgets to Main Tab #
        ###########################

        mainTabLayout.addWidget(caseWidget)

        caseLayout.addWidget(QLabel("Case #:"))
        caseLayout.addWidget(self.v['CASENUM'])
        caseLayout.addWidget(self.v['TELEPHONIC'])
        caseLayout.addWidget(QLabel("               Fill out all boxes that are needed for your warrant. Proofread the final product."))
        caseLayout.addStretch()

        mainTabLayout.addWidget(infoWidget)

        infoLayout.addWidget(QLabel("Rank:"))
        infoLayout.addWidget(self.v['RANK'])
        infoLayout.addWidget(QLabel("Name:"))
        infoLayout.addWidget(self.v['NAME'])
        infoLayout.addWidget(QLabel("Badge:"))
        infoLayout.addWidget(self.v['BADGE'])
        infoLayout.addWidget(QLabel("Years On:"))
        infoLayout.addWidget(self.v['YEARS'])

        infoLayout.addStretch()

        mainTabLayout.addWidget(courtWidget)

        courtLayout.addWidget(QLabel("County:"))
        courtLayout.addWidget(self.v['COUNTY'])
        courtLayout.addWidget(QLabel("Court:"))
        courtLayout.addWidget(self.v['COURT'])
        courtLayout.addWidget(QLabel("Judge's Name:"))
        courtLayout.addWidget(self.v['JUDGE'])
        courtLayout.addStretch()

        mainTabLayout.addWidget(locWidget)
        
        locLayout.addWidget(QLabel("In Possession Of:"), 0, 0)
        locLayout.addWidget(QLabel("On Premises:"), 0, 1)
        locLayout.addWidget(QLabel("In Vehicle(s):"), 0, 2)
        locLayout.addWidget(self.v['SUSPECT'], 1, 0)
        locLayout.addWidget(self.v['PREMISES'], 1, 1)
        locLayout.addWidget(self.v['VEHICLE'], 1, 2)
        
        mainTabLayout.addWidget(QLabel("Property Sought:"))
        mainTabLayout.addWidget(self.v['PROPERTY'])

        mainTabLayout.addWidget(QLabel("Which property or things:"))

        mainTabLayout.addWidget(self.rForm)
   
        # Reason loop
        for index, item in enumerate(self.r):
            label = QLabel(item)
            label.adjustSize()
            label.setWordWrap(True)
            checkbox = QCheckBox()
            self.rCB.append(checkbox)
            self.rForm_l.addRow(checkbox, label)
   
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

        ###################################################
        # Establish the layout of the Common Verbiage tab #
        ###################################################

        self.verbiageTab = QWidget()
        self.verbiageTabLayout = QVBoxLayout()
        self.verbiageTabLayout.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)
        self.verbiageTab.setLayout(self.verbiageTabLayout)
        self.verbiageScroll = QScrollArea()
        self.verbiageScroll.setWidget(self.verbiageTab)
        self.verbiageScroll.setWidgetResizable(True)

        # Establish topical buttons, widgets and layouts for common verbiage tab
        # This list will hold the categories which are made into button objects
        self.button_list = []
        # This list will hold the content of the verbiage
        self.verbiage_list = []
        # This list will reference the widgets to be shown or hidden which contain the verbiage itself
        self.hidden_widget_list = []
        self.checkbox_list = []

        self.print_checks = QPushButton()
        self.print_checks.setText('Print Checked Items')
        self.print_checks.clicked.connect(self.submitForm)

        self.verbiageTabLayout.addWidget(QLabel("Click topics to expand/contract - check any that apply. \nAfter selections are made, return to the main tab to finish."))
        self.verbiageTabLayout.addWidget(QLabel("Modify the results to suit your case, if needed."))
        

        for index, item in enumerate(my_list):
            self.button_list.append(item)
            self.button_list[index] = QPushButton()
            self.button_list[index].setText(item[0])
            self.button_list[index].setCheckable(True)
            self.button_list[index].setFixedWidth(200)
            self.button_list[index].clicked.connect( lambda checked, idx=index: self.toggle_widget(checked, idx))
            self.verbiageTabLayout.addWidget(self.button_list[index])


            listVar_w = QWidget()
            listVar_l = QFormLayout()
            listVar_l.setSpacing(10)
            listVar_w.setLayout(listVar_l)
            self.verbiageTabLayout.addWidget(listVar_w)
            listVar_w.setHidden( True )
            self.hidden_widget_list.append(listVar_w)

            for index, listItem in enumerate(item):
                if index > 0:
                    self.verbiage_list.append(listItem)
                    label = QLabel(listItem)
                    label.setWordWrap(True)
                    label.setStyleSheet("border: 2px inset darkGray; border-radius: 10px;")
                    label.setMargin(10)
                    label.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
                    checkbox = QCheckBox()
                    self.checkbox_list.append(checkbox)
                    listVar_l.setSpacing(10)
                    listVar_l.addRow(checkbox, label)

        ###################################################
        # Establish the layout of the Common Verbiage tab #
        ###################################################

        self.trainingTab = QWidget()
        self.trainingTabLayout = QVBoxLayout()
        self.trainingTabLayout.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)
        self.trainingTab.setLayout(self.trainingTabLayout)
        self.trainingScroll = QScrollArea()
        self.trainingScroll.setWidget(self.trainingTab)
        self.trainingScroll.setWidgetResizable(True)

        self.trainingContent = QTextEdit()
        self.trainingContent.setMaximumHeight(300)
        self.trainingContent.setText(self.TandESrc)

        self.trainingSave = QPushButton()
        self.trainingSave.setText("Save Changes")
        self.trainingSave.clicked.connect( self.saveTrainingChanges )

        self.trainingReload = QPushButton()
        self.trainingReload.setText("Reload Current Version")
        self.trainingReload.clicked.connect( self.reloadTrainingContent )

        self.trainingTabLayout.addWidget(QLabel("If you make changes to this, you must save them for the changes to apper in your warrant."))
        self.trainingTabLayout.addWidget(QLabel("This is how your training and Experience will look currently:"))
        self.trainingTabLayout.addWidget(self.trainingContent)
        self.trainingTabLayout.addWidget(self.trainingSave)
        self.trainingTabLayout.addWidget(self.trainingReload)
        self.trainingTabLayout.addStretch()

        # Add tabs
        self.tabs.addTab(mainScroll, "Warrant Content")
        self.tabs.addTab(self.verbiageScroll, "Template Verbiage")
        self.tabs.addTab(self.trainingScroll, "Training and Experience")
        self.setCentralWidget(self.tabs)

    # Toggles the common verbiage topics
    def toggle_widget(self, checked, target):
        if checked:
            self.hidden_widget_list[target].show()
        else:
            self.hidden_widget_list[target].hide()
        #self.verbiageTabLayout.adjustSize()
        self.verbiageScroll.updateGeometry()

    
    # Disables/enables the second dateEdit
    def date_range_enable(self, i):
        if i == True:
            self.v['DATE2'].setDisabled(False)
        elif i == False:
            self.v['DATE2'].setDisabled(True)

    # Disables/enables the night time justification textEdit
    def night_time_click(self, i):
        if i == True:
            self.v['NIGHTJUSTIFY'].setHidden(False)
        elif i == False:
            self.v['NIGHTJUSTIFY'].setHidden(True)

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

    def saveTrainingChanges(self):
        confirmation_box = QMessageBox()
        confirmation_box.setIcon(QMessageBox.Icon.Question)
        confirmation_box.setWindowTitle("Confirm Submission?")
        confirmation_box.setText("Are you sure you want to save these changes to your training and experience? You cannot go back if you click 'Yes'.")
        confirmation_box.setStandardButtons(QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.Cancel)

        result = confirmation_box.exec()
        
        if result == QMessageBox.StandardButton.Yes:
            with open('./sources/TandE.txt', 'w') as file:
                file.write(self.trainingContent.toPlainText())
            self.TandESrc = open('./sources/TandE.txt', 'r').read()

    def reloadTrainingContent(self):
        confirmation_box = QMessageBox()
        confirmation_box.setIcon(QMessageBox.Icon.Question)
        confirmation_box.setWindowTitle("Reload current content?")
        confirmation_box.setText("Are you sure you want to reload the current value of the training and experience file? Any changes that have not been saved will be lost.")
        confirmation_box.setStandardButtons(QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.Cancel)

        result = confirmation_box.exec()
        
        if result == QMessageBox.StandardButton.Yes:
            self.trainingContent.setText(self.TandESrc)

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
                elif isinstance(self.v[key], QLineEdit):
                    context[key] = widget.text()
                elif isinstance(self.v[key], QCheckBox):
                    context[key] = widget.text()
                elif isinstance(self.v[key], QTextEdit):
                    context[key] = widget.toPlainText()
                elif isinstance(self.v[key], QDateEdit):
                    context[key] = widget.date().toString() 
                    context[f'{key}DAY_NUMBER'] = self.dateSuffix(widget.date().day())
                    context[f'{key}MONTH'] = widget.date().toString('MMMM')
                    context[f'{key}YEAR'] = widget.date().year()
                    # Prints the formatted date to check the above function
                    #print("The date you entered was " + context[f'{key}MONTH'] + ' ' + context[f'{key}DAY_NUMBER'] + ', ' + str(context[f'{key}YEAR']))
                else:
                    print("You haven't supported this type of widget yet")
            context['TELEPHONIC'] = self.v['TELEPHONIC'].isChecked()
            # Is the date range box checked? Establish the fully formatted date/date range.
            context['ON_OR_BETWEEN'] = ''
            if self.rangeCheck.isChecked() == True:
                if self.v['DATE1'].date().toString() == self.v['DATE2'].date().toString():
                    context['ON_OR_BETWEEN'] = f"on {context['DATE1MONTH']} {context['DATE1DAY_NUMBER']}, {context['DATE1YEAR']}."
                else:
                    context['ON_OR_BETWEEN'] = f"between {context['DATE1MONTH']} {context['DATE1DAY_NUMBER']}, {context['DATE1YEAR']} and {context['DATE2MONTH']} {context['DATE2DAY_NUMBER']}, {context['DATE2YEAR']}"
            else:
                context['ON_OR_BETWEEN'] = f"on {context['DATE1MONTH']} {context['DATE1DAY_NUMBER']}, {context['DATE1YEAR']}"

            # Correctly zeroes out the day/night values and reapplies them according to the checkbox values. In the future this could be simplified by
            # only grabbing the values if the associated checkbox is checked. Common verbiage will likely force this.
            context['DAYTIME'] = ''
            context['NIGHTTIME'] = ''
            context['NIGHTJUSTIFY'] = ''
            if self.v['DAYTIME'].isChecked() == True:
                context['DAYTIME'] = self.v['DAYTIME'].text() + '.\n'
            if self.v['NIGHTTIME'].isChecked() == True:
                context['NIGHTTIME1'] = self.v['NIGHTTIME'].text() + ' for the following reason(s):\n\n'
                context['NIGHTJUSTIFY'] = self.v['NIGHTJUSTIFY'].toPlainText()
                context['NIGHTTIME2'] = self.v['NIGHTTIME'].text() + ', good cause having been shown.\n'
            
            # Compile reasons
            for index, item in enumerate(self.r):
                if self.rCB[index].isChecked() == True:
                    self.rHolder = self.rHolder + item + '\n\n'
            context['PROPERTY_REASONS'] = self.rHolder

            # Compile Common Verbiage
            context['COMMON_VERBIAGE'] = ''
            for index, item in enumerate(self.verbiage_list):
                if self.checkbox_list[index].isChecked():
                    self.vHolder = self.vHolder + item + '\n\n'                    
    
            context['COMMON_VERBIAGE'] = self.vHolder               
                   
            # Establish correct grammar for number of years experience
            if context['YEARS'] == '1':
                context['YEARS'] = '1 year'
            else:
                context['YEARS'] = context['YEARS'] + ' years'

            # Establish unresolved variables
            
            context['T_AND_E'] = self.TandESrc
            context['DAY_NUMBER'] = self.dateSuffix(datetime.now().day)
            context['MONTH'] = datetime.now().strftime('%B')
            context['YEAR'] = datetime.now().year

            self.docOut.render(context, autoescape=True)
            self.output_path = f"./output/{self.v['CASENUM'].text()}-warrant.docx"
            self.docOut.save(self.output_path)

            # Confirmation QMessageBox()
            messageComplete = QMessageBox()
            messageComplete.setIcon(QMessageBox.Icon.Information)
            messageComplete.setWindowTitle("Warrant Generated Successfully!")
            messageComplete.setText(f"The warrant was built successfully! It has been saved to warrantBuilder/output/{self.v['CASENUM'].text()}-warrant.docx. Don't forget to proofread!")
            messageComplete.setStandardButtons(QMessageBox.StandardButton.Ok)
            messageComplete.exec()

            # Close window - comment out if second shot at generation is wanted?
            # If keeping window open, consider checking filename to see if exists and iterate by 1 to avoid crashes.
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

    def errorOut(self, missingNo):
        errorOutMsg = QMessageBox()
        errorOutMsg.setIcon(QMessageBox.Icon.Critical)
        errorOutMsg.setWindowTitle(f"{missingNo} not found!")
        errorOutMsg.setText(f"The program is missing the {missingNo}. Please get a new copy of the missing item or download the warrantBuilder .zip again. This program will now exit.")
        errorOutMsg.setStandardButtons(QMessageBox.StandardButton.Ok)
        errorOutMsg.exec()

app = QApplication(sys.argv)

window = MainWindow()
window.show()
app.setStyle('Fusion')
app.exec()