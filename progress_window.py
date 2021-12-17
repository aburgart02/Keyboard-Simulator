import json
import os.path
import pyqtgraph
from PyQt5.QtWidgets import QWidget, QPushButton, QGridLayout
from key_handler import key_processing
import styles


class Progress(QWidget):
    def __init__(self, main):
        super().__init__(main)
        self.application = main
        self.previous_window = False
        pyqtgraph.setConfigOption('background', '#ffffff')
        self.graph = None
        self.layout = QGridLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 200)
        self.styles = {'color': '#0000ff', 'font-size': '24px'}
        self.rus_progress_button = QPushButton('Русская раскладка', self)
        self.eng_progress_button = QPushButton('Английская раскладка', self)
        self.reset_progress_button = QPushButton('Сбросить прогресс', self)
        self.assign_buttons()

    def keyPressEvent(self, e):
        key_processing(self, e)

    def create_statistics_graph(self, language):
        self.layout.removeWidget(self.graph)
        self.graph = pyqtgraph.PlotWidget()
        self.configure_graph(language)
        with open(os.path.join('progress', 'progress.txt'), 'r') as f:
            statistics = json.load(f)
        chart = pyqtgraph.BarGraphItem(x=[i for i in range(1, 11)], height=statistics[language], width=1, brush='b')
        self.graph.addItem(chart)
        self.layout.addWidget(self.graph)

    def configure_graph(self, language):
        self.graph.setTitle("Русская раскладка", color="b", size="20pt") if language == 'rus_progress' \
            else self.graph.setTitle("Английская раскладка", color="b", size="20pt")
        self.graph.setLabel('left', 'Скорость печати', **self.styles)
        self.graph.setLabel('bottom', 'Номер урока', **self.styles)
        self.graph.setXRange(1, 10)

    def configure_elements(self, ratio):
        self.rus_progress_button.setStyleSheet(styles.lesson_button_style.format(str(int(20 * ratio))))
        self.rus_progress_button.adjustSize()
        self.rus_progress_button.move(100 * ratio, 600 * ratio)
        self.eng_progress_button.setStyleSheet(styles.lesson_button_style.format(str(int(20 * ratio))))
        self.eng_progress_button.adjustSize()
        self.eng_progress_button.move(500 * ratio, 600 * ratio)
        self.reset_progress_button.setStyleSheet(styles.lesson_button_style.format(str(int(20 * ratio))))
        self.reset_progress_button.adjustSize()
        self.reset_progress_button.move(900 * ratio, 600 * ratio)

    def assign_buttons(self):
        self.rus_progress_button.clicked.connect(lambda x: self.create_statistics_graph('rus_progress'))
        self.rus_progress_button.setAutoDefault(True)
        self.eng_progress_button.clicked.connect(lambda x: self.create_statistics_graph('eng_progress'))
        self.eng_progress_button.setAutoDefault(True)
        self.reset_progress_button.clicked.connect(self.reset_progress)
        self.reset_progress_button.setAutoDefault(True)

    @staticmethod
    def reset_progress():
        with open(os.path.join('progress', 'progress.txt'), 'w') as f:
            f.write(json.dumps({
                'rus_progress': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                'eng_progress': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]},
                indent=4))

    def change_resolution(self, ratio):
        self.setFixedSize(1280 * ratio, 720 * ratio)
        self.configure_elements(ratio)
