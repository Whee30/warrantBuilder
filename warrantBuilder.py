import sys
from PyQt6.QtWidgets import QApplication, QStatusBar, QToolBar, QListView, QFormLayout, QMessageBox, QSizePolicy, QCheckBox, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QGridLayout, QTabWidget, QLineEdit, QComboBox, QPushButton, QLabel, QTextEdit, QFrame, QScrollArea, QDateEdit
from PyQt6.QtCore import Qt, QDate, QDir, QEvent, QSize
from PyQt6.QtGui import QFileSystemModel, QAction, QIcon, QKeySequence
from docxtpl import DocxTemplate
import os
from datetime import datetime
import json
import glob
import requests
import hashlib
import time
#import pyi_splash


# Global variables
local_version = 2.5
remote_refs = "https://forrestcook.net/wp-content/uploads/misc/requirements.json"
hash_refs = "https://raw.githubusercontent.com/Whee30/warrantBuilder/refs/heads/main/sources/hash_list.json"
t_and_e = ""
req = {}
hash_list = {}
headers = {
    'Cache-Control': 'no-cache, no-store, must-revalidate',
    'Pragma': 'no-cache',
    'Expires': '0'
    }
settings_data = {}
cvdata = {}
req_json = "./sources/requirements.json"

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initial_prep()

        # Declare values dictionary
        self.v = {}
        # This variable will hold the property reason checkbox values
        self.rHolder = ''''''
        # This variable holds the common verbiage additions
        self.vHolder = ''''''    
        # Where the source template file lives
        self.templatePath = "./sources/skeleton.docx"
        # Output file variable
        self.docOut = DocxTemplate(self.templatePath)

        # Establish the tab position and settings
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
        self.v['JUDGE'].setPlaceholderText("'A. Smith'")

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
        submitButton.setStatusTip("Generate the warrant.")

        clearButton = QPushButton()
        clearButton.setText("Reset Form")
        clearButton.clicked.connect(lambda: self.are_you_sure(self.clearForm))
        clearButton.setStatusTip("Reset the form to blank values.")

        quitButton = QPushButton()
        quitButton.setText("Quit Program")
        quitButton.clicked.connect(lambda: self.are_you_sure(self.quit_program))
        quitButton.setStatusTip("Quit the program.")

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
        caseLayout.addWidget(QLabel("Complete all fields that apply. Don't forget to proofread your warrant!\t"))
        #caseLayout.addStretch()

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
        self.loadOldWarrant.setStatusTip("Load the selected warrant into the builder for modification.")

        self.deleteOldWarrant = QPushButton()
        self.deleteOldWarrant.setText("Delete Selected Entry")
        self.deleteOldWarrant.setFixedWidth(200)
        self.deleteOldWarrant.clicked.connect(lambda: self.are_you_sure(self.delete_selected_warrant))
        self.deleteOldWarrant.setStatusTip("Delete the selected warrant from the previous warrants list.")  

        self.deleteAllOldWarrants = QPushButton()
        self.deleteAllOldWarrants.setText("Delete All History")
        self.deleteAllOldWarrants.setFixedWidth(200)
        self.deleteAllOldWarrants.clicked.connect(lambda: self.are_you_sure(self.delete_all_old_warrants))
        self.deleteAllOldWarrants.setStatusTip("Delete all previous warrants from the list.")

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
        # Add the tabs to the layout #
        ##############################

        self.tabs.addTab(self.mainScroll, "Warrant Content")
        self.tabs.addTab(self.verbiageScroll, "Template Verbiage")
        self.tabs.addTab(self.savedWarrantsScroll, "Previous Warrants")
        self.setCentralWidget(self.tabs)
        




        ########################
        # Establish Menu items #
        ########################

        # Bring training and experience here?
        # Future home for switching to Subpoena module or warrant return module?

        self.menu_training = QAction("Training and Experience", self)
        self.menu_training.setStatusTip("Edit or view your training and experience verbiage.")
        self.menu_training.triggered.connect(self.launch_training)

        self.menu_settings = QAction("Change Settings", self)
        self.menu_settings.setStatusTip("Change the application settings.")
        self.menu_settings.triggered.connect(self.launch_settings)

        self.menu_update = QAction("Check for updates", self)
        self.menu_update.setStatusTip("Check for updates to the warrant builder.")
        self.menu_update.triggered.connect(self.launch_update)

        self.menu_quit = QAction("Quit the program", self)
        self.menu_quit.setStatusTip("Quit the program.")
        self.menu_quit.triggered.connect(self.quit_program)


        

        menu_bar = self.menuBar()
        options_menu = menu_bar.addMenu("Application Menu")
        options_menu.addAction(self.menu_training)
        options_menu.addAction(self.menu_settings)
        options_menu.addAction(self.menu_update)
        options_menu.addSeparator()
        options_menu.addAction(self.menu_quit)



        self.setStatusBar(QStatusBar(self))








    #######################
    # Establish Functions #
    #######################
    # Update Functions    #
    #######################






    def initial_prep(self):
        global t_and_e
        global hash_list
        global headers
        global settings_data
        global cv_data
        global req
        global req_json
        global remote_refs
        global local_version
        print("Running initial prep function")    
        
        # Check for locally required directories and files
        print("checking for local files")        
        if os.path.exists('./output') == False:
            os.mkdir('./output')
        if os.path.exists('./sources') == False:
            os.mkdir("./sources")
        if os.path.exists('./sources/previousWarrants') == False:
            os.mkdir('./sources/previousWarrants')
        if os.path.exists('./sources/TandE.txt') == False:
            with open("./sources/TandE.txt", "w") as file:
                file.write("This is where you include your relevant experience")
        if os.path.exists('./sources/settings.json') == False:
            with open("./sources/settings.json", "w") as file:
                file.write('{\n')
                file.write('\t"rank_options": ["Ofc.", "Det.", "Sgt."],\n')
                file.write('\t"county_options": ["County One", "County Two"],\n')
                file.write('\t"court_options": ["Court One", "Court Two"],\n')
                file.write('\t"agency_name": "Anytown Police Department",\n')
                file.write('\t"state_name": "Texas"\n')
                file.write('}')
        
                # Loads the app settings
        print("getting settings.json")        
        settings_json = "./sources/settings.json"
        with open(settings_json, 'r') as file:
            settings_data = json.load(file)

        self.setWindowTitle(f"{settings_data['agency_name']} Warrant Builder - v{local_version}")

        t_and_e = open('./sources/TandE.txt', 'r').read()

        print("Initial Prep - Loading required files...")
        if os.path.exists(req_json) == False:
            print("req path not found")
            r_response = requests.get(remote_refs, headers=headers)
            req = r_response.json()
            with open(req_json, 'w') as file:
                json.dump(req, file, indent=4)
        with open(req_json, 'r') as file:
            print("req file found")
            req = json.load(file)
        
        print(req)

        for k, v in req['local_files'].items():
            print(f"looping through required files [{k}]")
            if os.path.exists(v) == False:
                print(f"{k} not found")
                self.replace_file(k)

        print("getting cvsources")
        cv_json = './sources/cv_sources.json'
        with open(cv_json, 'r') as file:
            cv_data = json.load(file)


    def get_remote_data(self):
        global req
        global hash_list
        global remote_refs
        global hash_refs
        global headers
        print("Get remote data function")
        try:
            print("grabbing remote requirements")
            r_response = requests.get(remote_refs, headers=headers)
            req = r_response.json()
            h_response = requests.get(hash_refs, headers=headers)
            hash_list = h_response.json()            
        except:
            print("Something failed in run update while gettings json data")
            return False

    # This function completes the download of files into their expected positions.
    def replace_file(self, k):
        global req
        global hash_list
        global headers 
        if hash_list == {}:
            self.get_remote_data()               
        hash_to_compare = hash_list[k]
        remote_sha256_hash = hashlib.sha256()
        try:
            response = requests.get(req['remote_files'][k], headers=headers)
        except:
            return False
        remote_sha256_hash.update(response.content)
        # If the calculated and listed hashes match, the file will be downloaded
        print(f"remote calculated hash for {k} is: {remote_sha256_hash.hexdigest()}")
        print(f"remote listed hash for {k} is:     {hash_to_compare}")
        if remote_sha256_hash.hexdigest() == hash_to_compare:
            with open(req['local_files'][k], 'wb') as file:
                file.write(response.content)
            print(f"The hashes match and the {k} file was updated.")
        # If not, the files and hashes should be examined for what's rotten in Denmark
        else:
            print(f"The hashes don't match! Something's wonky in dolphin-town. The {k} file was not replaced.")
            print(f"{k} calculated: {remote_sha256_hash.hexdigest()}")
            print(f"{k} Stored:     {hash_to_compare}")


    #########################
    # End Initial Functions #
    #########################



    # Menu Settings function
    def launch_settings(self, checked):
        self.s_w = settings_window()
        self.s_w.show()


    # Menu Update function
    def launch_update(self, checked):
        self.u_w = update_window()
        self.u_w.show()


    # Menu Training function
    def launch_training(self, checked):
        self.t_w = training_window()
        self.t_w.show()


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


    # Main form submission function
    def submitForm(self):
        global t_and_e
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
            context['T_AND_E'] = t_and_e
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

            # Open the output directory to show the new warrant
            os.startfile(os.path.abspath('./output'))

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
            json.dump(context, file, indent=4)

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
        
    # Quits the program   
    def quit_program(self):
        window.close()

    def nothing_selected(self):
        # Consider a list of verbiage that can be called dynamically by the calling button to customize the alert?
        confirmation_box = QMessageBox()
        confirmation_box.setIcon(QMessageBox.Icon.Question)
        confirmation_box.setWindowTitle("Attention!")
        confirmation_box.setText("No file was selected.")
        confirmation_box.setStandardButtons(QMessageBox.StandardButton.Ok)
        confirmation_box.exec()
        










