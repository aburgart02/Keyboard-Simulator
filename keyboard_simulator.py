import settings
from PyQt5 import QtGui, QtCore
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QWidget, QLabel
from input_field import RightField, LeftField
from settings import resolution, resolution_ratio


class KeyboardSimulator(QWidget):
    def __init__(self, main):
        super().__init__(main)
        self.text = settings.text
        self.right_field = RightField(self, self.text)
        self.left_field = LeftField(self)
        self.errors_counter = QLabel(self)
        self.timer = QLabel(self)
        self.progress_counter = QLabel(self)
        self.speed_counter = QLabel(self)
        self.text_size = QLabel(self)
        self.accuracy_counter = QLabel(self)
        self.picture_slot = QLabel(self)
        self.configure_elements(1)
        self.update_data()
        self.global_timer = QtCore.QTimer()
        self.global_timer.timeout.connect(self.update_data)
        self.global_timer.start(10)

    def update_data(self):
        if len(self.right_field.type_text) == 0:
            self.global_timer.stop()
        self.errors_counter.setText("Число ошибок: " + str(self.right_field.errors))
        self.errors_counter.adjustSize()
        self.timer.setText("Время: " + self.right_field.time.toString())
        self.timer.adjustSize()
        self.progress_counter.setText("Прогресс: " + str(round(100 * self.right_field.index / len(self.text), 1)) + "%")
        self.progress_counter.adjustSize()
        self.speed_counter.setText("Знаков в минуту: " + str(round(60 * self.right_field.index
                                                                   / (self.right_field.time.second()
                                                                      + self.right_field.time.minute() * 60 + 0.1))))
        self.speed_counter.adjustSize()
        self.text_size.setText("Длина текста: " + str(len(self.text)))
        self.text_size.adjustSize()
        self.accuracy_counter.setText("Точность: "
                                      + str(round(100 * self.right_field.index
                                                  / (self.right_field.index + self.right_field.errors + 0.001))) + "%")
        self.accuracy_counter.adjustSize()
        self.left_field.update(self.right_field.typed_text)
        if len(self.right_field.type_text) != 0:
            self.pixmap = QPixmap((r'keyboards\k' + str(ord(self.right_field.type_text[0])) + '.png'))
            if self.width() == resolution.width():
                self.pixmap = self.pixmap.scaled(self.pixmap.width() * resolution_ratio,
                                                 self.pixmap.height() * resolution_ratio)
        self.picture_slot.setPixmap(self.pixmap)
        self.picture_slot.adjustSize()

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
        self.right_field.setStyleSheet('background : #abcdef; font-weight: 500; color: black; font-size:'
                                       + str(24 * ratio) + 'pt; ''border: 2px solid green; '
                                                           'border-width : 2px 2px 2px 2px;')
        self.left_field.setStyleSheet('background : #abcdef; font-weight: 500; color: grey; font-size:'
                                      + str(24 * ratio) + 'pt; ''border: 2px solid green; '
                                                          'border-width : 2px 0px 2px 2px;')
