# Setting up Folders for Text Cleaning
1. Download the folders you wish to clean from the eebo Box
2. Drag them to the directory you plan on using
3. Unzip the folders and rename them so that they have the right P tag at the end
  * E.g. A2 -> A2\_P4
4. inside each unzipped folder add subfolders with the following labels:
  * the name of the folder + \_cleaned (E.g.A2\_cleaned)
  * output
5. Within the subfolder folder name + \_cleaned, add two more subfolders:
  * cleaned
    * If VARD crashes, place all of the csvs that have already been normalized in this folder before running the script again
  * uncleaned
    * the main.py script will remove all csvs over 1000kb and place them in this folder

# Useful Tips for Text Cleaning
1. The shortcut for renaming a folder on windows is `f2`
2. The shortcut for moving from a folder to its parent directory on windows is `Alt + up arrow`
3. Copying and pasting the subfolders in steps 4 and 5 will save a lot of time
4. Check the script every once in a while to see if a new developer token is needed
