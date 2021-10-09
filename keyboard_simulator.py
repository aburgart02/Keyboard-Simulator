import json
import settings
import os.path
from PyQt5 import QtGui, QtCore
from PyQt5.QtGui import QPixmap, QFont
from PyQt5.QtWidgets import QWidget, QLabel
from input_field import RightField, LeftField
from settings import resolution, codes


class KeyboardSimulator(QWidget):
    def __init__(self, main):
        super().__init__(main)
        self.text = settings.text
        self.text_id = settings.text_id
        self.text_language = settings.text_language
        self.right_field = RightField(self, self.text)
        self.left_field = LeftField(self, self.text)
        self.errors_counter = QLabel(self)
        self.timer = QLabel(self)
        self.progress_counter = QLabel(self)
        self.speed_counter = QLabel(self)
        self.text_size = QLabel(self)
        self.accuracy_counter = QLabel(self)
        self.picture_slot = QLabel(self)
        self.pixmap = None
        self.configure_elements(1)
        self.update_data()
        self.global_timer = QtCore.QTimer()
        self.global_timer.timeout.connect(self.update_data)
        self.global_timer.start(10)

    def update_data(self):
        self.errors_counter.setText("Число ошибок: " + str(self.right_field.errors))
        self.errors_counter.adjustSize()
        self.timer.setText("Время: " + self.right_field.time.toString())
        self.timer.adjustSize()
        self.progress_counter.setText("Прогресс: " + str(round(100 * self.right_field.index / len(self.text), 1)) + "%")
        self.progress_counter.adjustSize()
        self.speed_counter.setText("Знаков в минуту: " + str(round(60 * self.right_field.right_letters_count
                                                                   / (self.right_field.time.second()
                                                                      + self.right_field.time.minute() * 60 + 0.1))))
        self.speed_counter.adjustSize()
        self.text_size.setText("Длина текста: " + str(len(self.text)))
        self.text_size.adjustSize()
        self.accuracy_counter.setText("Точность: "
                                      + str(round(100 * self.right_field.right_letters_count
                                                  / (self.right_field.right_letters_count
                                                     + self.right_field.errors + 0.001))) + "%")
        self.accuracy_counter.adjustSize()
        self.left_field.update(self.right_field.word, self.right_field.words_in_text, self.right_field.letter_number,
                               self.right_field.word_number)
        if len(self.right_field.type_text) == 0:
            self.finish_printing()
        if len(self.right_field.type_text) != 0 and self.right_field.next_symbol:
            self.set_keyboard_picture()
            self.right_field.next_symbol = False
        self.picture_slot.adjustSize()

    def finish_printing(self):
        self.global_timer.stop()
        with open(os.path.join('progress', 'progress.txt'), 'r') as f:
            data = f.readlines()
        progress_rus = json.loads(data[0])
        progress_eng = json.loads(data[1])
        rus_max_speed = json.loads(data[2])
        eng_max_speed = json.loads(data[3])
        if self.text_id is not None and self.text_id < 10:
            if self.text_language == 0:
                progress_rus[self.text_id] = 1
            else:
                progress_eng[self.text_id] = 1
        if int(self.speed_counter.text().split()[3]) > rus_max_speed and self.text_language == 0:
            rus_max_speed = int(self.speed_counter.text().split()[3])
        if int(self.speed_counter.text().split()[3]) > eng_max_speed and self.text_language == 1:
            eng_max_speed = int(self.speed_counter.text().split()[3])
        with open(os.path.join('progress', 'progress.txt'), 'w') as f:
            f.write(json.dumps(progress_rus))
            f.write('\n')
            f.write(json.dumps(progress_eng))
            f.write('\n')
            f.write(json.dumps(rus_max_speed))
            f.write('\n')
            f.write(json.dumps(eng_max_speed))

    def set_keyboard_picture(self):
        self.pixmap = QPixmap((os.path.join('keyboards',
                                            'k' + str(codes[self.right_field.type_text.lower()[0]][self.text_language])
                                            + '.png')))
        if self.width() == 1280:
            self.picture_slot.setPixmap(self.pixmap.scaled(1280, self.pixmap.height()
                                                           // (self.pixmap.width() / 1280)))
        if self.width() == resolution.width():
            self.picture_slot.setPixmap(self.pixmap.scaled(resolution.width(), self.pixmap.height()
                                                           // (self.pixmap.width() / resolution.width())))

    def configure_elements(self, ratio):
        self.errors_counter.move(60 * ratio, 30 * ratio)
        self.errors_counter.setFont(QtGui.QFont("Arial", 12 * ratio, QtGui.QFont.Bold))
        self.timer.move(270 * ratio, 30 * ratio)
        self.timer.setFont(QtGui.QFont("Arial", 12 * ratio, QtGui.QFont.Bold))
        self.progress_counter.move(470 * ratio, 30 * ratio)
        self.progress_counter.setFont(QtGui.QFont("Arial", 12 * ratio, QtGui.QFont.Bold))
        self.speed_counter.move(670 * ratio, 30 * ratio)
        self.speed_counter.setFont(QtGui.QFont("Arial", 12 * ratio, QtGui.QFont.Bold))
        self.text_size.move(910 * ratio, 30 * ratio)
        self.text_size.setFont(QtGui.QFont("Arial", 12 * ratio, QtGui.QFont.Bold))
        self.accuracy_counter.move(1110 * ratio, 30 * ratio)
        self.accuracy_counter.setFont(QtGui.QFont("Arial", 12 * ratio, QtGui.QFont.Bold))
        self.picture_slot.move(0, 240 * ratio)

    def change_resolution(self, ratio):
        self.setFixedSize(1280 * ratio, 720 * ratio)
        self.configure_elements(ratio)
        self.right_field.setGeometry(450 * ratio, 110 * ratio, 720 * ratio, 50 * ratio)
        self.left_field.setGeometry(60 * ratio, 110 * ratio, 390 * ratio, 50 * ratio)
        self.right_field.setStyleSheet('background : #abcdef; font-weight: 500; color: black; border: 2px solid green; '
                                       'border-width : 2px 2px 2px 2px;')
        self.right_field.setFont(QFont('Arial', 22 * ratio))
        self.left_field.setStyleSheet('background : #abcdef; font-weight: 500; color: grey; border: 2px solid green; '
                                      'border-width : 2px 0px 2px 2px;')
        self.left_field.setFont(QFont('Arial', 22 * ratio))
        self.set_keyboard_picture()
