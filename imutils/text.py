import cv2


def put_text(img, text, org, font_face, font_scale, color, thickness=1, line_type=8, bottom_left_origin=False):
    """Utility for drawing text with line breaks

    :param img: Image.
    :param text: Text string to be drawn.
    :param org: Bottom-left corner of the first line of the text string in the image.
    :param font_face: Font type. One of FONT_HERSHEY_SIMPLEX, FONT_HERSHEY_PLAIN, FONT_HERSHEY_DUPLEX,
                          FONT_HERSHEY_COMPLEX, FONT_HERSHEY_TRIPLEX, FONT_HERSHEY_COMPLEX_SMALL,
                          FONT_HERSHEY_SCRIPT_SIMPLEX, or FONT_HERSHEY_SCRIPT_COMPLEX, where each of the font ID’s
                          can be combined with FONT_ITALIC to get the slanted letters.
    :param font_scale: Font scale factor that is multiplied by the font-specific base size.
    :param color: Text color.
    :param thickness: Thickness of the lines used to draw a text.
    :param line_type: Line type. See the line for details.
    :param bottom_left_origin: When true, the image data origin is at the bottom-left corner.
                               Otherwise, it is at the top-left corner.
    :return: None; image is modified in place
    """
    # Break out drawing coords
    x, y = org

    # Break text into list of text lines
    text_lines = text.split('\n')

    # Get height of text lines in pixels (height of all lines is the same)
    _, line_height = cv2.getTextSize('', font_face, font_scale, thickness)[0]
    # Set distance between lines in pixels
    line_gap = line_height // 3

    for i, text_line in enumerate(text_lines):
        # Find total size of text block before this line
        line_y_adjustment = i * (line_gap + line_height)

        # Move text down from original line based on line number
        if not bottom_left_origin:
            line_y = y + line_y_adjustment
        else:
            line_y = y - line_y_adjustment

        # Draw text
        cv2.putText(img,
                    text=text_lines[i],
                    org=(x, line_y),
                    fontFace=font_face,
                    fontScale=font_scale,
                    color=color,
                    thickness=thickness,
                    lineType=line_type,
                    bottomLeftOrigin=bottom_left_origin)


def put_centered_text(img, text, font_face, font_scale, color, thickness=1, line_type=8):
    """Utility for drawing vertically & horizontally centered text with line breaks

    :param img: Image.
    :param text: Text string to be drawn.
    :param font_face: Font type. One of FONT_HERSHEY_SIMPLEX, FONT_HERSHEY_PLAIN, FONT_HERSHEY_DUPLEX,
                          FONT_HERSHEY_COMPLEX, FONT_HERSHEY_TRIPLEX, FONT_HERSHEY_COMPLEX_SMALL,
                          FONT_HERSHEY_SCRIPT_SIMPLEX, or FONT_HERSHEY_SCRIPT_COMPLEX, where each of the font ID’s
                          can be combined with FONT_ITALIC to get the slanted letters.
    :param font_scale: Font scale factor that is multiplied by the font-specific base size.
    :param color: Text color.
    :param thickness: Thickness of the lines used to draw a text.
    :param line_type: Line type. See the line for details.
    :return: None; image is modified in place
    """
    # Save img dimensions
    img_h, img_w = img.shape[:2]

    # Break text into list of text lines
    text_lines = text.split('\n')

    # Get height of text lines in pixels (height of all lines is the same; width differs)
    _, line_height = cv2.getTextSize('', font_face, font_scale, thickness)[0]
    # Set distance between lines in pixels
    line_gap = line_height // 3

    # Calculate total text block height for centering
    text_block_height = len(text_lines) * (line_height + line_gap)
    text_block_height -= line_gap  # There's one less gap than lines

    for i, text_line in enumerate(text_lines):
        # Get width of text line in pixels (height of all lines is the same)
        line_width, _ = cv2.getTextSize(text_line, font_face, font_scale, thickness)[0]

        # Center line with image dimensions
        x = (img_w - line_width) // 2
        y = (img_h + line_height) // 2

        # Find total size of text block before this line
        line_adjustment = i * (line_gap + line_height)

        # Adjust line y and re-center relative to total text block height
        y += line_adjustment - text_block_height // 2 + line_gap

        # Draw text
        cv2.putText(img,
                    text=text_lines[i],
                    org=(x, y),
                    fontFace=font_face,
                    fontScale=font_scale,
                    color=color,
                    thickness=thickness,
                    lineType=line_type)
