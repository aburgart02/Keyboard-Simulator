import os.path
import settings
import styles
from settings import keys
from PyQt5 import QtGui
from PyQt5.QtCore import QSize
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QWidget, QLabel, QPushButton


class PrintModeSelection(QWidget):
    def __init__(self, main):
        super().__init__(main)
        self.next_window = False
        self.previous_window = False
        self.toggle_full_screen = False
        self.keyboard_layout = ''
        self.text = QLabel("Select the mode", self)
        self.first_text_button = QPushButton(self)
        self.second_text_button = QPushButton(self)
        self.mode = QPushButton("   Ignore mistakes", self)
        self.mode.setIcon(QIcon(os.path.join('materials', 'cross.png')))
        self.mode.clicked.connect(self.change_mode)
        self.mode.setAutoDefault(True)
        self.configure_elements(1)

    def keyPressEvent(self, e):
        if e.key() == keys['ESC_KEY']:
            self.previous_window = True
        if e.key() == keys['F11_KEY']:
            self.toggle_full_screen = True

    def configure_elements(self, ratio):
        self.text.setFont(QtGui.QFont("Arial", 22 * ratio, QtGui.QFont.Bold))
        self.text.adjustSize()
        self.text.move((self.width() - self.text.width()) // 4, 45 * ratio)
        self.first_text_button.setFixedSize(1024, 268)
        self.first_text_button.setStyleSheet(styles.keyboard_layout_button_style)
        self.first_text_button.move((self.width() - self.first_text_button.width()) // 2, 120 * ratio)
        self.first_text_button.setIcon(QIcon(os.path.join("keyboards", "rus.png")))
        self.first_text_button.setIconSize(QSize(1024, 272))
        self.first_text_button.clicked.connect(lambda x: self.select_keyboard_layout('rus'))
        self.first_text_button.setAutoDefault(True)
        self.second_text_button.setFixedSize(1024, 268)
        self.second_text_button.setStyleSheet(styles.keyboard_layout_button_style)
        self.second_text_button.move((self.width() - self.second_text_button.width()) // 2, 420 * ratio)
        self.second_text_button.setIcon(QIcon(os.path.join("keyboards", "eng.png")))
        self.second_text_button.setIconSize(QSize(1024, 272))
        self.second_text_button.clicked.connect(lambda x: self.select_keyboard_layout('eng'))
        self.second_text_button.setAutoDefault(True)
        self.mode.move(int((self.width() - self.text.width()) // 1.5), 42 * ratio)
        self.mode.setStyleSheet(styles.printing_mode_button_style.format(str(int(28 * ratio))))
        self.mode.setIconSize(QSize(30 * ratio, 30 * ratio))
        self.mode.adjustSize()

    def change_resolution(self, ratio):
        self.setFixedSize(1280 * ratio, 720 * ratio)
        self.configure_elements(ratio)

    def select_keyboard_layout(self, language):
        self.next_window = True
        self.keyboard_layout = language

    def change_mode(self):
        if settings.print_mode:
            self.mode.setIcon(QIcon(os.path.join('materials', 'cross.png')))
            settings.print_mode = False
        else:
            self.mode.setIcon(QIcon(os.path.join('materials', 'mark.png')))
            settings.print_mode = True
