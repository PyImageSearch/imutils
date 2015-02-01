# imutils
A series of convenience functions to make basic image processing functions such as translation, rotation, resizing, skeletonization, and displaying Matplotlib images easier with OpenCV and Python.

For more information, along with a detailed code review check out the following posts on the [PyImageSearch.com](http://www.pyimagesearch.com) blog:

- [http://www.pyimagesearch.com/2015/02/02/just-open-sourced-personal-imutils-package-series-opencv-convenience-functions/](http://www.pyimagesearch.com/2015/02/02/just-open-sourced-personal-imutils-package-series-opencv-convenience-functions/)

## Translation
Translation is the shifting of an image in either the *x* or *y* direction. To translate an image in OpenCV you would need to supply the *(x, y)*-shift, denoted as *(t<sub>x</sub>, t<sub>y</sub>)* to construct the translation matrix *M*:

![Translation equation](docs/images/translation_eq.png?raw=true)

And from there, you would need to apply the `cv2.warpAffine` function.

Instead of manually constructing the translation matrix *M* and calling `cv2.warpAffine`, you can simply make a call to the `translate` function of `imutils`.

#### Example:
<pre># translate the image x=25 pixels to the right and y=75 pixels up
translated = imutils.translate(workspace, 25, -75)</pre>

#### Output:
<img src="docs/images/translation.png?raw=true" alt="Translation example"/ style="max-width: 500px;">

## Rotation
Rotating an image in OpenCV is accomplished by making a call to `cv2.getRotationMatrix2D` and `cv2.warpAffine`. Further care has to be taken to supply the *(x, y)*-coordinate of the point the image is to be rotated about. These calculation calls can quickly add up and make your code bulky and less readable. The `rotate` function in `imutils` helps resolve this problem.

#### Example:
<pre># loop over the angles to rotate the image
for angle in xrange(0, 360, 90):
	# rotate the image and display it
	rotated = imutils.rotate(bridge, angle=angle)
	cv2.imshow("Angle=%d" % (angle), rotated)</pre>

#### Output:
<img src="docs/images/rotation.png?raw=true" alt="Rotation example"/ style="max-width: 500px;">

## Resizing
Resizing an image in OpenCV is accomplished by calling the `cv2.resize` function. However, special care needs to be taken to ensure that the aspect ratio is maintained.  This `resize` function of `imutils` maintains the aspect ratio and provides the keyword arguments `width` and `height` so the image can be resized to the intended width/height while (1) maintaining aspect ratio and (2) ensuring the dimensions of the image do not have to be explicitly computed by the developer.

Another optional keyword argument, `inter`, can be used to specify interpolation method as well.

#### Example:
<pre># loop over varying widths to resize the image to
for width in (400, 300, 200, 100):
	# resize the image and display it
	resized = imutils.resize(workspace, width=width)
	cv2.imshow("Width=%dpx" % (width), resized)</pre>

#### Output:
<img src="docs/images/resizing.png?raw=true" alt="Resizing example"/ style="max-width: 500px;">

## Skeletonization
Skeletonization is the process of constructing the "topological skeleton" of an object in an image, where the object is presumed to be white on a black background. OpenCV does not provide a function to explicity construct the skeleton, but does provide the morphological and binary functions to do so.

For convenience, the `skeletonize` function of `imutils` can be used to construct the topological skeleton of the image.

The first argument, `size` is the size of the structuring element kernel. An optional argument, `structuring`, can be used to control the structuring element -- it defaults to `cv2.MORPH_RECT`	, but can be any valid structuring element.

#### Example:
<pre># skeletonize the image
gray = cv2.cvtColor(logo, cv2.COLOR_BGR2GRAY)
skeleton = imutils.skeletonize(gray, size=(3, 3))
cv2.imshow("Skeleton", skeleton)</pre>

#### Output:
<img src="docs/images/skeletonization.png?raw=true" alt="Skeletonization example"/ style="max-width: 500px;">

## Displaying with Matplotlib
In the Python bindings of OpenCV, images are represented as NumPy arrays in BGR order. This works fine when using the `cv2.imshow` function. However, if you intend on using Matplotlib, the `plt.imshow` function assumes the image is in RGB order. A simple call to `cv2.cvtColor` will resolve this problem, or you can use the `opencv2matplotlib` conveince function.

#### Example:
<pre># INCORRECT: show the image without converting color spaces
plt.figure("Incorrect")
plt.imshow(cactus)

# CORRECT: convert color spaces before using plt.imshow
plt.figure("Correct")
plt.imshow(imutils.opencv2matplotlib(cactus))
plt.show()</pre>

#### Output:
<img src="docs/images/matplotlib.png?raw=true" alt="Matplotlib example"/ style="max-width: 500px;">