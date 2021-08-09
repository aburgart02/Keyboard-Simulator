from PyQt5 import QtGui
from PyQt5.QtCore import QSize
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QWidget, QLabel, QPushButton


class KeyboardLayoutSelection(QWidget):
    def __init__(self, main):
        super().__init__(main)
        self.next_window = False
        self.previous_window = False
        self.toggle_full_screen = False
        self.keyboard_layout = ''
        self.text = QLabel("Выберите раскладку клавиатуры", self)
        self.first_text_button = QPushButton(self)
        self.second_text_button = QPushButton(self)
        self.configure_elements(1)

    def keyPressEvent(self, e):
        if e.key() == 16777216:
            self.previous_window = True
        if e.key() == 16777274:
            self.toggle_full_screen = True

    def configure_elements(self, ratio):
        self.text.move(420 * ratio, 45 * ratio)
        self.text.setFont(QtGui.QFont("Arial", 16 * ratio, QtGui.QFont.Bold))
        self.text.adjustSize()
        self.first_text_button.move(130 * ratio ** 3, 120 * ratio)
        self.first_text_button.setFixedSize(1024, 268)
        self.first_text_button.setIcon(QIcon(r"keyboards\rus.png"))
        self.first_text_button.setIconSize(QSize(1024, 272))
        self.first_text_button.clicked.connect(lambda x: self.select_keyboard_layout('rus'))
        self.second_text_button.move(130 * ratio ** 3, 420 * ratio)
        self.second_text_button.setFixedSize(1024, 268)
        self.second_text_button.setIcon(QIcon(r"keyboards\eng.png"))
        self.second_text_button.setIconSize(QSize(1024, 272))
        self.second_text_button.clicked.connect(lambda x: self.select_keyboard_layout('eng'))

    def change_resolution(self, ratio):
        self.setFixedSize(1280 * ratio, 720 * ratio)
        self.configure_elements(ratio)

    def select_keyboard_layout(self, language):
        self.next_window = True
        self.keyboard_layout = language
