from PyQt5 import QtCore
from PyQt5.QtCore import QUrl
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5.QtWidgets import QLineEdit


class RightField(QLineEdit):
    def __init__(self, window, text):
        super().__init__(window)
        self.setGeometry(450, 110, 720, 50)
        self.type_text = text
        self.typed_text = ''
        self.index = 0
        self.toggle_full_screen = False
        self.previous_window = False
        self.is_uppercase = False
        self.setText(self.type_text)
        self.setCursorPosition(0)
        self.setReadOnly(True)
        self.setStyleSheet('background : #abcdef; font-weight: 500; color: black; font-size:24pt; '
                           'border: 2px solid green; border-width : 2px 2px 2px 2px;')
        self.errors = 0
        self.media_player = QMediaPlayer()
        self.sound_file = QUrl.fromLocalFile(r"sounds\error_sound.mp3")
        self.media_content = QMediaContent(self.sound_file)
        self.media_player.setMedia(self.media_content)
        self.media_player.setVolume(50)
        self.time = QtCore.QTime(0, 0, 0)
        self.timer = QtCore.QTimer()
        self.timer_flag = False

    def keyPressEvent(self, e):
        if not self.timer_flag:
            self.timer.start(1000)
            self.timer.timeout.connect(self.tick)
            self.timer_flag = True
        try:
            if e.key() == 16777216:
                self.previous_window = True
            if e.key() == 16777274:
                self.toggle_full_screen = True
            if e.key() == 16777248:
                self.is_uppercase = True
            if self.set_register(chr(e.key())) == self.type_text[0]:
                self.type_text = self.type_text[1:]
                self.setText(self.type_text)
                self.setCursorPosition(0)
                self.typed_text += self.set_register(chr(e.key()))
                self.index += 1
            else:
                self.errors += 1
                self.media_player.play()
        except ValueError:
            pass

    def set_register(self, c):
        if self.is_uppercase:
            return c.upper()
        else:
            return c.lower()

    def keyReleaseEvent(self, e):
        if e.key() == 16777248:
            self.is_uppercase = False

    def tick(self):
        self.time = self.time.addSecs(1)


class LeftField(QLineEdit):
    def __init__(self, window):
        super().__init__(window)
        self.setGeometry(60, 110, 390, 50)
        self.setAlignment(QtCore.Qt.AlignmentFlag.AlignRight)
        self.setStyleSheet('background : #abcdef; font-weight: 500; color: grey; font-size:24pt; '
                           'border: 2px solid green; border-width : 2px 0px 2px 2px;')

    def update(self, typed_text):
        self.setText(typed_text)
