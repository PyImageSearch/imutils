# author:    Adrian Rosebrock
# website:   http://www.pyimagesearch.com

# import the necessary packages
from __future__ import print_function
from imutils import paths

# loop over the image paths in the previous 'demo_images'
# directory and print the paths to the terminal
for imagePath in paths.list_images("../demo_images"):
    print(imagePath)
