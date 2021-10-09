import settings
import os.path
from PyQt5 import QtGui
from PyQt5 import QtCore
from PyQt5.QtCore import QUrl
from PyQt5.QtGui import QTextCursor, QTextCharFormat, QColor
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5.QtWidgets import QTextEdit


class RightField(QTextEdit):
    def __init__(self, window, text):
        super().__init__(window)
        self.setGeometry(450, 110, 720, 50)
        self.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.cursor = self.textCursor()
        self.format = QTextCharFormat()
        self.format.setUnderlineStyle(QTextCharFormat.SingleUnderline)
        self.format.setUnderlineColor(QColor(255, 0, 0))
        self.type_text = text
        self.typed_text = ''
        self.word = ''
        self.words_in_text = text.split()
        self.word_number = 0
        self.letter_number = 0
        self.right_letters_count = 0
        self.index = 0
        self.errors = 0
        self.toggle_full_screen = False
        self.previous_window = False
        self.is_uppercase = False
        self.next_symbol = False
        self.setText(self.type_text)
        self.setReadOnly(True)
        self.media_player = QMediaPlayer()
        self.sound_file = QUrl.fromLocalFile(os.path.join("sounds", "error_sound.mp3"))
        self.media_content = QMediaContent(self.sound_file)
        self.media_player.setMedia(self.media_content)
        self.media_player.setVolume(settings.volume_level)
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
            if settings.print_mode:
                self.compose_word(e)
                self.check_word_correctness()
            if not settings.print_mode:
                if e.key() == 16777219 and len(self.word) != 0 and self.word_number != len(self.words_in_text) - 1:
                    self.type_text = self.words_in_text[self.word_number][self.letter_number - 1] + self.type_text
                    self.next_symbol = True
                    self.letter_number -= 1
                    self.word = self.word[:len(self.word) - 1]
                    self.check_word_correctness()
                if self.word != self.words_in_text[self.word_number][:self.letter_number] and self.type_text[0] == ' ':
                    self.media_player.play()
                    self.errors += 1
                else:
                    self.compose_word(e)
                    self.check_word_correctness()
        except (ValueError, IndexError):
            pass

    def check_word_correctness(self):
        if self.word != self.words_in_text[self.word_number][:self.letter_number]:
            self.highlight_word()
        else:
            self.setText(self.type_text)
        self.index = sum([len(x) for x in self.words_in_text[:self.word_number]]) + self.letter_number \
                                                                                  + self.word_number

    def compose_word(self, e):
        if self.set_register(chr(e.key())) != self.type_text[0]:
            self.errors += 1
        else:
            self.right_letters_count += 1
        self.word += self.set_register(chr(e.key()))
        self.next_symbol = True
        self.letter_number += 1
        if self.type_text[0] == ' ':
            self.word_number += 1
            self.letter_number = 0
            self.word = ''
        self.type_text = self.type_text[1:]

    def highlight_word(self):
        self.setText(self.type_text)
        self.cursor.setPosition(0)
        self.cursor.movePosition(QTextCursor.EndOfWord, 1)
        self.cursor.mergeCharFormat(self.format)

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


class LeftField(QTextEdit):
    def __init__(self, window, text):
        super().__init__(window)
        self.setGeometry(60, 110, 390, 50)
        self.original_text = text
        self.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.setWordWrapMode(QtGui.QTextOption.NoWrap)
        self.cursor = self.textCursor()
        self.format = QTextCharFormat()
        self.format.setUnderlineStyle(QTextCharFormat.SingleUnderline)
        self.format.setUnderlineColor(QColor(255, 76, 91))

    def update(self, word, words_in_text, letter_number, word_number):
        self.setText(word)
        self.setAlignment(QtCore.Qt.AlignRight)
        if word != words_in_text[word_number][:letter_number]:
            self.cursor.setPosition(0)
            self.cursor.movePosition(QTextCursor.End, 1)
            self.cursor.mergeCharFormat(self.format)
