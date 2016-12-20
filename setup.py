from distutils.core import setup

setup(
    name='imutils',
    packages=['imutils', 'imutils.video', 'imutils.io'],
    version='0.3.8',
    description='A series of convenience functions to make basic image processing functions such as translation, rotation, resizing, skeletonization, displaying Matplotlib images, sorting contours, detecting edges, and much more easier with OpenCV and both Python 2.7 and Python 3.',
    author='Adrian Rosebrock',
    author_email='adrian@pyimagesearch.com',
    url='https://github.com/jrosebr1/imutils',
    download_url='https://github.com/jrosebr1/imutils/tarball/0.1',
    keywords=['computer vision', 'image processing', 'opencv', 'matplotlib'],
    classifiers=[],
    scripts=['bin/range-detector'],
)