#############################
# Establish Settings Window #
#############################

class settings_window(QMainWindow):
    def __init__(self):
        super().__init__()

        self.main_widget = QWidget()
        self.setCentralWidget(self.main_widget)
        self.setWindowTitle("Warrant Builder Settings")

        self.settings_layout = QVBoxLayout()
        self.main_widget.setLayout(self.settings_layout)

        self.h_container = QWidget()
        self.h_container_layout = QHBoxLayout()
        self.h_container_layout.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)
        self.h_container.setLayout(self.h_container_layout)

        self.h_container_2 = QWidget()
        self.h_container_2_layout = QHBoxLayout()
        self.h_container_2_layout.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)
        self.h_container_2.setLayout(self.h_container_2_layout)
        
        self.s_rank = QWidget()
        self.s_rank_layout = QVBoxLayout()
        self.s_rank.setLayout(self.s_rank_layout)

        self.s_court = QWidget()
        self.s_court_layout = QVBoxLayout()
        self.s_court.setLayout(self.s_court_layout) 
        
        self.s_county = QWidget()
        self.s_county_layout = QVBoxLayout()
        self.s_county.setLayout(self.s_county_layout)   
        
        self.s_state = QWidget()
        self.s_state_layout = QVBoxLayout()
        self.s_state.setLayout(self.s_state_layout)
        
        self.s_agency = QWidget()
        self.s_agency_layout = QVBoxLayout()
        self.s_agency.setLayout(self.s_agency_layout)

        self.settings_layout.addWidget(QLabel("Warrant Builder Settings:"))
        self.settings_layout.addWidget(QLabel("The settings that you change here will alter the options available in the warrant builder.\nThe settings must be saved and the program restarted for the settings to take effect.\nSaving changes will automatically shut down the warrant builder."))
        self.settings_layout.addWidget(self.h_container)

        self.h_container_layout.addWidget(self.s_state)
        self.s_state_layout.addWidget(QLabel("State name:"))
        self.s_state_text = QLineEdit()
        self.s_state_text.setFixedWidth(200)
        self.s_state_layout.addWidget(self.s_state_text)

        self.h_container_layout.addWidget(self.s_agency)
        self.s_agency_layout.addWidget(QLabel("Agency name:"))
        self.s_agency_text = QLineEdit()
        self.s_agency_text.setFixedWidth(200)   
        self.s_agency_layout.addWidget(self.s_agency_text)

        self.h_container_layout.addStretch()

        self.settings_layout.addWidget(QLabel("Enter one option per line for the following settings:"))
        self.settings_layout.addWidget(self.h_container_2)  

        self.h_container_2_layout.addWidget(self.s_rank)
        self.s_rank_layout.addWidget(QLabel("Rank options:"))
        self.s_rank_text = QTextEdit()
        self.s_rank_text.setFixedWidth(100)
        self.s_rank_text.setFixedHeight(100)
        self.s_rank_layout.addWidget(self.s_rank_text)

        self.h_container_2_layout.addWidget(self.s_county)
        self.s_county_layout.addWidget(QLabel("County options:"))
        self.s_county_text = QTextEdit()
        self.s_county_text.setFixedWidth(100)
        self.s_county_text.setFixedHeight(100)
        self.s_county_layout.addWidget(self.s_county_text)

        self.h_container_2_layout.addWidget(self.s_court)
        self.s_court_layout.addWidget(QLabel("Court options:"))
        self.s_court_text = QTextEdit()
        self.s_court_text.setFixedWidth(200)
        self.s_court_text.setFixedHeight(100)
        self.s_court_layout.addWidget(self.s_court_text)

        self.h_container_2_layout.addStretch()

        self.s_buttons = QWidget()
        self.s_buttons_layout = QHBoxLayout()
        self.s_buttons.setLayout(self.s_buttons_layout)
    
        self.settings_layout.addWidget(self.s_buttons)
        
        self.s_submit = QPushButton()
        self.s_submit.setText("Save and Close")
        self.s_submit.setFixedWidth(200)
        self.s_submit.clicked.connect(lambda: self.are_you_sure(self.save_settings))
        self.s_submit.setStatusTip("Save changes and close the program.")

        self.s_quit = QPushButton()
        self.s_quit.setText("Close Window")
        self.s_quit.setFixedWidth(200)
        self.s_quit.clicked.connect(self.close)
        self.s_quit.setStatusTip("Close this window without saving changes.")

        self.s_buttons_layout.addStretch()
        self.s_buttons_layout.addWidget(self.s_submit)
        self.s_buttons_layout.addWidget(self.s_quit)
        self.s_buttons_layout.addStretch()

        self.setStatusBar(QStatusBar())
        self.populate_settings()






    
    ################################
    # Establish settings functions #
    ################################

    def save_settings(self):
        print("Save settings")
        global settings_data
        settings_data['rank_options'] = self.s_rank_text.toPlainText().splitlines()
        for line in settings_data['rank_options']:
            line = line.strip()
        settings_data['county_options'] = self.s_county_text.toPlainText().splitlines()
        for line in settings_data['county_options']:
            line = line.strip()
        settings_data['court_options'] = self.s_court_text.toPlainText().splitlines()
        for line in settings_data['court_options']:
            line = line.strip()
        settings_data['state_name'] = self.s_state_text.text().strip()
        settings_data['agency_name'] = self.s_agency_text.text().strip()
        with open('./sources/settings.json', 'w') as file:
            json.dump(settings_data, file, indent=4)
        #self.close()
        app.quit()
    
    def populate_settings(self):
        global settings_data
        self.s_rank_text.setText('\n'.join(settings_data['rank_options']))
        self.s_county_text.setText('\n'.join(settings_data['county_options']))
        self.s_court_text.setText('\n'.join(settings_data['court_options']))
        self.s_state_text.setText(settings_data['state_name'])
        self.s_agency_text.setText(settings_data['agency_name'])

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









