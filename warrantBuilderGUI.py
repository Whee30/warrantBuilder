#!/usr/bin/python
import PySimpleGUI as Sg
from pathlib import Path
from docxtpl import DocxTemplate

# YouTube tutorial for these functions
# https://www.youtube.com/watch?v=fziZXbeaegc


# Where the source template file lives
templatePath = Path(__file__).parent / "WarrantSkeleton.docx"
# Output file variable
docOut = DocxTemplate(templatePath)

# Assign the content of the source files to variables
resSrc = open('./sources/residence.txt').read()
vehSrc = open('./sources/vehicle.txt').read()
socSrc = open('./sources/social.txt').read()

# Defines options in a multi-select list
s = (
    "Cellphones",
    "Residences",
    "Vehicles"
    )

# Tuple containing reasons, checkboxes will call these
r = (
    "Were stolen or embezzled",
    "Were used as a means for committing a public offense.",
    "Is being possessed with the intent to use it as a means of committing a public offense",
    "Are in the possession of to whom it was delivered for the purpose of concealing it or preventing it from "
    "being discovered",
    "Consists of any item or constitutes any evidence which tends to show that a public offense has been committed,"
    " or tends to show that a particular person committed the public offense",
    "The person sought is the subject of an outstanding arrest warrant which offense occurred on or about the day of"
    " , 20 in the County of Pima, State of Arizona",
    "In the daytime (excluding the time period between 10:00 p.m and 6:30 a.m)",
    "In the nighttime"
    )

# Define available ranks for the dropdown
ranks = ["Ofc.", "Det.", "Sgt."]
# Define available courts for the dropdown
courts = ["Oro Valley Magistrate Court", "Pima County Superior Court", "Pima County Justice Court"]

dateCols = [
    [Sg.vtop(Sg.Text("Date Range:", size=(10, 1)))],
    [Sg.CalendarButton(button_text="Start Date", key="STARTTIME", format='%a %B %d, %Y', target='START_TIME'),
     Sg.Input(key="START_TIME", default_text="From", size=(18, 1))],

    [Sg.CalendarButton(button_text="End Date", key="ENDTIME", format='%a %B %d, %Y', target='END_TIME'),
     Sg.Input(key="END_TIME", default_text="To", size=(18, 1))]
]

column1 = [
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
     Sg.Multiline(key="PROPERTY", size=(100, 10))
     ],

    [Sg.vtop(Sg.Text("Crimes:", size=(12, 1))),
     Sg.Multiline(key="CRIMES", size=(40, 5)),
     Sg.Column(dateCols)],

    [Sg.Listbox(s, size=(20, 4), key='s1', enable_events=True),
     Sg.Checkbox("Residence", key='s2'),
     Sg.Checkbox("Social", key='s3')
     ],
    [Sg.Checkbox(text=f"{r[0]}", key='r[0]')],
    [Sg.Checkbox(text=f"{r[1]}", key='r[1]')],
    [Sg.Checkbox(text=f"{r[2]}", key='r[2]')],
    [Sg.Checkbox(text=f"{r[3]}", key='r[3]')],
    [Sg.Checkbox(text=f"{r[4]}", key='r[4]')],
    [Sg.Checkbox(text=f"{r[5]}", key='r[5]')],
    [Sg.Button("Generate Warrant"), Sg.Exit()],
]



layout = [
    [Sg.Column(column1, scrollable=True, vertical_scroll_only=True, size=(990, 590))]
]

window = Sg.Window("Warrant Builder V0.1", layout, size=(1000, 600), resizable=True)

while True:
    event, values = window.read()
    if event == Sg.WIN_CLOSED or event == "Exit":
        break
#    if event == "START_TIME":
#        window['startText'].update(window['START_TIME'].value)
    if event == "Generate Warrant":
        docOut.render(values)
        output_path = Path(__file__).parent / f"output/{values['CASENUM']}-search warrant.docx"
        docOut.save(output_path)
        Sg.popup("Warrant built, don't forget to proofread!", f"File has been saved to: {output_path}")
        break
        
window.close()
