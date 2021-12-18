import json
import os.path
import pyqtgraph
from settings import graph_settings
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
        self.rus_detailed_progress_button = QPushButton('Подробный график', self)
        self.eng_progress_button = QPushButton('English layout', self)
        self.eng_detailed_progress_button = QPushButton('Detailed chart', self)
        self.reset_progress_button = QPushButton('Сбросить прогресс', self)
        self.assign_buttons()

    def keyPressEvent(self, e):
        key_processing(self, e)

    def create_statistics_graph(self, language):
        self.layout.removeWidget(self.graph)
        self.graph = pyqtgraph.PlotWidget()
        self.configure_graph(language, 'Скорость печати', 'Номер урока')
        self.graph.setXRange(1, 10)
        with open(os.path.join('progress', 'progress.txt'), 'r') as f:
            statistics = json.load(f)
        chart = pyqtgraph.BarGraphItem(x=[i for i in range(1, 11)], height=[item[0] for item in statistics[language]],
                                       width=1, brush='b')
        self.graph.addItem(chart)
        self.layout.addWidget(self.graph)

    def create_detailed_statistics_graph(self, language):
        self.layout.removeWidget(self.graph)
        self.graph = pyqtgraph.plot()
        self.configure_graph(language, 'Точность', 'Скорость печати')
        self.graph.addLegend()
        with open(os.path.join('progress', 'progress.txt'), 'r') as f:
            statistics = json.load(f)
        for i in range(0, len(statistics[language])):
            self.graph.plot([statistics[language][i][0]], [statistics[language][i][1]], name=graph_settings[i][0],
                            pen=graph_settings[i][1], symbolBrush=graph_settings[i][1], symbol='o',
                            symbolPen='w', symbolSize=14)
        self.layout.addWidget(self.graph)

    def configure_graph(self, language, left, bottom):
        self.graph.setTitle("Русская раскладка", color="b", size="20pt") if language == 'rus_progress' \
            else self.graph.setTitle("English layout", color="b", size="20pt")
        self.graph.setLabel('left', left, **self.styles)
        self.graph.setLabel('bottom', bottom, **self.styles)

    def configure_elements(self, ratio):
        self.rus_progress_button.setStyleSheet(styles.lesson_button_style.format(str(int(20 * ratio))))
        self.rus_progress_button.adjustSize()
        self.rus_progress_button.move(100 * ratio, 600 * ratio)
        self.rus_detailed_progress_button.setStyleSheet(styles.lesson_button_style.format(str(int(20 * ratio))))
        self.rus_detailed_progress_button.adjustSize()
        self.rus_detailed_progress_button.move(100 * ratio, 650 * ratio)
        self.eng_progress_button.setStyleSheet(styles.lesson_button_style.format(str(int(20 * ratio))))
        self.eng_progress_button.adjustSize()
        self.eng_progress_button.move(500 * ratio, 600 * ratio)
        self.eng_detailed_progress_button.setStyleSheet(styles.lesson_button_style.format(str(int(20 * ratio))))
        self.eng_detailed_progress_button.adjustSize()
        self.eng_detailed_progress_button.move(500 * ratio, 650 * ratio)
        self.reset_progress_button.setStyleSheet(styles.lesson_button_style.format(str(int(20 * ratio))))
        self.reset_progress_button.adjustSize()
        self.reset_progress_button.move(900 * ratio, 600 * ratio)

    def assign_buttons(self):
        self.rus_progress_button.clicked.connect(lambda x: self.create_statistics_graph('rus_progress'))
        self.rus_progress_button.setAutoDefault(True)
        self.rus_detailed_progress_button.clicked.connect(
            lambda x: self.create_detailed_statistics_graph('rus_progress'))
        self.rus_detailed_progress_button.setAutoDefault(True)
        self.eng_progress_button.clicked.connect(lambda x: self.create_statistics_graph('eng_progress'))
        self.eng_progress_button.setAutoDefault(True)
        self.eng_detailed_progress_button.clicked.connect(
            lambda x: self.create_detailed_statistics_graph('eng_progress'))
        self.eng_detailed_progress_button.setAutoDefault(True)
        self.reset_progress_button.clicked.connect(self.reset_progress)
        self.reset_progress_button.setAutoDefault(True)

    @staticmethod
    def reset_progress():
        with open(os.path.join('progress', 'progress.txt'), 'w') as f:
            f.write(json.dumps({
                'rus_progress': [[0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0],
                                 [0, 0], [0, 0], [0, 0]],
                'eng_progress': [[0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0],
                                 [0, 0], [0, 0], [0, 0]]}, indent=4))

    def change_resolution(self, ratio):
        self.setFixedSize(1280 * ratio, 720 * ratio)
        self.configure_elements(ratio)
