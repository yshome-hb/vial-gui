# SPDX-License-Identifier: GPL-2.0-or-later
from PyQt5.QtWidgets import QVBoxLayout, QPushButton, QWidget, QHBoxLayout, QLabel
from PyQt5.QtCore import Qt, QTimer

import math

from basic_editor import BasicEditor
from util import tr
from vial_device import VialKeyboard
from key_widget import KeyWidget


class KeyboardTest(BasicEditor):

    def __init__(self, layout_editor):
        super().__init__()

        self.layout_editor = layout_editor

        self.reset_btn = QPushButton("Reset")

        btn_layout = QHBoxLayout()
        btn_layout.addStretch()
        btn_layout.addWidget(self.reset_btn)
        self.addLayout(btn_layout)

        self.keyboard = None
        self.device = None

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
        layout = QVBoxLayout()
        layout.addWidget(KeyWidget())
        # layout.setAlignment(self.keyboardWidget, Qt.AlignCenter)
        self.addLayout(layout)

    def activate(self):
        self.grabber.grabKeyboard()

    def deactivate(self):
        self.grabber.releaseKeyboard()
