# SPDX-License-Identifier: GPL-2.0-or-later
from PyQt5.QtWidgets import QVBoxLayout, QPushButton, QWidget, QHBoxLayout, QLabel
from PyQt5.QtCore import Qt

import math

from basic_editor import BasicEditor
from util import tr, KeycodeDisplay
from vial_device import VialKeyboard
from keyboard_widget import KeyboardWidget
from kle_serial import Key
from keycodes import Keycode
import keyboard

ansi_layout = [
    [0,     0,     1,   1,   0x29,   "Esc"],
    [2,     0,     1,   1,   0x3A,   "F1"],
    [3,     0,     1,   1,   0x3B,   "F2"],
    [4,     0,     1,   1,   0x3C,   "F3"],
    [5,     0,     1,   1,   0x3D,   "F4"],
    [6.5,   0,     1,   1,   0x3E,   "F5"],
    [7.5,   0,     1,   1,   0x3F,   "F6"],
    [8.5,   0,     1,   1,   0x40,   "F7"],
    [9.5,   0,     1,   1,   0x41,   "F8"],
    [11,    0,     1,   1,   0x42,   "F9"],
    [12,    0,     1,   1,   0x43,   "F10"],
    [13,    0,     1,   1,   0x44,   "F11"],
    [14,    0,     1,   1,   0x45,   "F12"],
    [15.25, 0,     1,   1,   0x46,   "PrtSc"],
    [16.25, 0,     1,   1,   0x47,   "Scroll Lock"],
    [17.25, 0,     1,   1,   0x48,   "Pause\nBreak"],

    [0,     1.5,   1,   1,   0x35,   "~\n`"],
    [1,     1.5,   1,   1,   0x1E,   "!\n1"],
    [2,     1.5,   1,   1,   0x1F,   "@\n2"],
    [3,     1.5,   1,   1,   0x20,   "#\n3"],
    [4,     1.5,   1,   1,   0x21,   "$\n4"],
    [5,     1.5,   1,   1,   0x22,   "%\n5"],
    [6,     1.5,   1,   1,   0x23,   "^\n6"],
    [7,     1.5,   1,   1,   0x24,   "&\n7"],
    [8,     1.5,   1,   1,   0x25,   "*\n8"],
    [9,     1.5,   1,   1,   0x26,   "(\n9"],
    [10,    1.5,   1,   1,   0x27,   ")\n0"],
    [11,    1.5,   1,   1,   0x2D,   "_\n-"],
    [12,    1.5,   1,   1,   0x2E,   "+\n="],
    [13,    1.5,   2,   1,   0x2A,   "Backspace"],
    [15.25, 1.5,   1,   1,   0x49,   "Insert"],
    [16.25, 1.5,   1,   1,   0x4A,   "Home"],
    [17.25, 1.5,   1,   1,   0x4B,   "PgUp"],
    [18.5,  1.5,   1,   1,   0x53,   "Num Lock"],
    [19.5,  1.5,   1,   1,   0x54,   "/"],
    [20.5,  1.5,   1,   1,   0x55,   "*"],
    [21.5,  1.5,   1,   1,   0x56,   "-"],
    
    [0,     2.5,   1.5, 1,   0x2B,   "Tab"],
    [1.5,   2.5,   1,   1,   0x14,   "Q"],
    [2.5,   2.5,   1,   1,   0x1A,   "W"],
    [3.5,   2.5,   1,   1,   0x08,   "E"],
    [4.5,   2.5,   1,   1,   0x15,   "R"],
    [5.5,   2.5,   1,   1,   0x17,   "T"],
    [6.5,   2.5,   1,   1,   0x1C,   "Y"],
    [7.5,   2.5,   1,   1,   0x18,   "U"],
    [8.5,   2.5,   1,   1,   0x0C,   "I"],
    [9.5,   2.5,   1,   1,   0x12,   "O"],
    [10.5,  2.5,   1,   1,   0x13,   "P"],
    [11.5,  2.5,   1,   1,   0x2F,   "{\n["],
    [12.5,  2.5,   1,   1,   0x30,   "}\n]"],
    [13.5,  2.5,   1.5, 1,   0x31,   "|\n\\"],
    [15.25, 2.5,   1,   1,   0x4C,   "Delete"],
    [16.25, 2.5,   1,   1,   0x4D,   "End"],
    [17.25, 2.5,   1,   1,   0x4E,   "PgDn"],
    [18.5,  2.5,   1,   1,   0x5F,   "7\nHome"],
    [19.5,  2.5,   1,   1,   0x60,   "8\n↑"],
    [20.5,  2.5,   1,   1,   0x61,   "9\nPgUp"],
    [21.5,  2.5,   1,   2,   0x57,   "+"],

    [0,     3.5,   1.75,1,   0x39,   "Caps Lock"],
    [1.75,  3.5,   1,   1,   0x04,   "A"],
    [2.75,  3.5,   1,   1,   0x016,  "S"],
    [3.75,  3.5,   1,   1,   0x07,   "D"],
    [4.75,  3.5,   1,   1,   0x09,   "F"],
    [5.75,  3.5,   1,   1,   0x0A,   "G"],
    [6.75,  3.5,   1,   1,   0x0B,   "H"],
    [7.75,  3.5,   1,   1,   0x0D,   "J"],
    [8.75,  3.5,   1,   1,   0x0E,   "K"],
    [9.75,  3.5,   1,   1,   0x0F,   "L"],
    [10.75, 3.5,   1,   1,   0x33,   ":\n;"],
    [11.75, 3.5,   1,   1,   0x34,   "\"\n'"],
    [12.75, 3.5,   2.25,1,   0x28,   "Enter"],
    [18.5,  3.5,   1,   1,   0x5C,   "4\n←"],
    [19.5,  3.5,   1,   1,   0x5D,   "5"],
    [20.5,  3.5,   1,   1,   0x5E,   "6\n→"],
    
    [0,     4.5,   2.25,1,   0xE1,   "Shift"],
    [2.25,  4.5,   1,   1,   0x1D,   "Z"],
    [3.25,  4.5,   1,   1,   0x1B,   "X"],
    [4.25,  4.5,   1,   1,   0x06,   "C"],
    [5.25,  4.5,   1,   1,   0x19,   "V"],
    [6.25,  4.5,   1,   1,   0x05,   "B"],
    [7.25,  4.5,   1,   1,   0x11,   "N"],
    [8.25,  4.5,   1,   1,   0x10,   "M"],
    [9.25,  4.5,   1,   1,   0x36,   "<\n,"],
    [10.25, 4.5,   1,   1,   0x37,   ">\n."],
    [11.25, 4.5,   1,   1,   0x38,   "?\n/"],
    [12.25, 4.5,   2.75,1,   0xE5,   "Shift"],
    [16.25, 4.5,   1,   1,   0x52,   "↑"],
    [18.5,  4.5,   1,   1,   0x59,   "1\nEnd"],
    [19.5,  4.5,   1,   1,   0x5A,   "2\n↓"],
    [20.5,  4.5,   1,   1,   0x5B,   "3\nPgDn"],
    [21.5,  4.5,   1,   2,   0x58,   "Enter"],

    [0,     5.5,   1.25,1,   0xE0,   "Ctrl"],
    [1.25,  5.5,   1.25,1,   0xE3,   "Win"],
    [2.5,   5.5,   1.25,1,   0xE2,   "Alt"],
    [3.75,  5.5,   6.25,1,   0x2C,   " "],
    [10,    5.5,   1.25,1,   0xE6,   "Alt"],
    [11.25, 5.5,   1.25,1,   0xE7,   "Win"],
    [12.5,  5.5,   1.25,1,   0x65,   "Menu"],
    [13.75, 5.5,   1.25,1,   0xE4,   "Ctrl"],
    [15.25, 5.5,   1,   1,   0x50,   "←"],
    [16.25, 5.5,   1,   1,   0x51,   "↓"],
    [17.25, 5.5,   1,   1,   0x4F,   "→"],
    [18.5,  5.5,   2,   1,   0x62,   "0\nIns"],
    [20.5,  5.5,   1,   1,   0x63,   ".\nDel"]
]

