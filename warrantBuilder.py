import os
from pathlib import Path
from docxtpl import DocxTemplate

# Where the source template file lives
templatePath = Path(__file__).parent / "template.docx"
# Output file variable
docOut = DocxTemplate(templatePath)

#Assign the content of the source files to variables
resSrc = open('./sources/residence.txt').read()
vehSrc = open('./sources/vehicle.txt').read()
socSrc = open('./sources/social.txt').read()


# User input variables
userName = input("Please enter your name:")
caseNum = input("Please enter your case number:")

# Create a variable that will name the output file
fullPath = caseNum + " search warrant.docx"


# Can only render once! Only the last render call will happen and the previous calls will be wiped out
docOut.render({
    "NAME": userName,
    "RESIDENCE": resSrc,
    "VEHICLE": vehSrc,
    "SOCIAL": socSrc,
    "CASENUMBER": caseNum
})

# Save the rendered changes to the file based on the case number entered.
docOut.save(Path(__file__).parent / fullPath)

input('Press ENTER to exit')