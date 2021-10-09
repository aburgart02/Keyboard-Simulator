import json
import os.path
from PyQt5.QtWidgets import QWidget, QLabel, QPushButton


class Progress(QWidget):
    def __init__(self, main):
        super().__init__(main)
        self.toggle_full_screen = False
        self.previous_window = False
        self.rus_progress_text = QLabel('Прогресс обучения на русской раскладке: ', self)
        self.eng_progress_text = QLabel('Progress of learning in the english layout: ', self)
        self.rus_max_speed_text = QLabel('Наибольшая скорость печати на русской раскладке: ', self)
        self.eng_max_speed_text = QLabel('The highest printing speed on the english layout: ', self)
        self.reset_progress_button = QPushButton('Reset progress', self)
        self.rus_progress = 0
        self.eng_progress = 0
        self.rus_max_speed = 0
        self.eng_max_speed = 0
        self.get_progress_data()

    def keyPressEvent(self, e):
        if e.key() == 16777216:
            self.previous_window = True
        if e.key() == 16777274:
            self.toggle_full_screen = True

    def get_progress_data(self):
        with open(os.path.join('progress', 'progress.txt'), 'r') as f:
            data = f.readlines()
        rus_progress = json.loads(data[0])
        for x in rus_progress:
            self.rus_progress += x
        eng_progress = json.loads(data[1])
        for x in eng_progress:
            self.eng_progress += x
        self.rus_max_speed = json.loads(data[2])
        self.eng_max_speed = json.loads(data[3])

    def configure_elements(self, ratio):
        self.set_texts(1)
        self.rus_progress_text.setStyleSheet('background-color: #570290; border-style: outset; border-width: 2px; '
                                             'border-radius: 4px; border-color: blue; font: bold '
                                             + str(int(28 * ratio)) + 'px; min-width: 10em; '
                                             'padding: 6px; color: white;')
        self.rus_progress_text.move(100 * ratio, 100 * ratio)
        self.rus_progress_text.adjustSize()
        self.eng_progress_text.setStyleSheet('background-color: #570290; border-style: outset; border-width: 2px; '
                                             'border-radius: 4px; border-color: blue; font: bold '
                                             + str(int(28 * ratio)) + 'px; min-width: 10em; '
                                             'padding: 6px; color: white;')
        self.eng_progress_text.move(100 * ratio, 200 * ratio)
        self.eng_progress_text.adjustSize()
        self.rus_max_speed_text.setStyleSheet('background-color: #570290; border-style: outset; border-width: 2px; '
                                              'border-radius: 4px; border-color: blue; font: bold '
                                              + str(int(28 * ratio)) + 'px; min-width: 10em; '
                                              'padding: 6px; color: white;')
        self.rus_max_speed_text.move(100 * ratio, 300 * ratio)
        self.rus_max_speed_text.adjustSize()
        self.eng_max_speed_text.setStyleSheet('background-color: #570290; border-style: outset; border-width: 2px; '
                                              'border-radius: 4px; border-color: blue; font: bold '
                                              + str(int(28 * ratio)) + 'px; min-width: 10em; '
                                              'padding: 6px; color: white;')
        self.eng_max_speed_text.move(100 * ratio, 400 * ratio)
        self.eng_max_speed_text.adjustSize()
        self.reset_progress_button.setStyleSheet('background-color: #570290; border-style: outset; border-width: 2px; '
                                                 'border-radius: 4px; border-color: blue; font: bold '
                                                 + str(int(28 * ratio)) + 'px; min-width: 10em; '
                                                 'padding: 6px; color: white;')
        self.reset_progress_button.move(100 * ratio, 500 * ratio)
        self.reset_progress_button.clicked.connect(self.reset_progress)
        self.reset_progress_button.setAutoDefault(True)
        self.reset_progress_button.adjustSize()

    def set_texts(self, reset_flag):
        self.rus_progress_text.setText('Прогресс обучения на русской раскладке: '
                                       + str(self.rus_progress * 10 * reset_flag) + '%')
        self.eng_progress_text.setText('Progress of learning in the english layout: '
                                       + str(self.eng_progress * 10 * reset_flag) + '%')
        self.rus_max_speed_text.setText('Наибольшая скорость печати на русской раскладке: '
                                        + str(self.rus_max_speed * reset_flag) + ' знаков в минуту')
        self.eng_max_speed_text.setText('The highest printing speed on the english layout: '
                                        + str(self.eng_max_speed * reset_flag) + ' characters per minute')

    def reset_progress(self):
        with open(os.path.join('progress', 'progress.txt'), 'w') as f:
            f.write(json.dumps([0, 0, 0, 0, 0, 0, 0, 0, 0, 0]))
            f.write('\n')
            f.write(json.dumps([0, 0, 0, 0, 0, 0, 0, 0, 0, 0]))
            f.write('\n')
            f.write(json.dumps(0))
            f.write('\n')
            f.write(json.dumps(0))
        self.set_texts(0)

    def change_resolution(self, ratio):
        self.setFixedSize(1280 * ratio, 720 * ratio)
        self.configure_elements(ratio)
