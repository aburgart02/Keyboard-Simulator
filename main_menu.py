import styles
from PyQt5.QtWidgets import QWidget, QPushButton


class MainMenu(QWidget):
    def __init__(self, main):
        super().__init__(main)
        self.setFixedSize(1280, 720)
        self.start_button = QPushButton("Start", self)
        self.progress_button = QPushButton("Progress", self)
        self.settings_button = QPushButton("Settings", self)
        self.exit_button = QPushButton("Exit", self)
        self.configure_elements(1)

    def assign_buttons(self, main):
        self.start_button.clicked.connect(main.display_print_mode_selection_window)
        self.start_button.setAutoDefault(True)
        self.progress_button.clicked.connect(main.display_progress_window)
        self.progress_button.setAutoDefault(True)
        self.settings_button.clicked.connect(main.display_settings_window)
        self.settings_button.setAutoDefault(True)
        self.exit_button.clicked.connect(main.close_application)
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

    def change_resolution(self, ratio):
        self.setFixedSize(1280 * ratio, 720 * ratio)
        self.configure_elements(ratio)
