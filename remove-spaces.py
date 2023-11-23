import os

# get a list of all file names in the current directory
filenames = os.listdir()

# iterate over all file names
for filename in filenames:
    # replace spaces in the file name with underscores
    new_filename = filename.replace(" ", "_")
    # rename the file
    os.rename(filename, new_filename)

