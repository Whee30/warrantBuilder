Built with PyQT6 and docxtpl, needs python 3.9x. Working on figuring out how to translate the GUI to a modern version of Python, but PyQT6 isn't supported it doesn't look like.

The first version of this project was born into PySimpleGUI. After they went closed source, I pivoted to PyQT6. The interface is cleaner, but the progress stalled while the learning curve spiked.

The goal is to have a self-contained application to speed along the process of warrant writing so that the "boots on the ground" can focus on the facts of the case vs. finding the right template from someone's thumbdrive. 

The common verbiage tab is dynamically populated from a cvSources.py document which contains lists for each "topic" of verbiage. The importing and handling of the topics is now dynamically generated! If you need to add or modify a category of information, the first entry of the list category should be the title you want printed on the button. This list should also be added in whatever order you want it to appear in the "list of lists" at the bottom of the document. The program will iterate through ths list of lists, build a button based on the first entry of that chil list and populate the verbiage with checkboxes appropriately. The order that this verbiage will be populated in the warrant is top down, so keep that in mind if you format your lists with a specific order in mind.

Open to suggestions, this isn't intended as a public release just yet, it is unfinished and built specifically for one agency... however if someone else gets use of it please let me know!

As of 09/26/24, the program is functional. Common verbiage content needs to be brought into the 21st century but the actual function is there.
