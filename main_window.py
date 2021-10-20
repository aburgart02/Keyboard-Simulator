import os.path
from PyQt5.QtCore import QSize
from PyQt5.QtGui import QImage, QPalette, QBrush
from PyQt5.QtWidgets import QWidget, QPushButton, QDesktopWidget
from text_selection import TextSelection
from keyboard_simulator import KeyboardSimulator
from print_mode_selection import PrintModeSelection
from progress_window import Progress
from settings_window import Settings
from settings import keys
import styles


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
        self.start_button = QPushButton("Start", self)
        self.progress_button = QPushButton("Progress", self)
        self.settings_button = QPushButton("Settings", self)
        self.exit_button = QPushButton("Exit", self)
        self.print_mode_selection_widget = PrintModeSelection(self)
        self.text_selection_widget = TextSelection(self)
        self.keyboard_simulator_widget = KeyboardSimulator(self)
        self.settings_widget = Settings(self)
        self.progress_widget = Progress(self)
        self.widgets_list = [(self.print_mode_selection_widget, self.display_main_window,
                              self.display_text_selection_window),
                             (self.text_selection_widget, self.display_print_mode_selection_window,
                              self.display_keyboard_simulator_window),
                             (self.settings_widget, self.display_main_window),
                             (self.keyboard_simulator_widget, self.display_text_selection_window),
                             (self.progress_widget, self.display_main_window)]
        self.hide_windows()
        self.set_background(1)
        self.configure_elements(1)
        self.assign_buttons()
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

    def assign_buttons(self):
        self.start_button.clicked.connect(self.display_print_mode_selection_window)
        self.start_button.setAutoDefault(True)
        self.progress_button.clicked.connect(self.display_progress_window)
        self.progress_button.setAutoDefault(True)
        self.settings_button.clicked.connect(self.display_settings_window)
        self.settings_button.setAutoDefault(True)
        self.exit_button.clicked.connect(self.close_application)
        self.exit_button.setAutoDefault(True)

    def configure_elements(self, ratio):
        self.start_button.setStyleSheet(styles.main_menu_button_style.format(str(int(28 * ratio))))
        self.start_button.adjustSize()
        self.start_button.move((self.width() - self.start_button.width()) // 2, int(120 * ratio))
        self.progress_button.setStyleSheet(styles.main_menu_button_style.format(str(int(28 * ratio))))
        self.progress_button.adjustSize()
        self.progress_button.move((self.width() - self.progress_button.width()) // 2, int(220 * ratio))
        self.settings_button.setStyleSheet(styles.main_menu_button_style.format(str(int(28 * ratio))))
        self.settings_button.adjustSize()
        self.settings_button.move((self.width() - self.settings_button.width()) // 2, int(320 * ratio))
        self.exit_button.setStyleSheet(styles.main_menu_button_style.format(str(int(28 * ratio))))
        self.exit_button.adjustSize()
        self.exit_button.move((self.width() - self.exit_button.width()) // 2, int(420 * ratio))

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
            self.configure_elements(1)
        else:
            self.showFullScreen()
            self.set_background(self.resolution_ratio)
            self.configure_elements(self.resolution_ratio)

    def change_widget_resolution(self, widget):
        widget.change_resolution(self.resolution_ratio) if self.isFullScreen() else widget.change_resolution(1)

    def display_main_window(self):
        self.start_button.setFocus()
        self.start_button.show()
        self.progress_button.show()
        self.settings_button.show()
        self.exit_button.show()

    def hide_main_window(self):
        self.start_button.hide()
        self.progress_button.hide()
        self.settings_button.hide()
        self.exit_button.hide()

    def display_keyboard_simulator_window(self):
        self.keyboard_simulator_widget = KeyboardSimulator(self)
        self.widgets_list[3] = (self.keyboard_simulator_widget, self.display_text_selection_window)
        self.change_widget_resolution(self.keyboard_simulator_widget)
        self.keyboard_simulator_widget.show()
        self.keyboard_simulator_widget.right_field.setFocus()

    def display_print_mode_selection_window(self):
        self.change_widget_resolution(self.print_mode_selection_widget)
        self.hide_main_window()
        self.print_mode_selection_widget.show()
        self.print_mode_selection_widget.first_text_button.setFocus()

    def display_settings_window(self):
        self.change_widget_resolution(self.settings_widget)
        self.hide_main_window()
        self.settings_widget.show()
        self.settings_widget.decrease_volume_button.setFocus()

    def display_progress_window(self):
        self.progress_widget = Progress(self)
        self.widgets_list[4] = (self.progress_widget, self.display_main_window)
        self.change_widget_resolution(self.progress_widget)
        self.hide_main_window()
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
