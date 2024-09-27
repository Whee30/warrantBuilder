The first version of this project was born into PySimpleGUI. After they went closed source, I pivoted to PyQT6. The interface is cleaner, but the progress stalled while the learning curve spiked.

The goal is to have a self-contained application to speed along the process of warrant writing so that the "boots on the ground" can focus on the facts of the case vs. finding the right template from someone's thumbdrive. 

The common verbiage tab is dynamically populated from a sources.py document which contains lists for each "topic" of verbiage. The importing and handling of the topics is currently explicitly declared (adding a new topic to the sources.py will not add a new topic to the Common Verbiage tab). Refining the code to accommodate for additional lists being added to sources.py and handling them appropriately in-app is the end goal.

Open to suggestions, this isn't intended as a public release just yet, it is unfinished and built specifically for one agency... however if someone else gets use of it please let me know!

As of 09/26/24, the program is functional. Common verbiage content needs to be brought into the 21st century but the actual function is there.
