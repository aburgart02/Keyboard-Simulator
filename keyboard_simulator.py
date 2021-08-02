from PyQt5 import QtGui, QtCore
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QWidget, QLabel
from input_field import RightField, LeftField


class KeyboardSimulator(QWidget):
    def __init__(self, main):
        super().__init__(main)
        with open(r'texts\buffer.txt', 'r') as f:
            self.text = f.read()
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
            self.pixmap = QPixmap(str(ord(self.right_field.type_text[0])) + '.png')
            if self.width() == 1920:
                self.pixmap = self.pixmap.scaled(self.pixmap.width() * 1.5, self.pixmap.height() * 1.5)
        self.picture_slot.setPixmap(self.pixmap)
        self.picture_slot.adjustSize()

    def configure_elements(self, x):
        self.errors_counter.move(60 * x, 30 * x)
        self.errors_counter.setFont(QtGui.QFont("Arial", 12 * x, QtGui.QFont.Bold))
        self.timer.move(270 * x, 30 * x)
        self.timer.setFont(QtGui.QFont("Arial", 12 * x, QtGui.QFont.Bold))
        self.progress_counter.move(470 * x, 30 * x)
        self.progress_counter.setFont(QtGui.QFont("Arial", 12 * x, QtGui.QFont.Bold))
        self.speed_counter.move(670 * x, 30 * x)
        self.speed_counter.setFont(QtGui.QFont("Arial", 12 * x, QtGui.QFont.Bold))
        self.text_size.move(910 * x, 30 * x)
        self.text_size.setFont(QtGui.QFont("Arial", 12 * x, QtGui.QFont.Bold))
        self.accuracy_counter.move(1110 * x, 30 * x)
        self.accuracy_counter.setFont(QtGui.QFont("Arial", 12 * x, QtGui.QFont.Bold))
        self.picture_slot.move(0, 240 * x)

    def change_resolution(self, x):
        self.setFixedSize(1280 * x, 720 * x)
        self.configure_elements(x)
        self.right_field.setGeometry(450 * x, 110 * x, 720 * x, 50 * x)
        self.left_field.setGeometry(60 * x, 110 * x, 390 * x, 50 * x)
        self.right_field.setStyleSheet('background : #abcdef; font-weight: 500; color: black; font-size:'
                                       + str(24 * x) + 'pt; ''border: 2px solid green; border-width : 2px 2px 2px 2px;')
        self.left_field.setStyleSheet('background : #abcdef; font-weight: 500; color: grey; font-size:'
                                      + str(24 * x) + 'pt; ''border: 2px solid green; border-width : 2px 0px 2px 2px;')
