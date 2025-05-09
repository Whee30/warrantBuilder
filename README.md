Built with PyQT6 and docxtpl. The goal is to have a self-contained application to speed along the process of warrant writing so that the "boots on the ground" can focus on the facts of the case vs. finding the right template from someone's thumbdrive. 

The common verbiage tab is dynamically populated from a cv_sources.json document which contains lists for each "topic" of verbiage. The importing and handling of the topics is now dynamically generated! If you need to add or modify a category of information, the first entry of the list category should be the title you want printed on the button. This list should also be added in whatever order you want it to appear in the "list of lists" in the program. The program will iterate through the json, build a button based on the first entry of each list and populate the verbiage with checkboxes appropriately. The order that this verbiage will be populated in the warrant is top down, so keep that in mind if you format your lists with a specific order in mind.

11/07/24 - Added a tab for Training and Experience to allow the user to see what the current value is. This value can be saved from the program or the currently saved value can be reloaded if the user makes a mistake during editing.

11/07/24 - Added a previous warrants tab to show previously completed warrants. You can load the previous warrant from JSON back into the builder. Useful for cases involving numerous similar warrants with slightly different details. 

11/30/24 - removed direct references to a specific agency. Script should be modified to associate to your specific agency if you intend on using it.

05/08/25 - converted the common verbiage source to json to simplify the process of inporting the verbiage. Added settings.json which will now populate the rank, county, court, agency and state variables accordingly. This enables easy modification for people who don't want to comb through 800 lines of python. This also makes distribution of self-contained executables possible while maintaining the ability to modify the values. settings.json will be stored in the "sources" directory.

Open to suggestions, if someone else gets use of it please let me know!
