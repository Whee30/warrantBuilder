#!/usr/bin/python3
#python tuple test
import PySimpleGUI as Sg


r = (
	"Were stolen or embezzled",
	"Were used as a means for committing a public offense.",
	"Is being possessed with the intent to use it as a means of committing a public offense",
	"Are in the possession of to whom it was delivered for the purpose of concealing it or\
 preventing it from being discovered",
	"Consists of any item or constitutes any evidence which tends to show that a public offense\
 has been committed, or tends to show that a particular person committed the public offense",
	"The person sought is the subject of an outstanding arrest warrant which offense occurred\
 on or about the day of , 20 in the County of Pima, State of Arizona",
	"In the daytime (excluding the time period between 10:00 p.m and 6:30 a.m)",
	"In the nighttime"
	)

rIndex = [0,1,2,3,4,5,6,7]

rHolder = ''''''

#print(r[3])

layout = [
    [Sg.Text('Select one of the following:')],
    [Sg.Checkbox(text=r[0], key=0)],
    [Sg.Checkbox(text=r[1], key=1)],
    [Sg.Checkbox(text=r[2], key=2)],
    [Sg.Checkbox(text=r[3], key=3)],
    [Sg.Checkbox(text=r[4], key=4)],
    [Sg.Checkbox(text=r[5], key=5)],
    [Sg.Checkbox(text=r[6], key=6)],
	[Sg.Checkbox(text=r[7], key=7)],
    [Sg.Button(button_text="Clear"), Sg.Button(button_text="Confirm"), Sg.Button(button_text="Exit")]
]

#  elif event == 'ON':
#         window ['checkbox']. Update (value = True)
#     elif event == 'OFF':
#         window ['checkbox']. Update (value = False)

Sg.theme('DarkGrey')

window = Sg.Window("Tuple selection", layout, resizable=True)

while True:
    event, values = window.read()
    if event == Sg.WIN_CLOSED or event == "Exit":
       break
    elif event == "Clear":
       for i in rIndex:
          window[i].update(value=False)
    # Trying to check whether or not the boxes are checked and then output the value if True
    elif event == 'Confirm':
       for check in rIndex:
          if window[check].Get() == True:
             print(window[check].Text + '\n')
             rHolder = rHolder + window[check].Text + '\n\n'
       print(rHolder)
       break
    





        
window.close()

