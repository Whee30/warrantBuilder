#!/usr/bin/python
import PySimpleGUI as Sg
from pathlib import Path
from docxtpl import DocxTemplate
import os

Sg.theme('Dark')

# Check for required directories
if os.path.exists('./output') == False:
    os.mkdir('./output')
    Sg.popup("Output directory was missing, created new output directory at warrantBuilder/output/")
if os.path.exists('./sources') == False:
    Sg.popup("You are missing the WarrantBuilder/sources/ directory! You need to re-download or re-extract the package. This program will now exit.")

# YouTube tutorial for these docxtple functions
# https://www.youtube.com/watch?v=fziZXbeaegc

# Where the source template file lives
# templatePath = Path(__file__).parent / "sources/WarrantSkeleton.docx"
templatePath = "./sources/WarrantSkeleton.docx"
# Output file variable
docOut = DocxTemplate(templatePath)


# Assign the content of the source files to variables
resSrc = open('./sources/residence.txt').read()
vehSrc = open('./sources/vehicle.txt').read()
socSrc = open('./sources/social.txt').read()
TandESrc = open('./sources/TandE.txt').read()
cellSrc = open('./sources/cellphone.txt').read()
narcSrc = open('./sources/narcotics.txt').read()
compSrc = open('./sources/computer.txt').read()
fraudSrc = open('./sources/fraud.txt').read()

county = 'Pima'

# Tuple containing reasons, checkboxes will call these
r = (
    "Were stolen or embezzled.",
    "Were used as a means for committing a public offense.",
    "Is being possessed with the intent to use it as a means of committing a public offense.",
    "Are in the possession of to whom it was delivered for the purpose of concealing it or preventing it from "
    "being discovered.",
    "Consists of any item or constitutes any evidence which tends to show that a public offense has been committed,"
    " or tends to show that a particular person committed the public offense.",
    "The person sought is the subject of an outstanding arrest warrant which offense occurred on or about the day of"
    " , 20 in the County of Pima, State of Arizona.",
    )

serviceTime = (
    "In the daytime (excluding the time period between 10:00 p.m and 6:30 a.m)",
    "In the nighttime"
)

serviceIndex = 0

common_verbiage = {
    'v_cellphone':cellSrc,
    'v_computer':compSrc,
    'v_residence':resSrc,
    'v_social':socSrc,
    'v_narcotics':narcSrc,
    'v_fraud':fraudSrc
}

rIndex = ['0','1','2','3','4','5']

# This variable will hold the property reason checkbox values
rHolder = ''''''

# This variable holds the common verbiage additions
vHolder = ''''''

# Define available ranks for the dropdown
ranks = ["Ofc.", "Det.", "Sgt."]

# Define available courts for the dropdown
courts = ["Oro Valley Magistrate Court", "Pima County Superior Court", "Pima County Justice Court"]

# This is the section of the layout that contain the date range buttons
dateCols = [
    [Sg.Text("Date Range:", size=(10, 1))],
    [Sg.CalendarButton(button_text="Start Date", size=(10, 1), key="STARTTIME", format='%A %B %d, %Y', target='START_TIME', pad=10),
     Sg.Input(key="START_TIME", default_text="From", size=(25, 1))],
    [Sg.CalendarButton(button_text="End Date", key="ENDTIME", size=(10, 1), format='%A %B %d, %Y', target='END_TIME', pad=10),
     Sg.Input(key="END_TIME", default_text="To", size=(25, 1))]
]

possession_column = [
    [Sg.Text('In possession of:', size=(12, 1))],
    [Sg.Multiline(key="SUSPECT", size=(30, 5), pad=10)]
]

residence_column = [
    [Sg.Text('On Premises:', size=(10, 1))],
    [Sg.Multiline(key="PREMISES", size=(30, 5), pad=10)]
]

vehicle_column = [
    [Sg.Text('In Vehicle(s):', size=(10, 1))],
    [Sg.Multiline(key="VEHICLE", size=(30, 5), pad=10)]
]

property_column = [
    [Sg.Text("Property Sought:", size=(12, 1))],
    [Sg.Multiline(key="PROPERTY", size=(100, 10), pad=10)]
]

crime_column = [
    [Sg.Text("Crimes:", size=(12, 1))],
    [Sg.Multiline(key="CRIMES", size=(50, 5), pad=10)]
]

affidavit_column = [
    [Sg.Text("Affidavit:", size=(12, 1), pad=10)],
    [Sg.Multiline(key="AFFIDAVIT", size=(100, 10), pad=10)]
]

