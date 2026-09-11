import subprocess
import os


os.mkdir("hidden_folder")

subprocess.run(["attrib", "+h", r"hidden_folder"])

with open('hidden_folder/output.txt', 'w') as file:
    file.write("Hello world")