############################################
# Establish Training and Experience Window #
############################################

class training_window(QMainWindow):
    def __init__(self):
        global t_and_e
        super().__init__()

        self.main_widget = QWidget()
        self.setCentralWidget(self.main_widget)
        self.window().setWindowTitle("Training and Experience Editor")

        self.training_layout = QVBoxLayout()
        self.training_layout.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)
        self.main_widget.setLayout(self.training_layout)

        self.training_content = QTextEdit()
        self.training_content.setMaximumHeight(300)
        self.training_content.setText(t_and_e)

        self.training_save = QPushButton()
        self.training_save.setText("Save Changes")
        self.training_save.clicked.connect(lambda: self.are_you_sure(self.save_training))
        self.training_save.setStatusTip("Save any changes made to the training verbiage.")

        self.training_reload = QPushButton()
        self.training_reload.setText("Reload Current Version")
        self.training_reload.clicked.connect(self.reload_training)
        self.training_reload.setStatusTip("Reload the current training verbiage to undo any pending changes.")

        self.training_close = QPushButton()
        self.training_close.setText("Close Window")
        self.training_close.clicked.connect(self.close)
        self.training_close.setStatusTip("Close this window.")

        self.training_layout.addWidget(QLabel("If you make changes to this, you must save them for the changes to appear in your warrant."))
        self.training_layout.addWidget(QLabel("This is how your training and Experience will look currently:"))
        self.training_layout.addWidget(self.training_content)
        self.training_layout.addWidget(self.training_save)
        self.training_layout.addWidget(self.training_reload)
        self.training_layout.addWidget(self.training_close)
        self.training_layout.addStretch()

        self.setStatusBar(QStatusBar())
    
    # Saves pending changes to the training and experience document
    def save_training(self):
        global t_and_e
        with open('./sources/TandE.txt', 'w') as file:
            file.write(self.training_content.toPlainText())
        t_and_e = open('./sources/TandE.txt', 'r').read()
        self.close()

    # Reloads the current saved training and experience content
    def reload_training(self):
        global t_and_e
        self.training_content.setText(t_and_e)

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












