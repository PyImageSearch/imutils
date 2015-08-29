# author:    Adrian Rosebrock
# website:   http://www.pyimagesearch.com

# import the necessary packages
from __future__ import print_function
import cv2
import re

def find_function(name, pretty_print=True, module=None):
	# if the module is None, initialize it to to the root `cv2`
	# library
	if module is None:
		module = cv2

	# grab all function names that contain `name` from the module
	p = ".*{}.*".format(name)
	filtered = filter(lambda x: re.search(p, x, re.IGNORECASE), dir(module))
	
	# check to see if the filtered names should be returned to the
	# calling function
	if not pretty_print:
		return filtered

	# otherwise, loop over the function names and print them
	for (i, funcName) in enumerate(filtered):
		print("{}. {}".format(i + 1, funcName))