# SPDX-License-Identifier: GPL-2.0-or-later

from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtWidgets import QTabWidget, QWidget, QScrollArea, QApplication
from PyQt5.QtGui import QPalette

from constants import KEYCODE_BTN_RATIO
from flowlayout import FlowLayout
from keycodes import KEYCODES_BASIC, KEYCODES_ISO, KEYCODES_MACRO, KEYCODES_LAYERS, KEYCODES_QUANTUM, KEYCODES_MAGIC, \
    KEYCODES_BACKLIGHT, KEYCODES_MEDIA, KEYCODES_SPECIAL, KEYCODES_SHIFTED, KEYCODES_USER, Keycode, KEYCODES_TAP_DANCE
from square_button import SquareButton
from util import tr, KeycodeDisplay


class TabbedKeycodes(QTabWidget):

    keycode_changed = pyqtSignal(int)
    anykey = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)

        self.target = None
        self.is_tray = False

        self.tab_basic = QScrollArea()
        self.tab_iso = QScrollArea()
        self.tab_layers = QScrollArea()
        self.tab_quantum = QScrollArea()
        self.tab_magic = QScrollArea()
        self.tab_backlight = QScrollArea()
        self.tab_media = QScrollArea()
        self.tab_tap_dance = QScrollArea()
        self.tab_user = QScrollArea()
        self.tab_macro = QScrollArea()

        self.widgets = []

        for (tab, label, keycodes) in [
            (self.tab_basic, "Basic", KEYCODES_SPECIAL + KEYCODES_BASIC + KEYCODES_SHIFTED),
            (self.tab_iso, "ISO/JIS", KEYCODES_ISO),
            (self.tab_layers, "Layers", KEYCODES_LAYERS),
            (self.tab_quantum, "Quantum", KEYCODES_QUANTUM),
            (self.tab_magic, "Magic", KEYCODES_MAGIC),
            (self.tab_backlight, "Backlight", KEYCODES_BACKLIGHT),
            (self.tab_media, "App, Media and Mouse", KEYCODES_MEDIA),
            (self.tab_tap_dance, "Tap Dance", KEYCODES_TAP_DANCE),
            (self.tab_user, "User", KEYCODES_USER),
            (self.tab_macro, "Macro", KEYCODES_MACRO),
        ]:
            layout = FlowLayout()
            if tab == self.tab_layers:
                self.layout_layers = layout
            elif tab == self.tab_tap_dance:
                self.layout_tap_dance = layout
            elif tab == self.tab_macro:
                self.layout_macro = layout
            elif tab == self.tab_user:
                self.layout_user = layout
            elif tab == self.tab_basic:
                # create the "Any" keycode button
                btn = SquareButton()
                btn.setText("Any")
                btn.setRelSize(KEYCODE_BTN_RATIO)
                btn.clicked.connect(lambda: self.anykey.emit())
                layout.addWidget(btn)

            self.widgets += self.create_buttons(layout, keycodes)

            tab.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
            tab.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
            tab.setWidgetResizable(True)

            w = QWidget()
            w.setLayout(layout)
            tab.setWidget(w)
            self.addTab(tab, tr("TabbedKeycodes", label))

        self.layer_keycode_buttons = []
        self.tap_dance_keycode_buttons = []
        self.macro_keycode_buttons = []
        self.user_keycode_buttons = []
        KeycodeDisplay.notify_keymap_override(self)

    def create_buttons(self, layout, keycodes, word_wrap=False):
        buttons = []

        for keycode in keycodes:
            btn = SquareButton()
            btn.setWordWrap(word_wrap)
            btn.setRelSize(KEYCODE_BTN_RATIO)
            btn.setToolTip(Keycode.tooltip(keycode.code))
            btn.clicked.connect(lambda st, k=keycode: self.keycode_changed.emit(k.code))
            btn.keycode = keycode
            layout.addWidget(btn)
            buttons.append(btn)

        return buttons

    def recreate_keycode_buttons(self):
        for btn in self.layer_keycode_buttons + self.tap_dance_keycode_buttons + self.macro_keycode_buttons \
                   + self.user_keycode_buttons:
            self.widgets.remove(btn)
            btn.hide()
            btn.deleteLater()
        self.layer_keycode_buttons = self.create_buttons(self.layout_layers, KEYCODES_LAYERS)
        self.tap_dance_keycode_buttons = self.create_buttons(self.layout_tap_dance, KEYCODES_TAP_DANCE)
        self.macro_keycode_buttons = self.create_buttons(self.layout_macro, KEYCODES_MACRO)
        self.user_keycode_buttons = self.create_buttons(self.layout_user, KEYCODES_USER, word_wrap=True)
        self.widgets += self.layer_keycode_buttons + self.tap_dance_keycode_buttons + \
            self.macro_keycode_buttons + self.user_keycode_buttons
        self.relabel_buttons()

    def on_keymap_override(self):
        self.relabel_buttons()

    def relabel_buttons(self):
        for widget in self.widgets:
            qmk_id = widget.keycode.qmk_id
            if qmk_id in KeycodeDisplay.keymap_override:
                label = KeycodeDisplay.keymap_override[qmk_id]
                highlight_color = QApplication.palette().color(QPalette.Link).getRgb()
                widget.setStyleSheet("QPushButton {color: rgb"+str(highlight_color)+";}")
            else:
                label = widget.keycode.label
                widget.setStyleSheet("QPushButton {}")
            widget.setText(label.replace("&", "&&"))

    @classmethod
    def set_tray(cls, tray):
        cls.tray = tray

    @classmethod
    def open_tray(cls, target):
        cls.tray.show()
        if cls.tray.target is not None and cls.tray.target != target:
            cls.tray.target.deselect()
        cls.tray.target = target

    @classmethod
    def close_tray(cls):
        if cls.tray.target is not None:
            cls.tray.target.deselect()
        cls.tray.target = None
        cls.tray.hide()

    def make_tray(self):
        self.is_tray = True
        TabbedKeycodes.set_tray(self)

        self.keycode_changed.connect(self.on_tray_keycode_changed)
        self.anykey.connect(self.on_tray_anykey)

    def on_tray_keycode_changed(self, kc):
        if self.target is not None:
            self.target.on_keycode_changed(kc)

    def on_tray_anykey(self):
        if self.target is not None:
            self.target.on_anykey()
