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

settings_json = "./sources/settings.json"

with open(settings_json, 'r') as file:
    settings_data = json.load(file)

# Get the path to the cvSources.py file (relative to the executable)
cv_json = './sources/cv_sources.json'

with open(cv_json, 'r') as file:
    cv_data = json.load(file)

# Access the list
#my_list = cv_data['cvDict']

class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        # Check for required directories and files        
        if os.path.exists('./output') == False:
            os.mkdir('./output')
        if os.path.exists('./sources/previousWarrants') == False:
            os.mkdir('./sources/previousWarrants')
        if os.path.exists('./sources') == False:
            self.errorOut("sources folder")        
        if os.path.exists('./sources/TandE.txt') == False:
            self.errorOut("TandE.txt")
        if os.path.exists('./sources/skeleton.docx') == False:
            self.errorOut("skeleton.docx")
        if os.path.exists('./sources/cv_sources.json') == False:
            self.errorOut("cv_sources.json")

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

        self.setWindowTitle("Warrant Builder v2.4")
        self.setFixedWidth(810)
        self.setMinimumHeight(600)
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
        for item in settings_data['rank_options']:
            self.v['RANK'].addItem(item)
        self.v['RANK'].setFixedWidth(100)
        self.v['RANK'].installEventFilter(self)

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
        for item in settings_data['county_options']:
            self.v['COUNTY'].addItem(item)

        self.v['COUNTY'].installEventFilter(self)

        self.v['COURT'] = QComboBox()
        
        for item in settings_data['court_options']:
            self.v['COURT'].addItem(item)
        
        self.v['COURT'].setEditable(True)
        self.v['COURT'].setFixedWidth(200)
        self.v['COURT'].installEventFilter(self)

        self.v['JUDGE'] = QLineEdit()
        self.v['JUDGE'].setFixedWidth(200)
        self.v['JUDGE'].setPlaceholderText("'J. Judy'")

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
        self.v['DATE1'].installEventFilter(self)

        self.rangeCheck = QCheckBox("Enable Date Range?")
        self.rangeCheck.clicked.connect(self.date_range_enable)

        self.v['DATE2'] = QDateEdit()
        self.v['DATE2'].setCalendarPopup(True)
        self.v['DATE2'].setDate(QDate().currentDate())
        self.v['DATE2'].setButtonSymbols(self.v['DATE2'].ButtonSymbols.NoButtons)
        self.v['DATE2'].setDisabled(True)
        self.v['DATE2'].installEventFilter(self)

        self.v['AFFIDAVIT'] = QTextEdit()
        self.v['AFFIDAVIT'].setPlaceholderText("Enter Affidavit details here")
        self.v['AFFIDAVIT'].setFixedSize(763,300)

        # Future addition
        #self.nd = "This is the non-disclosure verbiage for the affidavit"
        #self.nd2 = "This is the non-disclosure verbiage for the warrant"

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

        self.v['TELEPHONIC'] = QCheckBox()
        self.v['TELEPHONIC'].setText("Telephonic Warrant")

        # Future addition
        #self.v['NONDISCLOSURE'] = QCheckBox()
        #self.v['NONDISCLOSURE'].setText("Include Non-Disclosure verbiage (18 USC § 2703.b)")

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
        submitButton.clicked.connect(self.submitForm)

        clearButton = QPushButton()
        clearButton.setText("Reset Form")
        clearButton.clicked.connect(lambda: self.are_you_sure(self.clearForm))

        quitButton = QPushButton()
        quitButton.setText("Quit Program")
        quitButton.clicked.connect(lambda: self.are_you_sure(self.quitForm))

        #########################################
        # Establish the layouts of the main tab #
        #########################################

        self.mainTab = QWidget()
        self.mainTabLayout = QVBoxLayout()
        self.mainTabLayout.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)
        self.mainTab.setLayout(self.mainTabLayout)
        self.mainScroll = QScrollArea()
        self.mainScroll.setWidget(self.mainTab)
        self.mainScroll.setWidgetResizable(True)

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

        self.mainTabLayout.addWidget(caseWidget)

        caseLayout.addWidget(QLabel("Case #:"))
        caseLayout.addWidget(self.v['CASENUM'])
        caseLayout.addWidget(self.v['TELEPHONIC'])
        #caseLayout.addWidget(self.v['NONDISCLOSURE'])
        caseLayout.addStretch()
        caseLayout.addWidget(QLabel("Select all that apply. Don't forget to proofread your warrant!"))
        caseLayout.addStretch()

        self.mainTabLayout.addWidget(infoWidget)

        infoLayout.addWidget(QLabel("Rank:"))
        infoLayout.addWidget(self.v['RANK'])
        infoLayout.addWidget(QLabel("Name:"))
        infoLayout.addWidget(self.v['NAME'])
        infoLayout.addWidget(QLabel("Badge:"))
        infoLayout.addWidget(self.v['BADGE'])
        infoLayout.addWidget(QLabel("Years On:"))
        infoLayout.addWidget(self.v['YEARS'])

        infoLayout.addStretch()

        self.mainTabLayout.addWidget(courtWidget)

        courtLayout.addWidget(QLabel("County:"))
        courtLayout.addWidget(self.v['COUNTY'])
        courtLayout.addWidget(QLabel("Court:"))
        courtLayout.addWidget(self.v['COURT'])
        courtLayout.addWidget(QLabel("Judge's Name:"))
        courtLayout.addWidget(self.v['JUDGE'])
        courtLayout.addStretch()

        self.mainTabLayout.addWidget(locWidget)
        
        locLayout.addWidget(QLabel("In Possession Of:"), 0, 0)
        locLayout.addWidget(QLabel("On Premises:"), 0, 1)
        locLayout.addWidget(QLabel("In Vehicle(s):"), 0, 2)
        locLayout.addWidget(self.v['SUSPECT'], 1, 0)
        locLayout.addWidget(self.v['PREMISES'], 1, 1)
        locLayout.addWidget(self.v['VEHICLE'], 1, 2)
        
        self.mainTabLayout.addWidget(QLabel("Property Sought:"))
        self.mainTabLayout.addWidget(self.v['PROPERTY'])

        self.mainTabLayout.addWidget(QLabel("Which property or things:"))

        self.mainTabLayout.addWidget(self.rForm)
   
        # Reason loop
        for index, item in enumerate(self.r):
            label = QLabel(item)
            label.adjustSize()
            label.setWordWrap(True)
            checkbox = QCheckBox()
            self.rCB.append(checkbox)
            self.rForm_l.addRow(checkbox, label)
   
        self.mainTabLayout.addWidget(divider)

        self.mainTabLayout.addWidget(crimeWidget)

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

        self.mainTabLayout.addWidget(QLabel("Affidavit/Probable Cause:"))
        self.mainTabLayout.addWidget(self.v['AFFIDAVIT'])    
    
        self.mainTabLayout.addWidget(QLabel("I am seeking to serve this warrant:"))

        self.mainTabLayout.addWidget(self.v['DAYTIME'])
        self.mainTabLayout.addWidget(self.v['NIGHTTIME'])
        self.mainTabLayout.addWidget(self.v['NIGHTJUSTIFY'])

        self.mainTabLayout.addWidget(buttonWidget)

        buttonLayout.addWidget(submitButton)
        buttonLayout.addWidget(clearButton)
        buttonLayout.addWidget(quitButton)

        self.mainTabLayout.addStretch()

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

        # This list will hold the categories which are made into button objects
        self.button_list = []
        # This list will hold the content of the verbiage
        self.verbiage_list = []
        # This list will reference the widgets to be shown or hidden which contain the verbiage itself
        self.hidden_widget_list = []
        self.checkbox_list = []

        self.verbiageTabLayout.addWidget(QLabel("Click topics to expand/contract - check any that apply. \nAfter selections are made, return to the main tab to finish."))
        self.verbiageTabLayout.addWidget(QLabel("Modify the results to suit your case, if needed."))
        
        # Iterate the template verbiage into checkboxes.
        for index, key in enumerate(cv_data):
            self.button_list.append(key)
            print(key)
            self.button_list[index] = QPushButton()
            self.button_list[index].setText(cv_data[key][0])
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

            for index, listItem in enumerate(cv_data[key]):
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

        ###########################################################
        # Establish the layout of the Training and Experience tab #
        ###########################################################

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
        self.trainingSave.clicked.connect(lambda: self.are_you_sure(self.saveTrainingChanges))

        self.trainingReload = QPushButton()
        self.trainingReload.setText("Reload Current Version")
        self.trainingReload.clicked.connect(lambda: self.are_you_sure(self.reloadTrainingContent))

        self.trainingTabLayout.addWidget(QLabel("If you make changes to this, you must save them for the changes to apper in your warrant."))
        self.trainingTabLayout.addWidget(QLabel("This is how your training and Experience will look currently:"))
        self.trainingTabLayout.addWidget(self.trainingContent)
        self.trainingTabLayout.addWidget(self.trainingSave)
        self.trainingTabLayout.addWidget(self.trainingReload)
        self.trainingTabLayout.addStretch()

        #######################################
        # Establish the previous warrants tab #
        #######################################

        self.savedWarrantsTab = QWidget()
        self.savedWarrantsTabLayout = QVBoxLayout()
        self.savedWarrantsTabLayout.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)
        self.savedWarrantsTab.setLayout(self.savedWarrantsTabLayout)
        self.savedWarrantsScroll = QScrollArea()
        self.savedWarrantsScroll.setWidget(self.savedWarrantsTab)
        self.savedWarrantsScroll.setWidgetResizable(True)

        self.savedButtonContainer = QWidget()
        self.savedButtonLayout = QHBoxLayout()
        self.savedButtonContainer.setLayout(self.savedButtonLayout)

        self.loadOldWarrant = QPushButton()
        self.loadOldWarrant.setText("Load into Builder")
        self.loadOldWarrant.setFixedWidth(200)
        self.loadOldWarrant.clicked.connect( self.load_old_warrant_data )

        self.deleteOldWarrant = QPushButton()
        self.deleteOldWarrant.setText("Delete Selected Entry")
        self.deleteOldWarrant.setFixedWidth(200)
        self.deleteOldWarrant.clicked.connect(lambda: self.are_you_sure(self.delete_selected_warrant))

        self.deleteAllOldWarrants = QPushButton()
        self.deleteAllOldWarrants.setText("Delete All History")
        self.deleteAllOldWarrants.setFixedWidth(200)
        self.deleteAllOldWarrants.clicked.connect(lambda: self.are_you_sure(self.delete_all_old_warrants))

        self.savedWarrantsMid = QWidget()
        self.savedWarrantsMidLayout = QHBoxLayout()
        self.savedWarrantsMid.setLayout(self.savedWarrantsMidLayout)

        self.file_model = QFileSystemModel()
        self.file_model.setRootPath("./sources/previousWarrants")
        self.file_model.setFilter(QDir.Filter.Files | QDir.Filter.NoDotAndDotDot)

        self.savedWarrantLister = QListView()
        self.savedWarrantLister.setModel(self.file_model)
        self.savedWarrantLister.setFixedWidth(250)
        self.savedWarrantLister.setRootIndex(self.file_model.index("./sources/previousWarrants"))
        self.savedWarrantLister.clicked.connect( self.display_file_content )

        self.savedWarrantPreview = QTextEdit()
        self.savedWarrantPreview.isReadOnly()

        # Add the widgets to the tab
        self.savedWarrantsTabLayout.addWidget(QLabel("This tab will allow you to load old warrants you have previously completed with this program back into the builder to make modifications."))
        self.savedWarrantsTabLayout.addWidget(self.savedWarrantsMid)
        self.savedWarrantsMidLayout.addWidget(self.savedWarrantLister)
        self.savedWarrantsMidLayout.addWidget(self.savedWarrantPreview)

        self.savedWarrantsTabLayout.addWidget(self.savedButtonContainer)
        self.savedButtonLayout.addStretch()
        self.savedButtonLayout.addWidget(self.loadOldWarrant)
        self.savedButtonLayout.addWidget(self.deleteOldWarrant)
        self.savedButtonLayout.addWidget(self.deleteAllOldWarrants)
        self.savedButtonLayout.addStretch()

        ##############################
        # Establish the settings tab #
        ##############################

        # self.settings_tab = QWidget()
        # self.settings_tab_layout = QVBoxLayout()
        # self.settings_tab_layout.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)
        # self.settings_tab.setLayout(self.savedWarrantsTabLayout)

        # self.settings_label = QLabel("Set options")
        



        ##############################
        # Add the tabs to the layout #
        ##############################

        self.tabs.addTab(self.mainScroll, "Warrant Content")
        self.tabs.addTab(self.verbiageScroll, "Template Verbiage")
        self.tabs.addTab(self.trainingScroll, "Training and Experience")
        self.tabs.addTab(self.savedWarrantsScroll, "Previous Warrants")
        self.setCentralWidget(self.tabs)

    def eventFilter(self, source, event):
        if event.type() == QEvent.Type.Wheel:
            return True
        return super().eventFilter(source, event)

    # Displays the saved warrant content into the saved warrant tab
    def display_file_content(self, index):
        file_name = self.file_model.fileName(index)
        with open(f"./sources/previousWarrants/{file_name}", "r") as file:
            loaded_data = json.load(file)
        formatted_text = {}
        formatted_text_display = ""
        formatted_text['Date Created:'] = f"{loaded_data['MONTH']} {loaded_data['DAY_NUMBER']}, {loaded_data['YEAR']}"
        formatted_text['Case_Number:'] = loaded_data['CASENUM']
        if loaded_data['TELEPHONIC'] == True:
            formatted_text['Telephonic'] = " warrant"
        formatted_text['Person:'] = loaded_data['SUSPECT']
        formatted_text['Place:'] = loaded_data['PREMISES']
        formatted_text['Vehicle:'] = loaded_data['VEHICLE']
        formatted_text['Crimes:'] = loaded_data['CRIMES']
        formatted_text['Affidavit:'] = loaded_data['AFFIDAVIT']
        formatted_text['Property:'] = loaded_data['PROPERTY']
        for item, content in formatted_text.items():
            formatted_text_display = formatted_text_display + str(item) + " " + str(content) + "\n\n"
        self.savedWarrantPreview.setText(formatted_text_display)

    # Push saved warrant data back out to form
    def load_old_warrant_data(self):
        file_name = ''
        indexes = self.savedWarrantLister.selectedIndexes()
        if indexes:
            selected_index = indexes[0]
            file_name = self.file_model.fileName(selected_index)
        if file_name == '':
            self.nothing_selected()
            return
        with open(f"./sources/previousWarrants/{file_name}", "r") as file:
            loaded_data = json.load(file)
        self.v['CASENUM'].setText(loaded_data['CASENUM'])
        self.v['TELEPHONIC'].setChecked(loaded_data['TELEPHONIC'])
        self.v['RANK'].setCurrentIndex(loaded_data['reload_rank'])
        self.v['NAME'].setText(loaded_data['NAME'])
        self.v['BADGE'].setText(loaded_data['BADGE'])
        self.v['YEARS'].setText(loaded_data['YEARS'])
        self.v['COUNTY'].setCurrentIndex(loaded_data['reload_county'])
        self.v['COURT'].setCurrentIndex(loaded_data['reload_court'])
        self.v['JUDGE'].setText(loaded_data['JUDGE'])
        self.v['SUSPECT'].setText(loaded_data['SUSPECT'])
        self.v['PREMISES'].setText(loaded_data['PREMISES'])
        self.v['VEHICLE'].setText(loaded_data['VEHICLE'])
        self.v['PROPERTY'].setText(loaded_data['PROPERTY'])
        # Set the reason checkboxes
        for i in range(6):
            if loaded_data[f"reload_r{i}"] == True:
                self.rCB[int(i)].setChecked(True)
        self.v['CRIMES'].setText(loaded_data['CRIMES'])
        self.v['DATE1'].setDate(QDate(loaded_data['reload_date1'][0], loaded_data['reload_date1'][1], loaded_data['reload_date1'][2]))
        if loaded_data['reload_range'] == True:
            self.v['DATE2'].setDisabled(False)
        self.v['DATE2'].setDate(QDate(loaded_data['reload_date2'][0], loaded_data['reload_date2'][1], loaded_data['reload_date2'][2]))
        self.rangeCheck.setChecked(bool(loaded_data['reload_range']))
        self.v['AFFIDAVIT'].setText(loaded_data['AFFIDAVIT'])
        self.v['DAYTIME'].setChecked(loaded_data['reload_daytime'])
        self.v['NIGHTTIME'].setChecked(loaded_data['reload_nighttime'])
        if loaded_data['reload_nighttime'] == True:
            self.v['NIGHTJUSTIFY'].setHidden(False)
            self.v['NIGHTJUSTIFY'].setText(loaded_data['NIGHTJUSTIFY'])

    # Toggles the common verbiage topics
    def toggle_widget(self, checked, target):
        if checked:
            self.hidden_widget_list[target].show()
        else:
            self.hidden_widget_list[target].hide()
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

    # Saves pending changes to the training and experience document
    def saveTrainingChanges(self):
        with open('./sources/TandE.txt', 'w') as file:
            file.write(self.trainingContent.toPlainText())
        self.TandESrc = open('./sources/TandE.txt', 'r').read()

    # Reloads the current saved training and experience content
    def reloadTrainingContent(self):
        self.trainingContent.setText(self.TandESrc)

    # Main form submission function
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
                else:
                    print("You haven't supported this type of widget yet")
            context['TELEPHONIC'] = self.v['TELEPHONIC'].isChecked()
            # Is the date range box checked? Establish the fully formatted date/date range.
            context['ON_OR_BETWEEN'] = ''
            if self.rangeCheck.isChecked() == True:
                context['RANGECHECKED'] = True
                if self.v['DATE1'].date().toString() == self.v['DATE2'].date().toString():
                    context['ON_OR_BETWEEN'] = f"on {context['DATE1MONTH']} {context['DATE1DAY_NUMBER']}, {context['DATE1YEAR']}."
                else:
                    context['ON_OR_BETWEEN'] = f"between {context['DATE1MONTH']} {context['DATE1DAY_NUMBER']}, {context['DATE1YEAR']} and {context['DATE2MONTH']} {context['DATE2DAY_NUMBER']}, {context['DATE2YEAR']}"
            else:
                context['ON_OR_BETWEEN'] = f"on {context['DATE1MONTH']} {context['DATE1DAY_NUMBER']}, {context['DATE1YEAR']}"

            # Correctly zeroes out the day/night values and reapplies them according to the checkbox values. In the future this could be simplified by
            # only grabbing the values if the associated checkbox is checked.
            context['DAYTIME'] = ''
            context['NIGHTTIME'] = ''
            context['NIGHTJUSTIFY'] = ''
            if self.v['DAYTIME'].isChecked() == True:
                context['DAYTIME'] = self.v['DAYTIME'].text() + ',\n'
            if self.v['NIGHTTIME'].isChecked() == True:
                context['NIGHTTIME1'] = self.v['NIGHTTIME'].text() + ' for the following reason(s):\n\n'
                context['NIGHTJUSTIFY'] = self.v['NIGHTJUSTIFY'].toPlainText()
                context['NIGHTTIME2'] = self.v['NIGHTTIME'].text() + ', good cause having been shown,\n'
            
            # Compile reasons
            for index, item in enumerate(self.r):
                if self.rCB[index].isChecked() == True:
                    context[f'reload_r{index}'] = True
                    self.rHolder = self.rHolder + item + '\n\n'
                elif self.rCB[index].isChecked() == False:
                    context[f'reload_r{index}'] = False
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

            # Future addition - Establish the non-disclosure verbiage
            #if self.v['NONDISCLOSURE'].isChecked():
            #    context['NONDISCLOSUREREQUEST'] = self.nd
            #    context['NONDISCLOSUREORDER'] = self.nd2

            # Establish unresolved variables
            context['T_AND_E'] = self.TandESrc
            context['DAY_NUMBER'] = self.dateSuffix(datetime.now().day)
            context['MONTH'] = datetime.now().strftime('%B')
            context['YEAR'] = datetime.now().year
            context['AGENCY'] = settings_data['agency_name']
            context['STATE'] = settings_data['state_name']

            # Establish unresolved re-loading variables
            context['reload_court'] = self.v['COURT'].currentIndex()
            context['reload_rank'] = self.v['RANK'].currentIndex()
            context['reload_county'] = self.v['COUNTY'].currentIndex()
            context['reload_range'] = self.rangeCheck.isChecked()
            context['reload_date1'] = [self.v['DATE1'].date().year(), self.v['DATE1'].date().month(), self.v['DATE1'].date().day()]
            context['reload_date2'] = [self.v['DATE2'].date().year(), self.v['DATE2'].date().month(), self.v['DATE2'].date().day()]
            context['reload_daytime'] = self.v['DAYTIME'].isChecked()
            context['reload_nighttime'] = self.v['NIGHTTIME'].isChecked()

            # Actually build the .docx
            self.docOut.render(context, autoescape=True)
            self.output_filename = f"{self.v['CASENUM'].text()}_{datetime.now().strftime('%y%m%d_%H%M%S')}"
            self.output_path = f"./output/{self.output_filename}.docx"
            self.docOut.save(self.output_path)

            # Dump the information to JSON for the previous warrants tab
            self.save_to_previous_warrants(context)

            # Confirmation QMessageBox()
            messageComplete = QMessageBox()
            messageComplete.setIcon(QMessageBox.Icon.Information)
            messageComplete.setWindowTitle("Warrant Generated Successfully!")
            messageComplete.setText(f"The warrant was built successfully! It has been saved to: {self.output_path}. Don't forget to proofread!")
            messageComplete.setStandardButtons(QMessageBox.StandardButton.Ok)
            messageComplete.exec()


            # Clear out variables if a second warrant is desired
            context = ''
            self.vHolder = ''
            self.rHolder = ''
            self.clearForm()
            # Close window - comment out if second shot at generation is wanted?
            #window.close()
        else:
            print("Action Canceled")
    
    # Saves dictionary to JSON format in ./sources/previousWarrants/
    def save_to_previous_warrants(self, context):
        print("Saving warrant content to sources/previousWarrants/ directory...")
        with open(f"./sources/previousWarrants/{self.output_filename}", "w") as file:
            json.dump(context, file)

    def delete_selected_warrant(self):
        file_name = ''
        indexes = self.savedWarrantLister.selectedIndexes()
        if indexes:
            selected_index = indexes[0]
            file_name = self.file_model.fileName(selected_index)
        if file_name != '':
            os.remove(f"./sources/previousWarrants/{file_name}")
            self.savedWarrantPreview.setText('')
        elif file_name == '':
            self.nothing_selected()

    def delete_all_old_warrants(self):
        files = glob.glob('./sources/previousWarrants/*')
        for f in files:
            os.remove(f)

    def are_you_sure(self, target):
        # Consider a list of verbiage that can be called dynamically by the calling button to customize the alert?
        confirmation_box = QMessageBox()
        confirmation_box.setIcon(QMessageBox.Icon.Question)
        confirmation_box.setWindowTitle("Attention!")
        confirmation_box.setText("Are you sure you want to do this? You cannot go back if you click 'Yes'.")
        confirmation_box.setStandardButtons(QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.Cancel)

        result = confirmation_box.exec()

        if result == QMessageBox.StandardButton.Yes:
            target()
        else:
            print("Action Canceled")

    # Clears form inputs back to initial values
    def clearForm(self):
        for widget in window.findChildren(QWidget):
            if isinstance(widget, QLineEdit):
                widget.clear()  # Clear text in QLineEdit
            elif isinstance(widget, QCheckBox):
                widget.setChecked(False)  # Uncheck QCheckBox
            elif isinstance(widget, QComboBox):
                widget.setCurrentIndex(0) 
            elif isinstance(widget, QTextEdit):
                widget.clear()
            elif isinstance(widget, QDateEdit):
                widget.setDate(QDate.currentDate())
        self.trainingContent.setText(self.TandESrc)
        
    # Quits the program   
    def quitForm(self):
        window.close()

    # Errors out and quits the program if certain resource files are missing
    def errorOut(self, missingNo):
        errorOutMsg = QMessageBox()
        errorOutMsg.setIcon(QMessageBox.Icon.Critical)
        errorOutMsg.setWindowTitle(f"{missingNo} not found!")
        errorOutMsg.setText(f"The program is missing the {missingNo}. Please get a new copy of the missing item or download the warrantBuilder .zip again. This program will now exit.")
        errorOutMsg.setStandardButtons(QMessageBox.StandardButton.Ok)
        errorOutMsg.exec()

    def nothing_selected(self):
        # Consider a list of verbiage that can be called dynamically by the calling button to customize the alert?
        confirmation_box = QMessageBox()
        confirmation_box.setIcon(QMessageBox.Icon.Question)
        confirmation_box.setWindowTitle("Attention!")
        confirmation_box.setText("No file was selected.")
        confirmation_box.setStandardButtons(QMessageBox.StandardButton.Ok)
        confirmation_box.exec()


app = QApplication(sys.argv)

#pyi_splash.close()
window = MainWindow()
window.show()
app.setStyle('Fusion')
app.exec()