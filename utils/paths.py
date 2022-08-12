import os

USERDATA = ""
FOLDERNAME = "Parrot-USTVGO"
if os.name == 'nt': USERDATA = os.environ['APPDATA']
else:
    USERDATA = os.environ['HOME']
    FOLDERNAME = ".Parrot-USTVGO"

# Folder Paths
USERDATA = os.path.join(USERDATA, FOLDERNAME)
DB_FOLDER = os.path.join(USERDATA, "DB")

# If folders dont exist create them
if not os.path.exists(USERDATA): os.makedirs(USERDATA)
if not os.path.exists(DB_FOLDER): os.makedirs(DB_FOLDER)