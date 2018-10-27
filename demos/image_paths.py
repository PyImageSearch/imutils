# author:    Adrian Rosebrock
# website:   http://www.pyimagesearch.com

# USAGE
# from the demos folder:
# python image_paths.py

# import the necessary packages
from __future__ import print_function
# You'll need to force '../imutils' into the system path if testing
from imutils import paths

# loop over the image paths in the previous 'demo_images'
# directory and print the paths to the terminal
for imagePath in paths.list_images("../demo_images"):
    print(imagePath)

print('\nUsing `list_files` with a jpg file extension filter:\n')

# validExts must be a tuple
for imagePath in paths.list_files("../demo_images", validExts=('.jpg',)):
    print(imagePath)

print('\nUsing `list_files` with a contains filter:\n')

# validExts must be a tuple
for imagePath in paths.list_files("../demo_images", contains='bridge'):
    print(imagePath)