###########################
# Establish Update Window #
###########################

class update_window(QMainWindow):
    def __init__(self):
        super().__init__()

        self.main_widget = QWidget()
        self.setCentralWidget(self.main_widget)
        self.window().setWindowTitle("Update Utility")

        self.update_layout = QVBoxLayout()
        self.update_layout.setAlignment(Qt.AlignmentFlag.AlignCenter | Qt.AlignmentFlag.AlignTop)
        self.main_widget.setLayout(self.update_layout)
        self.update_layout.addWidget(QLabel("Checking for updates..."))

        self.update_report = QTextEdit()
        self.update_report.setReadOnly(True)
        self.update_layout.addWidget(self.update_report)

        self.update_buttonrow = QWidget()
        self.update_buttonrow_layout = QHBoxLayout()
        self.update_buttonrow.setLayout(self.update_buttonrow_layout)
        self.update_layout.addWidget(self.update_buttonrow)

        self.update_submit = QPushButton()
        self.update_submit.setText("Check for Updates")
        self.update_submit.setFixedWidth(200)
        self.update_submit.clicked.connect(self.run_update)
        self.update_submit.setStatusTip("Check online for updates to the warrant builder and its resources.")

        self.update_quit = QPushButton()
        self.update_quit.setText("Close Window")
        self.update_quit.setFixedWidth(200)
        self.update_quit.clicked.connect(self.close)
        self.update_quit.setStatusTip("Close this window.")

        self.update_buttonrow_layout.addWidget(self.update_submit)
        self.update_buttonrow_layout.addWidget(self.update_quit)

        self.setStatusBar(QStatusBar())

    def run_update(self):
        global remote_refs
        global req
        global hash_refs
        global hash_list
        global headers
        global local_version
        print("Running update function")
        
        try:
            print("grabbing remote requirements and hashes")
            self.status_update("Getting remote data...")
            r_response = requests.get(remote_refs, headers=headers)
            req = r_response.json()
            self.status_update("Getting remote hash list...")
            h_response = requests.get(hash_refs, headers=headers)
            hash_list = h_response.json()      
        except:
            self.status_update("Something failed while trying to get remote data. Are you connected to the internet?")
            print("Something failed in run update while gettings json data")
            return False

        self.status_update("Checking for remote files...")
        # Grab the remote requirements json data
        for k in req['local_files'].keys():
            print(f"Looping through remote requirements - [{k}]")
            hash_to_compare = hash_list[k]
            self.status_update(f"Checking hash for local {k} against remote hash list...")
            local_sha256_hash = hashlib.sha256()
            with open(req['local_files'][k], "rb") as file:
                for byte_block in iter(lambda: file.read(4096), b""):
                    local_sha256_hash.update(byte_block)
            print(f"hash to compare for remote {k} is: {hash_to_compare}")
            print(f"Local calculated hash for {k} is: {local_sha256_hash.hexdigest()}")
            if local_sha256_hash.hexdigest() != hash_to_compare:
                self.status_update(f"There is a different {k} file available.")
                remote_sha256_hash = hashlib.sha256()
                try:
                    response = requests.get(req['remote_files'][k], headers=headers)
                except:
                    print("run_update failed to get the remote file...")
                    return False
                remote_sha256_hash.update(response.content)
                # If the calculated and listed hashes match, the file will be downloaded
                print(f"remote calculated hash for {k} is: {remote_sha256_hash.hexdigest()}")
                print(f"remote listed hash for {k} is:     {hash_to_compare}")
                if remote_sha256_hash.hexdigest() == hash_to_compare:
                    with open(req['local_files'][k], 'wb') as file:
                        file.write(response.content)
                    self.status_update(f"The {k} file was updated.")
                elif remote_sha256_hash.hexdigest() != hash_to_compare:
                    print(f"The hashes don't match! Something's wonky in dolphin-town. The {k} file was not replaced.")
                    print(f"{k} calculated: {remote_sha256_hash.hexdigest()}")
                    print(f"{k} Stored:     {hash_to_compare}")
                    self.status_update(f"There is a problem with the remote file, {k} was NOT updated.")
            else:
                self.status_update(f"The {k} file is already up to date.")
        # Update the program itse
        print(local_version)
        print(req['app_version'])
        #if float(req['app_version']) > local_version:
        hash_to_compare = hash_list['program']
        self.status_update(f"Checking hash for local program against remote hash list...")
        
        print(req['program_location'])
        program_sha256_hash = hashlib.sha256()
        try:
            with requests.get(req['program_location'], headers=headers, stream=True, timeout=30) as response:
                response.raise_for_status()
                for chunk in response.iter_content(chunk_size=8192):
                    program_sha256_hash.update(chunk)
        except requests.exceptions.RequestException as e:
            print(f"Failed to download file: {e}")
            return False

        print(f"remote calculated hash for program is: {program_sha256_hash.hexdigest()}")
        print(f"remote listed hash for program is:     {hash_to_compare}")

            #if program_sha256_hash.hexdigest() == hash_to_compare:
            #    self.status_update("A new warrant builder is being downloaded. You can find it in the same folder as this one.")
            #    self.status_update(f"The new version is called 'warrantBuilder{req['app_version']}.exe'.")
            #    with open(f"warrantBuilder{req['app_version']}.exe", 'wb') as file:
            #        file.write(response.content)
            #else:
            #    print("The program hashes don't match!")
            #    self.status_update("There is a problem with the remote file, the program was NOT updated.")

        self.status_update("Finished checking for updates.")
        print("run update is done")
    
    def status_update(self, message):
        self.update_report.append(message)
        QApplication.processEvents()

    
app = QApplication(sys.argv)

#pyi_splash.close()
window = MainWindow()
window.show()
app.setStyle('Fusion')

app.exec()
