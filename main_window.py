from PyQt5 import QtCore
from PyQt5.QtCore import QSize
from PyQt5.QtGui import QImage, QPalette, QBrush
from PyQt5.QtWidgets import QWidget, QPushButton
from text_selection import TextSelection
from keyboard_simulator import KeyboardSimulator
from keyboard_layout_selection import KeyboardLayoutSelection
from settings import Settings


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setFixedSize(1280, 720)
        self.background_file = r"backgrounds\background_0.jpg"
        self.image = QImage(self.background_file)
        self.background = self.image.scaled(QSize(1280, 720))
        self.palette = QPalette()
        self.start_button = QPushButton("Start", self)
        self.progress_button = QPushButton("Progress", self)
        self.settings_button = QPushButton("Settings", self)
        self.exit_button = QPushButton("Exit", self)
        self.keyboard_layout_selection_widget = KeyboardLayoutSelection(self)
        self.text_selection_widget = TextSelection(self)
        self.keyboard_simulator_widget = KeyboardSimulator(self)
        self.settings_widget = Settings(self)
        self.hide_windows()
        self.set_background(1)
        self.configure_elements()
        self.global_timer = QtCore.QTimer()
        self.global_timer.timeout.connect(self.switch_windows)
        self.global_timer.timeout.connect(self.check_windows_resolution)
        self.global_timer.timeout.connect(self.change_background)
        self.global_timer.start(100)
        self.show()

    def keyPressEvent(self, e):
        if e.key() == 16777274:
            self.change_resolution()

    def hide_windows(self):
        self.keyboard_layout_selection_widget.hide()
        self.keyboard_simulator_widget.hide()
        self.text_selection_widget.hide()
        self.settings_widget.hide()

    def set_background(self, x):
        self.background = self.image.scaled(QSize(1280 * x, 720 * x))
        self.palette.setBrush(QPalette.Window, QBrush(self.background))
        self.setPalette(self.palette)

    def configure_elements(self):
        self.start_button.move(440, 100)
        self.start_button.clicked.connect(self.display_keyboard_layout_selection_window)
        self.start_button.setStyleSheet('''background-color: blue; border-style: outset; border-width: 2px; 
        border-radius: 10px; border-color: yellow; font: bold 28px; min-width: 10em; padding: 6px; color: red;''')
        self.progress_button.move(440, 200)
        self.progress_button.setStyleSheet('''background-color: blue; border-style: outset; border-width: 2px; 
        border-radius: 10px; border-color: yellow; font: bold 28px; min-width: 10em; padding: 6px; color: red;''')
        self.progress_button.clicked.connect(self.close_application)
        self.settings_button.move(440, 300)
        self.settings_button.setStyleSheet('''background-color: blue; border-style: outset; border-width: 2px; 
        border-radius: 10px; border-color: yellow; font: bold 28px; min-width: 10em; padding: 6px; color: red;''')
        self.settings_button.clicked.connect(self.display_settings_window)
        self.exit_button.move(440, 400)
        self.exit_button.clicked.connect(self.close_application)
        self.exit_button.setStyleSheet('''background-color: #6600ff; border-style: outset; border-width: 2px; 
        border-radius: 10px; border-color: yellow; font: 28px; min-width: 10em; padding: 6px; color: red;''')

    def switch_windows(self):
        if self.keyboard_simulator_widget.right_field.previous_window:
            self.keyboard_simulator_widget.close()
            self.keyboard_simulator_widget.right_field.previous_window = False
            self.text_selection_widget.show()
            self.text_selection_widget.setFocus()
        if self.text_selection_widget.next_window:
            self.text_selection_widget.hide()
            self.text_selection_widget.next_window = False
            self.display_keyboard_simulator_window()
        if self.text_selection_widget.previous_window:
            self.text_selection_widget.hide()
            self.text_selection_widget.previous_window = False
            self.display_keyboard_layout_selection_window()
        if self.keyboard_layout_selection_widget.next_window:
            self.keyboard_layout_selection_widget.hide()
            self.keyboard_layout_selection_widget.next_window = False
            self.display_text_selection_window()
        if self.keyboard_layout_selection_widget.previous_window:
            self.keyboard_layout_selection_widget.hide()
            self.keyboard_layout_selection_widget.previous_window = False
            self.display_main_window(True)
        if self.settings_widget.previous_window:
            self.settings_widget.hide()
            self.settings_widget.previous_window = False
            self.display_main_window(True)

    def check_windows_resolution(self):
        if self.keyboard_simulator_widget.right_field.toggle_full_screen:
            if self.isFullScreen():
                self.keyboard_simulator_widget.change_resolution(1)
            else:
                self.keyboard_simulator_widget.change_resolution(1.5)
            self.change_resolution()
            self.keyboard_simulator_widget.right_field.toggle_full_screen = False
        if self.keyboard_layout_selection_widget.toggle_full_screen:
            if self.isFullScreen():
                self.keyboard_layout_selection_widget.change_resolution(1)
            else:
                self.keyboard_layout_selection_widget.change_resolution(1.5)
            self.change_resolution()
            self.keyboard_layout_selection_widget.toggle_full_screen = False

    def change_resolution(self):
        if self.isFullScreen():
            self.showNormal()
            self.set_background(1)
        else:
            self.showFullScreen()
            self.set_background(1.5)

    def change_background(self):
        if self.settings_widget.background_file != self.background_file:
            self.background_file = self.settings_widget.background_file
            self.image = QImage(self.background_file)
            if self.isFullScreen():
                self.set_background(1.5)
            else:
                self.set_background(1)

    def display_main_window(self, status):
        if status:
            self.start_button.show()
            self.progress_button.show()
            self.settings_button.show()
            self.exit_button.show()
        else:
            self.start_button.hide()
            self.progress_button.hide()
            self.settings_button.hide()
            self.exit_button.hide()

    def display_keyboard_simulator_window(self):
        self.keyboard_simulator_widget = KeyboardSimulator(self)
        if self.isFullScreen():
            self.keyboard_simulator_widget.change_resolution(1.5)
        self.keyboard_simulator_widget.show()
        self.keyboard_simulator_widget.right_field.setFocus()

    def display_keyboard_layout_selection_window(self):
        self.display_main_window(False)
        self.keyboard_layout_selection_widget.show()
        self.keyboard_layout_selection_widget.setFocus()

    def display_settings_window(self):
        self.display_main_window(False)
        self.settings_widget.show()
        self.settings_widget.setFocus()

    def display_text_selection_window(self):
        self.text_selection_widget.show()
        if self.keyboard_layout_selection_widget.keyboard_layout == 'rus':
            self.text_selection_widget.set_rus_texts()
        else:
            self.text_selection_widget.set_eng_texts()
        self.text_selection_widget.setFocus()

    def close_application(self):
        self.close()