# Column containing form
scroll_column = [[
    Sg.vtop(Sg.Text('Warrant Builder v0.1 (beta)', 
    size=(50, 2), 
    font=("Arial", 20)))],

# Affiant info block
    [Sg.Text('Rank:'),
     Sg.Combo(ranks, key='RANK', default_value=ranks[1], pad=10),
     Sg.Text('Name:'),
     Sg.Input(key="NAME", size=(10, 1), pad=10),
     Sg.Text('Badge #:'),
     Sg.Input(key="BADGE", size=(10, 1), default_text="V"),
     Sg.Text('Case Number:', size=(12, 1)),
     Sg.Input(key="CASENUM", size=(20, 1), default_text="V", pad=10),
     ],

# Jurisdiction block
    [Sg.Text('Court:'),
     Sg.Combo(courts, key='COURT', default_value=courts[0]),
     Sg.Text('Judge:'),
     Sg.Input(key="JUDGE", size=(20, 1))
     ],

    [Sg.HorizontalSeparator(color='black', pad=20)],

# People/Places/Vehicles block
    [Sg.Column(possession_column),
     Sg.Column(residence_column),
     Sg.Column(vehicle_column)     
     ],

# Property block
    [Sg.Column(property_column)],

# Common verbiage block
    [Sg.vtop(Sg.Text("Common Verbiage:", pad=10)),
     Sg.Checkbox("Cellphone", key='v_cellphone'),
     Sg.Checkbox("Computer", key='v_computer'),
     Sg.Checkbox("Residence", key='v_residence'),
     Sg.Checkbox("SocialMedia", key='v_social'),
     Sg.Checkbox("Narcotics", key='v_narcotics'),
     Sg.Checkbox("Fraud", key='v_fraud')
     ],

# Statutes block
    [Sg.Column(crime_column),
     Sg.vtop(Sg.Column(dateCols))],

# Affidavit block
    [Sg.Column(affidavit_column)],

# Checkboxes for property reasons
    [Sg.Checkbox(text=r[0], key='0', size=(90, 2))],
    [Sg.Checkbox(text=r[1], key='1', size=(90, 2))],
    [Sg.Checkbox(text=r[2], key='2', size=(90, 2))],
    [Sg.Checkbox(text=r[3], key='3', size=(90, 2))],
    [Sg.Checkbox(text=r[4], key='4', size=(90, 2))],
    [Sg.Checkbox(text=r[5], key='5', size=(90, 2))],

    [Sg.HorizontalSeparator(color='black', pad=10)],

# Day/night service radio buttons
    [Sg.Radio(text=serviceTime[0], key='DAYTIME', 
              size=(90, 2), group_id='radio_service', default=True, enable_events=True)],
    [Sg.Radio(text=serviceTime[1], key='NIGHTTIME', 
              size=(90, 2), group_id='radio_service', enable_events=True)],
    [Sg.Text('Nighttime Justification:', key="night_text"),
     Sg.Input(key="NIGHTTIME_JUSTIFICATION", disabled=True, default_text='')],

    [Sg.HorizontalSeparator(color='black', pad=10)],

# Form buttons
    [Sg.Stretch(), Sg.Button("Generate Warrant", size=(20, 1)), Sg.Stretch(), Sg.Exit(button_text='Exit', size=(20, 1)), Sg.Stretch()],

# Hidden values placed here
    [Sg.Input(key='PROPERTY_REASONS', visible=False)],
    [Sg.Input(key='TRAININGEXPERIENCE', visible=False)],
    [Sg.Input(key='SERVICETIME', visible=False)],
    [Sg.Input(key='COMMON_VERBIAGE', visible=False)]
]


layout = [[
    Sg.Column(
        scroll_column, 
        scrollable=True, 
        vertical_scroll_only=True, 
        size=(980, 790))
    ]]

window = Sg.Window(
    "Warrant Builder V0.1", 
    layout, 
    size=(1010, 800), 
    resizable=True, 
    font=("Arial", 11)
    )

# Rules that govern what happens when you press buttons
while True:
    event, values = window.read()
    if event == Sg.WIN_CLOSED or event == "Exit":
        break
# daytime/nighttime radio button events
    if event == 'NIGHTTIME':
        window['NIGHTTIME_JUSTIFICATION'].update(disabled = False)
    if event == 'DAYTIME':
        window['NIGHTTIME_JUSTIFICATION'].update('')
        window['NIGHTTIME_JUSTIFICATION'].update(disabled = True)
    if event == "Generate Warrant":
# Property reason For loop
        for check in rIndex:
            if window[check].Get() == True:
                rHolder = rHolder + window[check].Text + '\n\n'
# Common verbiage For loop
        for each_check, data_source in common_verbiage.items():
            if window[each_check].Get() == True:
                vHolder = vHolder + data_source + '\n\n'
        values['COMMON_VERBIAGE'] = vHolder
        values['PROPERTY_REASONS'] = rHolder
        values['TRAININGEXPERIENCE'] = TandESrc
        values['COUNTY'] = county
        if window['DAYTIME'].Get() == True:
            serviceIndex = 0
        elif window['NIGHTTIME'].Get() == True:
            serviceIndex = 1
        values['SERVICETIME'] = serviceTime[serviceIndex]
        docOut.render(values)
        output_path = f"./output/{values['CASENUM']}-search warrant.docx"
        docOut.save(output_path)
        Sg.popup("Warrant built, don't forget to proofread!", f"File has been saved to: {output_path}")
        break

window.close()
