Built with PyQT6 and docxtpl, needs python 3.9x. Working on figuring out how to translate the GUI to a modern version of Python, but PyQT6 isn't supported it doesn't look like.

The first version of this project was born into PySimpleGUI. After they went closed source, I pivoted to PyQT6. The interface is cleaner, but the progress stalled while the learning curve spiked.

The goal is to have a self-contained application to speed along the process of warrant writing so that the "boots on the ground" can focus on the facts of the case vs. finding the right template from someone's thumbdrive. 

The common verbiage tab is dynamically populated from a cvSources.py document which contains lists for each "topic" of verbiage. The importing and handling of the topics is now dynamically generated! If you need to add or modify a category of information, the first entry of the list category should be the title you want printed on the button. This list should also be added in whatever order you want it to appear in the "list of lists" at the bottom of the document. The program will iterate through ths list of lists, build a button based on the first entry of that chil list and populate the verbiage with checkboxes appropriately. The order that this verbiage will be populated in the warrant is top down, so keep that in mind if you format your lists with a specific order in mind.

11/07/24 - Added a tab for Training and Experience to allow the user to see what the current value is. This value can be saved from the program or the currently saved value can be reloaded if the user makes a mistake during editing.

11/07/24 - Added a previous warrants tab to show previously completed warrants. You can load the previous warrant from JSON back into the builder. Useful for cases involving numerous similar warrants with slightly different details. 

11/30/24 - removed direct references to a specific agency. Script should be modified to associate to your specific agency if you intend on using it. Future plans include... get this... a warrant builder *builder*.

05/07/25 - working on exporting the court/county/etc customizations to an external JSON so that a self-contained executable can be useful to others who don't want to mess with learning to edit the python.

Open to suggestions, this isn't intended as a public release just yet, it is unfinished and built specifically for one agency... however if someone else gets use of it please let me know!
