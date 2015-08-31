# import the necessary packages
import numpy as np
import base64
import json

def base64_encode_image(a):
	# return a JSON-encoded list of the base64 encoded image, image data
	# type, and image shape
	return json.dumps([base64_encode_array(a), str(a.dtype), a.shape])

def base64_decode_image(a):
	# grab the array, data type, and shape from the JSON-decoded object,
	# then set the correct data type and reshape the matrix into an image
	(a, dtype, shape) = json.loads(a)
	a = base64_decode_array(a, dtype).reshape(shape)

	# return the loaded image
	return a

def base64_encode_array(a):
	# return the base64 encoded array
	return base64.b64encode(a)

def base64_decode_array(a, dtype):
	# decode and return the array
	return np.frombuffer(base64.decodestring(a), dtype=dtype)