# author:    Adam Spannbauer

# USAGE
# python text_demo.py -i ../demo_images/bridge.jpg
# python text_demo.py -i ../demo_images/bridge.jpg -c 0

# import the necessary packages
import argparse
import cv2
import imutils.text

# construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required=True, help="path to input image")
ap.add_argument("-c", "--center", default=1, type=int,
                help="Contrast, positive value for more contrast")
ap.add_argument("-x", default=5,
                help="X coordinate for text. Used if center == 0")
ap.add_argument("-y", default=25,
                help="Y coordinate for text. Used if center == 0")
args = vars(ap.parse_args())

# read in image to draw text on
image = cv2.imread(args['image'])

if args['center']:
    # draw centered text with a default font
    imutils.text.put_centered_text(image,
                                   'imutils.text\ndemo\noutput',
                                   font_face=cv2.FONT_HERSHEY_SIMPLEX,
                                   font_scale=1,
                                   color=(0, 255, 0),
                                   thickness=2)
else:
    # draw location specific text with a default font
    imutils.text.put_text(image,
                          'imutils.text\ndemo\noutput',
                          (args['x'], args['y']),
                          font_face=cv2.FONT_HERSHEY_SIMPLEX,
                          font_scale=1,
                          color=(0, 255, 0),
                          thickness=2)

# display resulting image with text
cv2.imshow('Image with Text', image)
cv2.waitKey(0)
