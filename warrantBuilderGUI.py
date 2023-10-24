import os
impor*t PySimpleGUI as sg
from pathlib import Path
from docxtpl import DocxTemplate
# YouTube tutorial for these functions
# https://www.youtube.com/watch?v=fziZXbeaegc


# Where the source template file lives
templatePath = Path(__file__).parent / "template.docx"
# Output file variable
docOut = DocxTemplate(templatePath)

#Assign the content of the source files to variables
resSrc = open('./sources/residence.txt').read()
vehSrc = open('./sources/vehicle.txt').read()
socSrc = open('./sources/social.txt').read()


# User input variables
# userName = input("Please enter your name:")
# caseNum = input("Please enter your case number:")

layout = [
    [sg.Text("Name"), sg.Input(key="NAME")],
    [sg.Text("Case Number"), sg.Input(key="CASENUM_FIELD")],
    [sg.Button("Generate Warrant"), sg.Exit()],
    [sg.Checkbox("Vehicle", key='c1')],
    [sg.Checkbox("Residence", key='c2')],
    [sg.Checkbox("Social", key='c3')],
    
]
    
window = sg.Window("Warrant Builder V0.1", layout)

while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED or event == "Exit":
        break
    if event == "Generate Warrant":
        value["NAME"]
        docOut.render
        print(event, values)
        
window.close()

# Create a variable that will name the output file
#fullPath = caseNum + " search warrant.docx"

# Tuple containing reasons, checkboxes will call these
#r = (
#	"Were stolen or embezzled",
#	"Were used as a means for committing a public offense.",
#	"Is being possessed with the intent to use it as a means of committing a public offense",
#	"Are in the possession of to whom it was delivered for the purpose of concealing it or preventing it from being discovered",
#	"Consists of any item or constitutes any evidence which tends to show that a public offense has been committed, or tends to show that a particular person committed the public offense",
#	"The person sought is the subject of an outstanding arrest warrant which offense occurred on or about the day of , 20 in the County of Pima, State of Arizona",
#	"In the daytime (excluding the time period between 10:00 p.m and 6:30 a.m)",
#	"In the nighttime"
#	)
	

# Can only render once! Only the last render call will happen and the previous calls will be wiped out
#docOut.render({
#    "NAME": userName,
#    "RESIDENCE": resSrc,
#    "VEHICLE": vehSrc,
#    "SOCIAL": socSrc,
#    "CASENUMBER": caseNum
#})

# Save the rendered changes to the file based on the case number entered.
#docOut.save(Path(__file__).parent / fullPath)

#input('Press ENTER to exit')