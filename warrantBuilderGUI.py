import os
import PySimpleGUI as sg
from textwrap import wrap
from pathlib import Path
from docxtpl import DocxTemplate

# YouTube tutorial for these functions
# https://www.youtube.com/watch?v=fziZXbeaegc


# Where the source template file lives
templatePath = Path(__file__).parent / "WarrantSkeleton.docx"
# Output file variable
docOut = DocxTemplate(templatePath)

#Assign the content of the source files to variables
resSrc = open('./sources/residence.txt').read()
vehSrc = open('./sources/vehicle.txt').read()
socSrc = open('./sources/social.txt').read()

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
	"Are in the possession of to whom it was delivered for the purpose of concealing it or preventing it from being discovered",
	"Consists of any item or constitutes any evidence which tends to show that a public offense has been committed, or tends to show that a particular person committed the public offense",
	"The person sought is the subject of an outstanding arrest warrant which offense occurred on or about the day of , 20 in the County of Pima, State of Arizona",
	"In the daytime (excluding the time period between 10:00 p.m and 6:30 a.m)",
	"In the nighttime"
	)

ranks = ["Ofc.","Det.","Sgt."]

layout = [
    [sg.Text('Rank:'),
    sg.Combo(ranks, key='RANK'), 
    sg.Text('Name:'), 
    sg.Input(key="NAME", size=(10,1)), 
    sg.Text('Badge #:'), 
    sg.Input(key="BADGE", size=(10,1)),
    sg.Text('Case Number:', size=(12,1)), 
    sg.Input(key="CASENUM", size=(20,1))],
    [sg.Text('Suspect Name:', size=(12,1)), 
    sg.Input(key="SUSPECT", size=(20,1))],
    [sg.Listbox(s, size=(20, 4), key='s1', enable_events=True),
    sg.Checkbox("Residence", key='s2'),
    sg.Checkbox("Social", key='s3')],
    [sg.Checkbox(text=f"{r[0]}", key='r[0]')],
    [sg.Checkbox(text=f"{r[1]}", key='r[1]')],
	[sg.Checkbox(text=f"{r[2]}", key='r[2]')],
	[sg.Checkbox(text=f"{r[3]}", key='r[3]')],
	[sg.Checkbox(text=f"{r[4]}", key='r[4]')],
	[sg.Checkbox(text=f"{r[5]}", key='r[5]')],
    [sg.Button("Generate Warrant"), sg.Exit()],

    
]
    
window = sg.Window("Warrant Builder V0.1", layout, size=(800, 600))

while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED or event == "Exit":
        break
    if event == "Generate Warrant":
        docOut.render(values)
        output_path = Path(__file__).parent / f"output/{values['CASENUM']}-search warrant.docx"
        docOut.save(output_path)
        sg.popup("Warrant built, don't forget to proofread!", f"File has been saved to: {output_path}")
        break
        
window.close()
