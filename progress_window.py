import json
import os.path
from PyQt5.QtWidgets import QWidget, QLabel, QPushButton
from settings import keys
import styles


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
        if e.key() == keys['ESC_KEY']:
            self.previous_window = True
        if e.key() == keys['F11_KEY']:
            self.toggle_full_screen = True

    def get_progress_data(self):
        with open(os.path.join('progress', 'progress.txt'), 'r') as f:
            statistics = json.load(f)
        self.rus_progress = sum(statistics['rus_progress'])
        self.eng_progress = sum(statistics['eng_progress'])
        self.rus_max_speed = statistics['rus_max_speed']
        self.eng_max_speed = statistics['eng_max_speed']

    def configure_elements(self, ratio):
        self.set_texts(1)
        self.rus_progress_text.setStyleSheet(styles.lesson_button_style.format(str(int(28 * ratio))))
        self.rus_progress_text.move(100 * ratio, 100 * ratio)
        self.rus_progress_text.adjustSize()
        self.eng_progress_text.setStyleSheet(styles.lesson_button_style.format(str(int(28 * ratio))))
        self.eng_progress_text.move(100 * ratio, 200 * ratio)
        self.eng_progress_text.adjustSize()
        self.rus_max_speed_text.setStyleSheet(styles.lesson_button_style.format(str(int(28 * ratio))))
        self.rus_max_speed_text.move(100 * ratio, 300 * ratio)
        self.rus_max_speed_text.adjustSize()
        self.eng_max_speed_text.setStyleSheet(styles.lesson_button_style.format(str(int(28 * ratio))))
        self.eng_max_speed_text.move(100 * ratio, 400 * ratio)
        self.eng_max_speed_text.adjustSize()
        self.reset_progress_button.setStyleSheet(styles.lesson_button_style.format(str(int(28 * ratio))))
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
            f.write(json.dumps({
                'rus_progress': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                'eng_progress': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                'rus_max_speed': 0,
                'eng_max_speed': 0}, indent=4))
        self.set_texts(0)

    def change_resolution(self, ratio):
        self.setFixedSize(1280 * ratio, 720 * ratio)
        self.configure_elements(ratio)
