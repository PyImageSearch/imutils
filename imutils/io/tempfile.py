# import the necessary packages
import uuid
import os

class TempFile:
	def __init__(self, basePath="./", ext=".jpg"):
		# expose the file name separately from its parent directory
		self.filename = "{rand}{ext}".format(rand=str(uuid.uuid4()), ext=ext)

		# construct the file path
		self.path = "{base_path}/{filename}".format(base_path=basePath,
			filename=self.filename)

	def cleanup(self):
		# remove the file
		os.remove(self.path)
