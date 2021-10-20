import os.path
from PyQt5.QtCore import QSize
from PyQt5.QtGui import QImage, QPalette, QBrush
from PyQt5.QtWidgets import QWidget, QDesktopWidget
from text_selection import TextSelection
from keyboard_simulator import KeyboardSimulator
from print_mode_selection import PrintModeSelection
from progress_window import Progress
from settings_window import Settings
from main_menu import MainMenu
from settings import keys


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setFixedSize(1280, 720)
        self.resolution = QDesktopWidget().availableGeometry()
        self.resolution_ratio = self.resolution.width() / 1280
        self.background_file = os.path.join("backgrounds", "background_0.jpg")
        self.image = QImage(self.background_file)
        self.background = self.image.scaled(QSize(1280, 720))
        self.palette = QPalette()
        self.main_menu_widget = MainMenu(self)
        self.print_mode_selection_widget = PrintModeSelection(self)
        self.text_selection_widget = TextSelection(self)
        self.keyboard_simulator_widget = KeyboardSimulator(self)
        self.settings_widget = Settings(self)
        self.progress_widget = Progress(self)
        self.widgets_list = [(self.print_mode_selection_widget, self.main_menu_widget.show,
                              self.display_text_selection_window),
                             (self.text_selection_widget, self.display_print_mode_selection_window,
                              self.display_keyboard_simulator_window),
                             (self.settings_widget, self.main_menu_widget.show),
                             (self.keyboard_simulator_widget, self.display_text_selection_window),
                             (self.progress_widget, self.main_menu_widget.show)]
        self.hide_windows()
        self.set_background(1)
        self.show()

    def keyPressEvent(self, e):
        if e.key() == keys['F11_KEY']:
            self.change_main_window_resolution()

    def hide_windows(self):
        self.print_mode_selection_widget.hide()
        self.keyboard_simulator_widget.hide()
        self.text_selection_widget.hide()
        self.progress_widget.hide()
        self.settings_widget.hide()

    def set_background(self, ratio):
        self.background = self.image.scaled(QSize(int(1280 * ratio), int(720 * ratio)))
        self.palette.setBrush(QPalette.Window, QBrush(self.background))
        self.setPalette(self.palette)

    def change_background(self):
        if self.settings_widget.background_file != self.background_file:
            self.background_file = self.settings_widget.background_file
            self.image = QImage(self.background_file)
            self.set_background(self.resolution_ratio) if self.isFullScreen() else self.set_background(1)

    def switch_windows(self):
        for widget in self.widgets_list:
            if widget[0].previous_window:
                widget[0].close()
                widget[0].previous_window = False
                widget[1]()
        for widget in self.widgets_list[:2]:
            if widget[0].next_window:
                widget[0].hide()
                widget[0].next_window = False
                widget[2]()

    def change_main_window_resolution(self):
        if self.isFullScreen():
            self.showNormal()
            self.set_background(1)
            self.main_menu_widget.configure_elements(1)
        else:
            self.showFullScreen()
            self.set_background(self.resolution_ratio)
            self.main_menu_widget.configure_elements(self.resolution_ratio)

    def change_widget_resolution(self, widget):
        widget.change_resolution(self.resolution_ratio) if self.isFullScreen() else widget.change_resolution(1)

    def display_keyboard_simulator_window(self):
        self.keyboard_simulator_widget = KeyboardSimulator(self)
        self.widgets_list[3] = (self.keyboard_simulator_widget, self.display_text_selection_window)
        self.change_widget_resolution(self.keyboard_simulator_widget)
        self.keyboard_simulator_widget.show()
        self.keyboard_simulator_widget.right_field.setFocus()

    def display_print_mode_selection_window(self):
        self.change_widget_resolution(self.print_mode_selection_widget)
        self.main_menu_widget.hide()
        self.print_mode_selection_widget.show()
        self.print_mode_selection_widget.first_text_button.setFocus()

    def display_settings_window(self):
        self.change_widget_resolution(self.settings_widget)
        self.main_menu_widget.hide()
        self.settings_widget.show()
        self.settings_widget.decrease_volume_button.setFocus()

    def display_progress_window(self):
        self.progress_widget = Progress(self)
        self.widgets_list[4] = (self.progress_widget, self.main_menu_widget.show)
        self.change_widget_resolution(self.progress_widget)
        self.main_menu_widget.hide()
        self.progress_widget.show()
        self.progress_widget.reset_progress_button.setFocus()

    def display_text_selection_window(self):
        self.change_widget_resolution(self.text_selection_widget)
        self.text_selection_widget.show()
        if self.print_mode_selection_widget.keyboard_layout == 'rus':
            self.text_selection_widget.set_rus_texts()
            self.text_selection_widget.rus_lesson_1.setFocus()
        else:
            self.text_selection_widget.set_eng_texts()
            self.text_selection_widget.eng_lesson_1.setFocus()

    def close_application(self):
        self.close()
