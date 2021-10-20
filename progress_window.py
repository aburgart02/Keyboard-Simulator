import json
import os.path
import pyqtgraph
from PyQt5.QtWidgets import QWidget, QPushButton, QGridLayout
from settings import keys
import styles


class Progress(QWidget):
    def __init__(self, main):
        super().__init__(main)
        self.application = main
        self.previous_window = False
        self.graph = None
        self.layout = QGridLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 200)
        self.rus_progress_button = QPushButton('Русская раскладка', self)
        self.eng_progress_button = QPushButton('Английская раскладка', self)
        self.reset_progress_button = QPushButton('Сбросить прогресс', self)
        self.assign_buttons()

    def keyPressEvent(self, e):
        if e.key() == keys['ESC_KEY']:
            self.previous_window = True
            self.application.switch_windows()
        if e.key() == keys['F11_KEY']:
            self.change_resolution(1) if self.application.isFullScreen() \
                else self.change_resolution(self.application.resolution_ratio)
            e.ignore()

    def get_progress_data(self, language):
        self.layout.removeWidget(self.graph)
        self.graph = pyqtgraph.plot()
        with open(os.path.join('progress', 'progress.txt'), 'r') as f:
            statistics = json.load(f)
        progress = statistics[language]
        chart = pyqtgraph.BarGraphItem(x=[i for i in range(1, 11)], height=progress, width=1, brush='b')
        self.graph.addItem(chart)
        self.layout.addWidget(self.graph)

    def configure_elements(self, ratio):
        self.rus_progress_button.setStyleSheet(styles.lesson_button_style.format(str(int(20 * ratio))))
        self.rus_progress_button.adjustSize()
        self.rus_progress_button.move(500 * ratio, 600 * ratio)
        self.eng_progress_button.setStyleSheet(styles.lesson_button_style.format(str(int(20 * ratio))))
        self.eng_progress_button.adjustSize()
        self.eng_progress_button.move(900 * ratio, 600 * ratio)
        self.reset_progress_button.setStyleSheet(styles.lesson_button_style.format(str(int(20 * ratio))))
        self.reset_progress_button.adjustSize()
        self.reset_progress_button.move(100 * ratio, 600 * ratio)

    def assign_buttons(self):
        self.rus_progress_button.clicked.connect(lambda x: self.get_progress_data('rus_progress'))
        self.rus_progress_button.setAutoDefault(True)
        self.eng_progress_button.clicked.connect(lambda x: self.get_progress_data('eng_progress'))
        self.eng_progress_button.setAutoDefault(True)
        self.reset_progress_button.clicked.connect(self.reset_progress)
        self.reset_progress_button.setAutoDefault(True)

    def reset_progress(self):
        with open(os.path.join('progress', 'progress.txt'), 'w') as f:
            f.write(json.dumps({
                'rus_progress': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                'eng_progress': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]},
                indent=4))

    def change_resolution(self, ratio):
        self.setFixedSize(1280 * ratio, 720 * ratio)
        self.configure_elements(ratio)
