from setuptools import setup
import sys

if sys.version_info.major == 2:
    open_cv = 'opencv-python==4.2.0.32'     # Last supported version for Python 2.7
else:
    open_cv = 'opencv-python'               # Latest available version

setup(
    name='imutils',
    packages=['imutils', 'imutils.video', 'imutils.io', 'imutils.feature', 'imutils.face_utils'],
    version='0.5.4',
    description='A series of convenience functions to make basic image processing functions such as translation, rotation, resizing, skeletonization, displaying Matplotlib images, sorting contours, detecting edges, and much more easier with OpenCV and both Python 2.7 and Python 3.',
    author='Adrian Rosebrock',
    author_email='adrian@pyimagesearch.com',
    url='https://github.com/jrosebr1/imutils',
    download_url='https://github.com/jrosebr1/imutils/tarball/0.1',
    keywords=['computer vision', 'image processing', 'opencv', 'matplotlib'],
    classifiers=[],
    scripts=['bin/range-detector'],
    install_requires=[
        'numpy', 
        'scipy', 
        'matplotlib', 
        open_cv
    ]
)
