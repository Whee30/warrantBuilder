#!/usr/bin/python
import PySimpleGUI as Sg
from pathlib import Path
from docxtpl import DocxTemplate

# YouTube tutorial for these functions
# https://www.youtube.com/watch?v=fziZXbeaegc

Sg.theme('DarkGray')

# Where the source template file lives
templatePath = Path(__file__).parent / "WarrantSkeleton.docx"
# Output file variable
docOut = DocxTemplate(templatePath)

# Assign the content of the source files to variables
resSrc = open('./sources/residence.txt').read()
vehSrc = open('./sources/vehicle.txt').read()
socSrc = open('./sources/social.txt').read()
TandESrc = open('./sources/TandE.txt').read()

county = 'Pima'

# Defines options in a multi-select list
s = (
    "Cellphones",
    "Residences",
    "Vehicles"
    )

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

serviceIndex = ['s0','s1']

rIndex = ['0','1','2','3','4','5']



rHolder = ''''''

# Define available ranks for the dropdown
ranks = ["Ofc.", "Det.", "Sgt."]
# Define available courts for the dropdown
courts = ["Oro Valley Magistrate Court", "Pima County Superior Court", "Pima County Justice Court"]

# This is the section of the layout that contain the date range buttons
dateCols = [
    [Sg.vtop(Sg.Text("Date Range:", size=(10, 1)))],
    [Sg.CalendarButton(button_text="Start Date", key="STARTTIME", format='%a %B %d, %Y', target='START_TIME'),
     Sg.Input(key="START_TIME", default_text="From", size=(25, 1))],

    [Sg.CalendarButton(button_text="End Date", key="ENDTIME", format='%a %B %d, %Y', target='END_TIME'),
     Sg.Input(key="END_TIME", default_text="To", size=(25, 1))]
]

# This is the section of the layout that contains the majority of the input fields
column1 = [
    [Sg.vtop(Sg.Text('Warrant Builder v0.1 (beta)', size=(50, 2), font=("Arial", 20)))],

    [Sg.Text('Rank:'),
     Sg.Combo(ranks, key='RANK', default_value=ranks[1]),
     Sg.Text('Name:'),
     Sg.Input(key="NAME", size=(10, 1)),
     Sg.Text('Badge #:'),
     Sg.Input(key="BADGE", size=(10, 1), default_text="V"),
     Sg.Text('Case Number:', size=(12, 1)),
     Sg.Input(key="CASENUM", size=(20, 1), default_text="V")
     ],

    [Sg.Text('Court:'),
     Sg.Combo(courts, key='COURT', default_value=courts[0]),
     Sg.Text('Judge:'),
     Sg.Input(key="JUDGE", size=(20, 1))
     ],

    [Sg.vtop(Sg.Text('In possession of:', size=(12, 1))),
     Sg.Multiline(key="SUSPECT", size=(20, 4)),
     Sg.vtop(Sg.Text('On Premises:', size=(10, 1))),
     Sg.Multiline(key="PREMISES", size=(20, 4)),
     Sg.vtop(Sg.Text('In Vehicle(s):', size=(10, 1))),
     Sg.Multiline(key="VEHICLE", size=(20, 4))
     ],

    [Sg.vtop(Sg.Text("Property Sought:", size=(12, 1))),
     Sg.Multiline(key="PROPERTY", size=(90, 10))
     ],

    [Sg.vtop(Sg.Text("Common \nVerbiage:", size=(12, 2))),
     Sg.Checkbox("CellPhones", key='s1'),
     Sg.Checkbox("Computers", key='s2'),
     Sg.Checkbox("Residence", key='s3'),
     Sg.Checkbox("SocialMedia", key='s4'),
     Sg.Checkbox("Narcotics", key='s5'),
     Sg.Checkbox("Fraud", key='s6')
     ],

    [Sg.vtop(Sg.Text("Crimes:", size=(12, 1))),
     Sg.Multiline(key="CRIMES", size=(40, 5)),
     Sg.Column(dateCols)],

    [Sg.vtop(Sg.Text("Affidavit:", size=(12, 1))),
     Sg.Multiline(key="AFFIDAVIT", size=(90, 10))],

    [Sg.Checkbox(text=r[0], key='0', size=(90, 2))],
    [Sg.Checkbox(text=r[1], key='1', size=(90, 2))],
    [Sg.Checkbox(text=r[2], key='2', size=(90, 2))],
    [Sg.Checkbox(text=r[3], key='3', size=(90, 2))],
    [Sg.Checkbox(text=r[4], key='4', size=(90, 2))],
    [Sg.Checkbox(text=r[5], key='5', size=(90, 2))],
    [Sg.Radio(text=serviceTime[0], key='dayService', size=(90, 2), group_id='serviceTime')],
    [Sg.Radio(text=serviceTime[1], key='nightService', size=(90, 2), group_id='serviceTime')],
    [Sg.Text('Nighttime Justification:'), Sg.Input(key="NIGHTTIME_JUSTIFICATION")],
    [Sg.Button("Generate Warrant"), Sg.Exit()],

# Hidden values placed here
    [Sg.Input(key='PROPERTY_REASONS', visible=False)],
    [Sg.Input(key='TRAININGEXPERIENCE', visible=False)]
]



layout = [
    [Sg.Column(column1, scrollable=True, vertical_scroll_only=True, size=(1000, 790))]
]

window = Sg.Window("Warrant Builder V0.1", layout, size=(1010, 800), resizable=True, font=("Arial", 11))

# Rules that govern what happens when you press buttons
while True:
    event, values = window.read()
    if event == Sg.WIN_CLOSED or event == "Exit":
        break
    if event == "Generate Warrant":
# Check whether or not the boxes are checked and then output the value if True. Adds
# the values to a variable and then commits the variable to the hidden text element
        for check in rIndex:
            if window[check].Get() == True:
                rHolder = rHolder + window[check].Text + '\n'
        # for check in serviceIndex:
        #     if window[check].Get() == True:
        #         rHolder = rHolder + window[check].Text + '\n'
# Set the value of PROPERTY_REASONS to the values from the checkboxes
        values['PROPERTY_REASONS'] = rHolder
# Set remaining values for static variables
        values['TRAININGEXPERIENCE'] = TandESrc
        values['COUNTY'] = county
        docOut.render(values)
        output_path = Path(__file__).parent / f"./output/{values['CASENUM']}-search warrant.docx"
        docOut.save(output_path)
        Sg.popup("Warrant built, don't forget to proofread!", f"File has been saved to: {output_path}")
        break

window.close()
