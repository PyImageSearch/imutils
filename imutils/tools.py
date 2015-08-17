# author:    Adrian Rosebrock
# website:   http://www.pyimagesearch.com


import cv2


class ClickCropper:
    def __init__(self, image):
        self.image = image
        self.image_rectangle = image.copy()
        self.positions = []
        self.state = None

    def mouse_callback(self, event, x, y, flags, param):
        # Saving the click coordinates
        if event == cv2.EVENT_LBUTTONUP:
            if not self.state:
                self.state = "clicked"
                self.positions.append((x, y))
            elif self.state == "clicked":
                self.positions.append((x, y))
                self.state = "double_clicked"

        # Showing the selected area in real time
        # with green rectangle
        elif event == cv2.EVENT_MOUSEMOVE:
            if self.state == "clicked":
                self.image_rectangle = self.image.copy()
                x1, y1 = self.positions[0]
                cv2.rectangle(self.image_rectangle, (x1, y1), (x, y), (0, 255, 0), 2)

        # Canceling the selection if right clicked
        elif event == cv2.EVENT_RBUTTONUP:
            if self.state == "double_clicked":
                self.image_rectangle = self.image.copy()
                self.positions = []
                self.state = None

    def crop(self):
        # Ensuring that we got only 2 coordinates
        if len(self.positions) != 2:
            return None

        x1, y1 = self.positions[0]
        x2, y2 = self.positions[1]

        # Swapping coordinates if selected from
        # right-to-left or bottom-to-top
        if x1 > x2:
            x1, x2 = x2, x1

        if y1 > y2:
            y1, y2 = y2, y1

        return self.image[y1:y2, x1:x2]


def click_and_crop(image):
    cropper = ClickCropper(image)
    cv2.namedWindow("Cropper")
    cv2.setMouseCallback("Cropper", cropper.mouse_callback)

    while True:
        cv2.imshow("Cropper", cropper.image_rectangle)

        key = cv2.waitKey(1) & 0xFF

        if key is ord('q'):
            cv2.destroyWindow("Cropper")
            return image
        elif key is ord('c'):
            cropped_image = cropper.crop()

            if cropped_image is not None:
                cv2.destroyWindow("Cropper")
                return cropped_image
