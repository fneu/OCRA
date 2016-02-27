import collections
import cv2

from Misc import median

Rectangle = collections.namedtuple('Rectangle', ['x', 'y', 'w', 'h'])


class RectangleGroup:
    def __init__(self, *args):
        self.items = list(args)

    def boundary(self):
        if not self.items:
            return False

        x, y, w, h = self.items[0]
        r = x+w
        b = y+h

        for item in self.items:
            x = min(x, item.x)
            y = min(y, item.y)
            r = max(r, item.x+item.w)
            b = max(b, item.y+item.h)

        return Rectangle(x, y, r-x, b-y)

    def append(self, rectangle):
        self.items.append(rectangle)

    def overlaps_y(self, rectangle, margin=40):
        """
        whether or not this group and the given rectangle overlap in the
        y-dimension

        :param rectangle: rectangle that is not yet in the group
        :param margin:    margin in px
        :return:          true or False
        """
        boundary = self.boundary()
        return (rectangle.y < boundary.y + boundary.h + margin and
                rectangle.y + rectangle.h + margin > boundary.y)


def get_rectangles(image):
    """
    return Rectangles of Areas where Text is found

    :param image: cv2 image object (cv2.imread)
    :return:      list of rectangles of text areas
    """
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)  # grayscale
    _,thresh = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY_INV) # threshold
    kernel = cv2.getStructuringElement(cv2.MORPH_CROSS, (3, 3))
    dilated = cv2.dilate(thresh, kernel, iterations=13)  # dilate -> prev 13
    contours, hierarchy = cv2.findContours(dilated,
                                           cv2.RETR_EXTERNAL,
                                           cv2.CHAIN_APPROX_NONE)  # contours

    rectangles = []
    for contour in contours:
        rectangles.append(Rectangle(*cv2.boundingRect(contour)))
    return rectangles


def is_valid_rect(rectangle):
    if rectangle.w>300 and rectangle.h>300:
        return False
    elif rectangle.w<40 or rectangle.h<40:
        return False
    else:
        return True

def draw_rectangle(image, rectangle, color, width):
    """
    draw a rectangle into the image

    :param image:     cv2 image object
    :param rectangle: rectangle object to be drawn
    :param color:     tuple with RGB values
    :param width:     line width (int)
    """
    cv2.rectangle(image,
                  (rectangle.x, rectangle.y),
                  (rectangle.x+rectangle.w, rectangle.y+rectangle.h),
                  tuple(reversed(color)),  # cv2 uses BGR
                  width)


def group_rectangles(rectangles):
    """
    group rectangles into horizontal groups

    :param rectangles: list of rectangles
    :return:           list of RectangleGroups
    """
    rect_groups = []

    for rectangle in sorted(filter(is_valid_rect, rectangles),
                            key=lambda rect: rect.y):
        appended = False
        for rect_group in rect_groups:
            if rect_group.overlaps_y(rectangle):
                rect_group.append(rectangle)
                appended = True
                break

        if not appended:
            rect_groups.append(RectangleGroup(rectangle))

    for group in reversed(rect_groups):
        if len(group.items) <= 3:
            rect_groups.remove(group)

    return rect_groups


def trim_groups(rect_groups, margin=30):
    """
    some groups extend further to the left or right than others. These most
    like include some areas wrongly recognized as text.

    :param rect_groups: rectangle groups, for best results pass all groups of
                        one page
    :param margin:      margin in px
    :return:
    """
    left_edges = []
    right_edges = []

    for group in rect_groups:
        boundary = group.boundary()
        left_edges.append(boundary.x)
        right_edges.append(boundary.x+boundary.w)

    left_edge = median(left_edges) - margin
    right_edge = median(right_edges) + margin

    for group in rect_groups:
        for rectangle in reversed(group.items):
            if rectangle.x < left_edge or rectangle.x+rectangle.w > right_edge:
                group.items.remove(rectangle)

    return rect_groups


def split_lines(rectangle):
    """
    split a rectangle of a text area into rectangles of it's lines

    :param rectangle: bounding rectangle of a text area
    :return:          n rectangles containing it's lines
    """
    n = int(rectangle.h/53.+0.5)
    # lines may overlap but there should be white space anyway
    height = rectangle.h/n

    line_rectangle_list = []
    for i in range(n):
        line_rectangle_list.append(Rectangle(rectangle.x,
                                             rectangle.y + i * height,
                                             rectangle.w,
                                             height))
    return line_rectangle_list


def crop_lines(file_name):
    image = cv2.imread(file_name)
    text_areas = get_rectangles(image)
    blocks = group_rectangles(text_areas)
    text_blocks = trim_groups(blocks)

    page_crops = []

    for tb in text_blocks:
        line_rects = split_lines(tb.boundary())
        entry_crops = []

        for lt in line_rects:
            # NOTE: its [y: y + h, x: x + w] and *not* [x: x + w, y: y + h]
            rect_crop = image[lt.y: lt.y+lt.h, lt.x:lt.x+lt.w]
            entry_crops.append(rect_crop)
        page_crops.append(entry_crops)

    return page_crops
