import os.path
import settings
from settings import keys
from PyQt5 import QtGui, QtCore
from PyQt5.QtGui import QPixmap, QFont
from PyQt5.QtWidgets import QWidget, QLabel
from input_field import RightField, LeftField
from settings import codes
from statistics_recorder import StatisticsRecorder
import styles


class KeyboardSimulator(QWidget):
    def __init__(self, main):
        super().__init__(main)
        self.application = main
        self.text = ' '.join(settings.text.replace('\n', ' ').split())
        self.text_id = settings.text_id
        self.text_language = settings.text_language
        self.right_field = RightField(self, self.text)
        self.left_field = LeftField(self)
        self.statistics_recorder = None
        self.errors_counter = QLabel(self)
        self.timer = QLabel(self)
        self.progress_counter = QLabel(self)
        self.speed_counter = QLabel(self)
        self.text_size = QLabel(self)
        self.accuracy_counter = QLabel(self)
        self.picture_slot = QLabel(self)
        self.success_text = QLabel('Упражнение пройдено', self)
        self.success_text.hide()
        self.failure_text = QLabel('Для прохождения необходима точность > 80% и\n'
                                   '        скорость печати > 150 знаков/минуту', self)
        self.failure_text.hide()
        self.is_finished = False
        self.previous_window = False
        self.pixmap = None
        self.configure_elements(1)
        self.update_data()
        self.global_timer = QtCore.QTimer()
        self.global_timer.timeout.connect(self.update_data)
        self.global_timer.start(10)

    def keyPressEvent(self, e):
        if e.key() == keys['ESC_KEY']:
            self.previous_window = True
            self.application.switch_windows()
        if e.key() == keys['F11_KEY']:
            self.change_resolution(1) if self.application.isFullScreen() \
                else self.change_resolution(self.application.resolution_ratio)
            e.ignore()

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
        self.show_result()
        self.is_finished = True
        self.statistics_recorder = StatisticsRecorder(self.text_id, self.text_language, self.speed_counter)
        self.statistics_recorder.record_statistics()

    def show_result(self):
        self.right_field.hide()
        self.left_field.hide()
        self.picture_slot.hide()
        if int(self.speed_counter.text().split()[3]) > 150 \
                and int(self.accuracy_counter.text().split()[1].replace('%', '')) > 80:
            self.success_text.show()
        else:
            self.failure_text.show()

    def set_keyboard_picture(self):
        self.pixmap = QPixmap((os.path.join('keyboards',
                                            'k' + str(codes[self.right_field.type_text.lower()[0]][self.text_language])
                                            + '.png')))
        if self.width() == 1280:
            self.picture_slot.setPixmap(self.pixmap.scaled(1280, self.pixmap.height()
                                                           // (self.pixmap.width() / 1280)))
        if self.width() == self.application.resolution.width():
            self.picture_slot.setPixmap(self.pixmap.scaled(
                self.application.resolution.width(),
                self.pixmap.height() // (self.pixmap.width() / self.application.resolution.width())))

    def configure_elements(self, ratio):
        self.errors_counter.move(60 * ratio, 30 * ratio)
        self.errors_counter.setFont(QtGui.QFont("Arial", 12 * ratio, QtGui.QFont.Bold))
        self.errors_counter.adjustSize()
        self.timer.move(270 * ratio, 30 * ratio)
        self.timer.setFont(QtGui.QFont("Arial", 12 * ratio, QtGui.QFont.Bold))
        self.timer.adjustSize()
        self.progress_counter.move(470 * ratio, 30 * ratio)
        self.progress_counter.setFont(QtGui.QFont("Arial", 12 * ratio, QtGui.QFont.Bold))
        self.progress_counter.adjustSize()
        self.speed_counter.move(670 * ratio, 30 * ratio)
        self.speed_counter.setFont(QtGui.QFont("Arial", 12 * ratio, QtGui.QFont.Bold))
        self.speed_counter.adjustSize()
        self.text_size.move(910 * ratio, 30 * ratio)
        self.text_size.setFont(QtGui.QFont("Arial", 12 * ratio, QtGui.QFont.Bold))
        self.text_size.adjustSize()
        self.accuracy_counter.move(1110 * ratio, 30 * ratio)
        self.accuracy_counter.setFont(QtGui.QFont("Arial", 12 * ratio, QtGui.QFont.Bold))
        self.accuracy_counter.adjustSize()
        self.success_text.setStyleSheet(styles.result_text_style.format(str(24 * ratio)))
        self.success_text.adjustSize()
        self.success_text.move((self.width() - self.success_text.width()) // 2, 300 * ratio)
        self.failure_text.setStyleSheet(styles.result_text_style.format(str(24 * ratio)))
        self.failure_text.adjustSize()
        self.failure_text.move((self.width() - self.failure_text.width()) // 2, 300 * ratio)
        self.picture_slot.move(0, 240 * ratio)

    def change_resolution(self, ratio):
        self.setFixedSize(1280 * ratio, 720 * ratio)
        self.configure_elements(ratio)
        self.right_field.setGeometry(450 * ratio, 110 * ratio, 720 * ratio, 50 * ratio)
        self.left_field.setGeometry(60 * ratio, 110 * ratio, 390 * ratio, 50 * ratio)
        self.right_field.setStyleSheet(styles.right_printing_field_style)
        self.right_field.setFont(QFont('Arial', 24 * ratio))
        self.left_field.setStyleSheet(styles.left_printing_field_style)
        self.left_field.setFont(QFont('Arial', 24 * ratio))
        if not self.is_finished:
            self.set_keyboard_picture()
