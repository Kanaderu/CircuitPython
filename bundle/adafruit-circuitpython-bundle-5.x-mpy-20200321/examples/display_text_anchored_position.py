"""
This examples shows the use of anchor_point and anchored_position.
"""
import board
import terminalio
from adafruit_display_text import label
import displayio

DISPLAY_WIDTH = 320
DISPLAY_HEIGHT = 240
TEXT = "Hello"

text_area_top_left = label.Label(terminalio.FONT, text=TEXT)
text_area_top_left.anchor_point = (0.0, 0.0)
text_area_top_left.anchored_position = (10, 10)

text_area_top_middle = label.Label(terminalio.FONT, text=TEXT)
text_area_top_middle.anchor_point = (0.5, 0.0)
text_area_top_middle.anchored_position = (DISPLAY_WIDTH / 2, 10)

text_area_top_right = label.Label(terminalio.FONT, text=TEXT)
text_area_top_right.anchor_point = (1.0, 0.0)
text_area_top_right.anchored_position = (DISPLAY_WIDTH - 10, 10)

text_area_middle_left = label.Label(terminalio.FONT, text=TEXT)
text_area_middle_left.anchor_point = (0.0, 0.5)
text_area_middle_left.anchored_position = (10, DISPLAY_HEIGHT / 2)

text_area_middle_middle = label.Label(terminalio.FONT, text=TEXT)
text_area_middle_middle.anchor_point = (0.5, 0.5)
text_area_middle_middle.anchored_position = (DISPLAY_WIDTH / 2, DISPLAY_HEIGHT / 2)

text_area_middle_right = label.Label(terminalio.FONT, text=TEXT)
text_area_middle_right.anchor_point = (1.0, 0.5)
text_area_middle_right.anchored_position = (DISPLAY_WIDTH - 10, DISPLAY_HEIGHT / 2)

text_area_bottom_left = label.Label(terminalio.FONT, text=TEXT)
text_area_bottom_left.anchor_point = (0.0, 1.0)
text_area_bottom_left.anchored_position = (10, DISPLAY_HEIGHT)

text_area_bottom_middle = label.Label(terminalio.FONT, text=TEXT)
text_area_bottom_middle.anchor_point = (0.5, 1.0)
text_area_bottom_middle.anchored_position = (DISPLAY_WIDTH / 2, DISPLAY_HEIGHT)

text_area_bottom_right = label.Label(terminalio.FONT, text=TEXT)
text_area_bottom_right.anchor_point = (1.0, 1.0)
text_area_bottom_right.anchored_position = (DISPLAY_WIDTH - 10, DISPLAY_HEIGHT)

text_group = displayio.Group(max_size=9)
text_group.append(text_area_top_middle)
text_group.append(text_area_top_left)
text_group.append(text_area_top_right)
text_group.append(text_area_middle_middle)
text_group.append(text_area_middle_left)
text_group.append(text_area_middle_right)
text_group.append(text_area_bottom_middle)
text_group.append(text_area_bottom_left)
text_group.append(text_area_bottom_right)

board.DISPLAY.show(text_group)

while True:
    pass
