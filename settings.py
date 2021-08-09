from PyQt5.QtWidgets import QWidget, QLabel, QPushButton


class Settings(QWidget):
    def __init__(self, main):
        super().__init__(main)
        self.previous_window = False
        self.toggle_full_screen = False
        self.background_file_index = 0
        self.background_file = r"backgrounds\background_0.jpg"
        self.background_text = QLabel("Background Picture", self)
        self.next_button = QPushButton("Next", self)
        self.previous_button = QPushButton("Previous", self)
        self.configure_elements(1)

    def keyPressEvent(self, e):
        if e.key() == 16777216:
            self.previous_window = True
        if e.key() == 16777274:
            self.toggle_full_screen = True

    def configure_elements(self, x):
        self.background_text.move(100 * x, 100 * x)
        self.previous_button.move(0 * x, 100 * x)
        self.previous_button.clicked.connect(lambda y: self.set_background_file_name(False))
        self.next_button.move(200 * x, 100 * x)
        self.next_button.clicked.connect(lambda y: self.set_background_file_name(True))

    def change_resolution(self, x):
        self.setFixedSize(1280 * x, 720 * x)
        self.configure_elements(x)

    def set_background_file_name(self, direction):
        if direction:
            self.background_file_index += 1
        else:
            self.background_file_index -= 1
        self.background_file_index = self.background_file_index % 4
        self.background_file = r"backgrounds\background_" + str(self.background_file_index) + ".jpg"