class KeyboardTest(BasicEditor):

    def __init__(self, layout_editor):
        super().__init__()

        self.layout_editor = layout_editor

        self.keyboardWidget = KeyboardWidget(layout_editor)
        self.keyboardWidget.set_enabled(False)
        
        self.reset_btn = QPushButton("Reset")

        layout = QVBoxLayout()
        layout.addWidget(self.keyboardWidget)
        layout.setAlignment(self.keyboardWidget, Qt.AlignCenter)

        self.addLayout(layout)

        btn_layout = QHBoxLayout()
        btn_layout.addStretch()
        btn_layout.addWidget(self.reset_btn)
        self.addLayout(btn_layout)

        self.keyboard = None
        self.device = None
        self.keys = []

        self.keyboard_ui()

        self.reset_btn.clicked.connect(self.reset_keyboard_ui)

        self.grabber = QWidget()

    def rebuild(self, device):
        super().rebuild(device)
        if self.valid():
            self.keyboard = device.keyboard

    def valid(self):
        # Check if vial protocol is v3 or later
        return isinstance(self.device, VialKeyboard)

    def reset_keyboard_ui(self):
        # reset keyboard widget
        for w in self.keyboardWidget.widgets:
            w.setPressed(False)
            w.setActive(False)

        self.keyboardWidget.update_layout()
        self.keyboardWidget.update()
        self.keyboardWidget.updateGeometry()

    def keyboard_ui(self):
        for item in ansi_layout:
            key = Key()
            key.x = item[0]
            key.y = item[1]
            key.width = item[2]
            key.height = item[3]
            key.layout_index = key.layout_option = -1        
            self.keys.append(key)

        self.keyboardWidget.set_keys(self.keys, [])

        for i in range(len(ansi_layout)):
            KeycodeDisplay.display_keycode(self.keyboardWidget.widgets[i], ansi_layout[i][4])

    def activate(self):
        self.grabber.grabKeyboard()
        keyboard.hook(self.on_key)

    def deactivate(self):
        self.grabber.releaseKeyboard()
        keyboard.unhook_all()

    def on_key(self, ev):
        code = Keycode.find_by_recorder_alias(ev.name)
        if code is None:
            return
            
        for i in range(len(ansi_layout)):
            if ansi_layout[i][4] == code.code:
                break
        else:
            return
        
        if ev.event_type == 'down' and self.keyboardWidget.widgets[i].pressed == False:
            self.keyboardWidget.widgets[i].setPressed(True)
            self.keyboardWidget.widgets[i].setActive(True)
            self.keyboardWidget.update()
        elif ev.event_type == 'up' and self.keyboardWidget.widgets[i].pressed == True:
            self.keyboardWidget.widgets[i].setPressed(False)
            self.keyboardWidget.update()
