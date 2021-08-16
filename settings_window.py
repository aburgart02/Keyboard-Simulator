import settings
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
        self.volume_level_text = QLabel('Volume level: ' + str(settings.volume_level), self)
        self.increase_volume_button = QPushButton(self)
        self.increase_volume_button.clicked.connect(lambda x: self.change_volume(True))
        self.decrease_volume_button = QPushButton(self)
        self.decrease_volume_button.clicked.connect(lambda x: self.change_volume(False))
        self.next_button = QPushButton(self)
        self.next_button.clicked.connect(lambda x: self.set_background_file_name(True))
        self.previous_button = QPushButton(self)
        self.previous_button.clicked.connect(lambda x: self.set_background_file_name(False))
        self.configure_elements(1)

    def keyPressEvent(self, e):
        if e.key() == 16777216:
            self.previous_window = True
        if e.key() == 16777274:
            self.toggle_full_screen = True

    def configure_elements(self, ratio):
        self.volume_level_text.setFont(QtGui.QFont("Arial", 20, QtGui.QFont.Bold))
        self.volume_level_text.setStyleSheet('background-color: #570290; border-style: outset; border-width: 2px; '
                                             'border-radius: 4px; border-color: blue; min-width: 10em;'
                                             'padding: 6px; color: white;')
        self.volume_level_text.adjustSize()
        self.volume_level_text.move((self.width() - self.volume_level_text.width()) // 2, 200 * ratio)
        self.background_text.setFont(QtGui.QFont("Arial", 20, QtGui.QFont.Bold))
        self.background_text.setStyleSheet('background-color: #570290; border-style: outset; border-width: 2px; '
                                           'border-radius: 4px; border-color: blue; min-width: 10em;'
                                           'padding: 6px; color: white;')
        self.background_text.adjustSize()
        self.background_text.move((self.width() - self.background_text.width()) // 2, 400 * ratio)
        self.increase_volume_button.setIcon(QIcon(r"materials\right_arrow.png"))
        self.increase_volume_button.setStyleSheet('background-color: rgb(0, 0, 0, 0)')
        self.increase_volume_button.setIconSize(QSize(60, 60))
        self.increase_volume_button.move(self.volume_level_text.x() + self.volume_level_text.width() + 20, 200 * ratio - 6)
        self.decrease_volume_button.setIcon(QIcon(r"materials\left_arrow.png"))
        self.decrease_volume_button.setStyleSheet('background-color: rgb(0, 0, 0, 0)')
        self.decrease_volume_button.setIconSize(QSize(60, 60))
        self.decrease_volume_button.move(self.volume_level_text.x() - 90, 200 * ratio - 6)
        self.previous_button.setIcon(QIcon(r"materials\left_arrow.png"))
        self.previous_button.setStyleSheet('background-color: rgb(0, 0, 0, 0)')
        self.previous_button.setIconSize(QSize(60, 60))
        self.previous_button.move(self.background_text.x() - 90, 400 * ratio - 6)
        self.next_button.setIcon(QIcon(r"materials\right_arrow.png"))
        self.next_button.setStyleSheet('background-color: rgb(0, 0, 0, 0)')
        self.next_button.setIconSize(QSize(60, 60))
        self.next_button.move(self.background_text.x() + self.background_text.width() + 20, 400 * ratio - 6)

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

    def change_volume(self, mode):
        if mode and settings.volume_level < 100:
            settings.volume_level += 10
        elif mode is False and settings.volume_level > 0:
            settings.volume_level -= 10
        self.volume_level_text.setText('Volume level: ' + str(settings.volume_level))
        self.volume_level_text.adjustSize()
