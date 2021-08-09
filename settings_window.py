from PyQt5 import QtGui
from PyQt5.QtCore import QSize
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QWidget, QLabel, QPushButton


class Settings(QWidget):
    def __init__(self, main):
        super().__init__(main)
        self.previous_window = False
        self.toggle_full_screen = False
        self.background_file_index = 0
        self.background_file = r"backgrounds\background_0.jpg"
        self.background_text = QLabel("Background", self)
        self.next_button = QPushButton(self)
        self.previous_button = QPushButton(self)
        self.configure_elements(1)

    def keyPressEvent(self, e):
        if e.key() == 16777216:
            self.previous_window = True
        if e.key() == 16777274:
            self.toggle_full_screen = True

    def configure_elements(self, ratio):
        self.background_text.setFont(QtGui.QFont("Arial", 18 * ratio, QtGui.QFont.Bold))
        self.background_text.setStyleSheet('background: #0073C0; border: 2px solid black')
        self.background_text.adjustSize()
        self.background_text.move((self.width() - self.background_text.width()) // 2, 500 * ratio)
        self.previous_button.setIcon(QIcon(r"materials\left_arrow.png"))
        self.previous_button.setStyleSheet('background-color: rgb(0, 0, 0, 0)')
        self.previous_button.setIconSize(QSize(60, 60))
        self.previous_button.move(500 * ratio, 500 * ratio)
        self.previous_button.clicked.connect(lambda y: self.set_background_file_name(False))
        self.next_button.setIcon(QIcon(r"materials\right_arrow.png"))
        self.next_button.setStyleSheet('background-color: rgb(0, 0, 0, 0)')
        self.next_button.setIconSize(QSize(60, 60))
        self.next_button.move(800 * ratio, 500 * ratio)
        self.next_button.clicked.connect(lambda y: self.set_background_file_name(True))

    def change_resolution(self, ratio):
        self.setFixedSize(1280 * ratio, 720 * ratio)
        self.configure_elements(ratio)

    def set_background_file_name(self, direction):
        if direction:
            self.background_file_index += 1
        else:
            self.background_file_index -= 1
        self.background_file_index = self.background_file_index % 4
        self.background_file = r"backgrounds\background_" + str(self.background_file_index) + ".jpg"
