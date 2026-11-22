from io import open
from os import path

from setuptools import setup


with open(path.join(path.dirname(__file__), 'README.md'),
          encoding='utf-8') as readme:
    long_description = readme.read()

setup(
    name='imutils',
    packages=['imutils', 'imutils.video', 'imutils.io', 'imutils.feature', 'imutils.face_utils'],
    version='0.5.4',
    description='A series of convenience functions to make basic image processing functions such as translation, rotation, resizing, skeletonization, displaying Matplotlib images, sorting contours, detecting edges, and much more easier with OpenCV and both Python 2.7 and Python 3.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    license='MIT',
    license_files=['LICENSE.txt'],
    author='Adrian Rosebrock',
    author_email='adrian@pyimagesearch.com',
    url='https://github.com/jrosebr1/imutils',
    download_url='https://github.com/jrosebr1/imutils/tarball/0.1',
    keywords=['computer vision', 'image processing', 'opencv', 'matplotlib'],
    classifiers=[],
    scripts=['bin/range-detector'],
)
