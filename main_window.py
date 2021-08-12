from PyQt5 import QtCore
from PyQt5.QtCore import QSize
from PyQt5.QtGui import QImage, QPalette, QBrush
from PyQt5.QtWidgets import QWidget, QPushButton
from text_selection import TextSelection
from keyboard_simulator import KeyboardSimulator
from keyboard_layout_selection import KeyboardLayoutSelection
from settings_window import Settings
from settings import resolution_ratio


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
        self.configure_elements(1)
        self.global_timer = QtCore.QTimer()
        self.global_timer.timeout.connect(self.switch_windows)
        self.global_timer.timeout.connect(self.check_windows_resolution)
        self.global_timer.timeout.connect(self.change_background)
        self.global_timer.start(100)
        self.show()

    def keyPressEvent(self, e):
        if e.key() == 16777274:
            self.change_main_window_resolution()

    def hide_windows(self):
        self.keyboard_layout_selection_widget.hide()
        self.keyboard_simulator_widget.hide()
        self.text_selection_widget.hide()
        self.settings_widget.hide()

    def set_background(self, ratio):
        self.background = self.image.scaled(QSize(1280 * ratio, 720 * ratio))
        self.palette.setBrush(QPalette.Window, QBrush(self.background))
        self.setPalette(self.palette)

    def change_background(self):
        if self.settings_widget.background_file != self.background_file:
            self.background_file = self.settings_widget.background_file
            self.image = QImage(self.background_file)
            if self.isFullScreen():
                self.set_background(resolution_ratio)
            else:
                self.set_background(1)

    def configure_elements(self, ratio):
        self.start_button.clicked.connect(self.display_keyboard_layout_selection_window)
        self.start_button.setStyleSheet('background-color: blue; border-style: outset; border-width: 2px; '
                                        'border-radius: 10px; border-color: yellow; font: bold ' +
                                        str(int(28 * ratio)) + 'px; min-width: 10em; padding: 6px; color: red;')
        self.start_button.adjustSize()
        self.start_button.move((self.width() - self.start_button.width()) // 2, 100 * ratio)
        self.progress_button.setStyleSheet('background-color: blue; border-style: outset; border-width: 2px; '
                                           'border-radius: 10px; border-color: yellow; font: bold '
                                           + str(int(28 * ratio)) + 'px; min-width: 10em; padding: 6px; color: red;')
        self.progress_button.clicked.connect(self.close_application)
        self.progress_button.adjustSize()
        self.progress_button.move((self.width() - self.progress_button.width()) // 2, 200 * ratio)
        self.settings_button.setStyleSheet('background-color: blue; border-style: outset; border-width: 2px; '
                                           'border-radius: 10px; border-color: yellow; font: bold '
                                           + str(int(28 * ratio)) + 'px; min-width: 10em; padding: 6px; color: red;')
        self.settings_button.clicked.connect(self.display_settings_window)
        self.settings_button.adjustSize()
        self.settings_button.move((self.width() - self.settings_button.width()) // 2, 300 * ratio)
        self.exit_button.clicked.connect(self.close_application)
        self.exit_button.setStyleSheet('background-color: #6600ff; border-style: outset; border-width: 2px; '
                                       'border-radius: 10px; border-color: yellow; font: '
                                       + str(int(28 * ratio)) + 'px; min-width: 10em; padding: 6px; color: red;')
        self.exit_button.adjustSize()
        self.exit_button.move((self.width() - self.exit_button.width()) // 2, 400 * ratio)

    def switch_windows(self):
        if self.keyboard_simulator_widget.right_field.previous_window:
            self.keyboard_simulator_widget.close()
            self.keyboard_simulator_widget.right_field.previous_window = False
            self.display_text_selection_window()
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
            self.change_widget_resolution(self.keyboard_simulator_widget, True)
            self.change_main_window_resolution()
            self.keyboard_simulator_widget.right_field.toggle_full_screen = False
        if self.keyboard_layout_selection_widget.toggle_full_screen:
            self.change_widget_resolution(self.keyboard_layout_selection_widget, True)
            self.change_main_window_resolution()
            self.keyboard_layout_selection_widget.toggle_full_screen = False
        if self.settings_widget.toggle_full_screen:
            self.change_widget_resolution(self.settings_widget, True)
            self.change_main_window_resolution()
            self.settings_widget.toggle_full_screen = False
        if self.text_selection_widget.toggle_full_screen:
            self.change_widget_resolution(self.text_selection_widget, True)
            self.change_main_window_resolution()
            self.text_selection_widget.toggle_full_screen = False

    def change_main_window_resolution(self):
        if self.isFullScreen():
            self.showNormal()
            self.set_background(1)
            self.configure_elements(1)
        else:
            self.showFullScreen()
            self.set_background(resolution_ratio)
            self.configure_elements(resolution_ratio)

    def change_widget_resolution(self, widget, mode):
        if mode:
            if self.isFullScreen():
                widget.change_resolution(1)
            else:
                widget.change_resolution(resolution_ratio)
        else:
            if self.isFullScreen():
                widget.change_resolution(resolution_ratio)
            else:
                widget.change_resolution(1)

    def display_main_window(self, mode):
        if mode:
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
        self.change_widget_resolution(self.keyboard_simulator_widget, False)
        self.keyboard_simulator_widget.show()
        self.keyboard_simulator_widget.right_field.setFocus()

    def display_keyboard_layout_selection_window(self):
        self.change_widget_resolution(self.keyboard_layout_selection_widget, False)
        self.display_main_window(False)
        self.keyboard_layout_selection_widget.show()
        self.keyboard_layout_selection_widget.setFocus()

    def display_settings_window(self):
        self.change_widget_resolution(self.settings_widget, False)
        self.display_main_window(False)
        self.settings_widget.show()
        self.settings_widget.setFocus()

    def display_text_selection_window(self):
        self.change_widget_resolution(self.text_selection_widget, False)
        self.text_selection_widget.show()
        if self.keyboard_layout_selection_widget.keyboard_layout == 'rus':
            self.text_selection_widget.set_rus_texts()
        else:
            self.text_selection_widget.set_eng_texts()
        self.text_selection_widget.setFocus()

    def close_application(self):
        self.close()
