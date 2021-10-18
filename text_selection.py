import random
import json
import os.path
import settings
from settings import keys
from PyQt5.QtWidgets import QWidget, QPushButton, QFileDialog
from PyQt5.QtCore import QSize
from PyQt5.QtGui import QIcon
from functools import partial
import styles


class TextSelection(QWidget):
    def __init__(self, main):
        super().__init__(main)
        self.next_window = False
        self.previous_window = False
        self.toggle_full_screen = False
        self.initialize_rus_texts()
        self.initialize_eng_texts()
        self.mark_picture = QIcon(os.path.join('materials', 'mark.png'))
        self.cross_picture = QIcon(os.path.join('materials', 'cross.png'))
        self.assign_buttons()
        self.configure_elements(1)

    def keyPressEvent(self, e):
        if e.key() == keys['ESC_KEY']:
            self.previous_window = True
        if e.key() == keys['F11_KEY']:
            self.toggle_full_screen = True

    def initialize_rus_texts(self):
        self.rus_lesson_1 = QPushButton("       Урок 1", self)
        self.rus_lesson_2 = QPushButton("       Урок 2", self)
        self.rus_lesson_3 = QPushButton("       Урок 3", self)
        self.rus_lesson_4 = QPushButton("       Урок 4", self)
        self.rus_lesson_5 = QPushButton("       Урок 5", self)
        self.rus_lesson_6 = QPushButton("       Урок 6", self)
        self.rus_lesson_7 = QPushButton("       Урок 7", self)
        self.rus_lesson_8 = QPushButton("       Урок 8", self)
        self.rus_lesson_9 = QPushButton("       Урок 9", self)
        self.rus_lesson_10 = QPushButton("       Урок 10", self)
        self.rus_text_1 = QPushButton("Короткий книжный текст", self)
        self.rus_text_2 = QPushButton("Средний книжный текст", self)
        self.rus_text_3 = QPushButton("Длинный книжный текст", self)
        self.rus_random_text = QPushButton("Случайный текст", self)
        self.rus_my_text = QPushButton("Выбрать свой текст", self)
        self.rus_texts = [self.rus_lesson_1, self.rus_lesson_2, self.rus_lesson_3, self.rus_lesson_4,
                          self.rus_lesson_5, self.rus_lesson_6, self.rus_lesson_7, self.rus_lesson_8,
                          self.rus_lesson_9, self.rus_lesson_10, self.rus_text_1, self.rus_text_2,
                          self.rus_text_3, self.rus_random_text, self.rus_my_text]

    def initialize_eng_texts(self):
        self.eng_lesson_1 = QPushButton("       Lesson 1", self)
        self.eng_lesson_2 = QPushButton("       Lesson 2", self)
        self.eng_lesson_3 = QPushButton("       Lesson 3", self)
        self.eng_lesson_4 = QPushButton("       Lesson 4", self)
        self.eng_lesson_5 = QPushButton("       Lesson 5", self)
        self.eng_lesson_6 = QPushButton("       Lesson 6", self)
        self.eng_lesson_7 = QPushButton("       Lesson 7", self)
        self.eng_lesson_8 = QPushButton("       Lesson 8", self)
        self.eng_lesson_9 = QPushButton("       Lesson 9", self)
        self.eng_lesson_10 = QPushButton("       Lesson 10", self)
        self.eng_text_1 = QPushButton("Short literary text", self)
        self.eng_text_2 = QPushButton("Average literary text", self)
        self.eng_text_3 = QPushButton("Long literary text", self)
        self.eng_random_text = QPushButton("Random text", self)
        self.eng_my_text = QPushButton("Choose your own text", self)
        self.eng_texts = [self.eng_lesson_1, self.eng_lesson_2, self.eng_lesson_3, self.eng_lesson_4,
                          self.eng_lesson_5, self.eng_lesson_6, self.eng_lesson_7, self.eng_lesson_8,
                          self.eng_lesson_9, self.eng_lesson_10, self.eng_text_1, self.eng_text_2,
                          self.eng_text_3, self.eng_random_text, self.eng_my_text]

    def configure_elements(self, ratio):
        with open(os.path.join('progress', 'progress.txt'), 'r') as f:
            data = f.readlines()
        progress_rus = json.loads(data[0])
        progress_eng = json.loads(data[1])
        for buttons in [self.rus_texts, self.eng_texts]:
            count = 0
            row = 1
            column = 1
            for button in buttons:
                if row / 5 > 1:
                    column += 1
                    row = 1
                button.move(360 * ratio * column - 240 * ratio, 100 * ratio * row)
                button.setStyleSheet(styles.lesson_button_style.format(str(int(26 * ratio))))
                if count < 10:
                    self.set_icon(button, count, ratio, progress_rus, progress_eng)
                button.adjustSize()
                row += 1
                count += 1

    def set_icon(self, button, count, ratio, progress_rus, progress_eng):
        if button in self.rus_texts:
            if progress_rus[count]:
                button.setIcon(self.mark_picture)
            else:
                button.setIcon(self.cross_picture)
        if button in self.eng_texts:
            if progress_eng[count]:
                button.setIcon(self.mark_picture)
            else:
                button.setIcon(self.cross_picture)
        button.setIconSize(QSize(30 * ratio, 30 * ratio))

    def assign_buttons(self):
        for k in range(len(self.rus_texts) - 2):
            self.rus_texts[k].clicked.connect(partial(self.set_text, os.path.join('texts', 'rus_texts',
                                                                                  't' + str(k) + '.txt'), k, 0))
            self.rus_texts[k].setAutoDefault(True)
        for k in range(len(self.eng_texts) - 2):
            self.eng_texts[k].clicked.connect(partial(self.set_text, os.path.join('texts', 'eng_texts',
                                                                                  't' + str(k) + '.txt'), k, 1))
            self.eng_texts[k].setAutoDefault(True)
        self.rus_my_text.clicked.connect(self.get_text_file)
        self.rus_my_text.setAutoDefault(True)
        self.eng_my_text.clicked.connect(self.get_text_file)
        self.eng_my_text.setAutoDefault(True)
        self.rus_random_text.clicked.connect(lambda x: self.create_text(os.path.join('texts',
                                                                                     'rus_texts', 'rus_words.txt'), 0))
        self.rus_random_text.setAutoDefault(True)
        self.eng_random_text.clicked.connect(lambda x: self.create_text(os.path.join('texts', 'eng_texts',
                                                                                     'eng_words.txt'), 1))
        self.eng_random_text.setAutoDefault(True)

    def change_resolution(self, ratio):
        self.setFixedSize(1280 * ratio, 720 * ratio)
        self.configure_elements(ratio)

    def set_rus_texts(self):
        [text.show() for text in self.rus_texts]
        [text.hide() for text in self.eng_texts]

    def set_eng_texts(self):
        [text.show() for text in self.eng_texts]
        [text.hide() for text in self.rus_texts]

    def create_text(self, path, text_language):
        text = ''
        with open(path, 'r', encoding='utf-8') as f:
            words = f.read().split('\n')
        for _ in range(0, 30):
            text += words[random.randint(0, len(words) - 1)] + ' '
        settings.text = text.strip()
        settings.text_language = text_language
        self.next_window = True

    def get_text_file(self):
        try:
            path = QFileDialog.getOpenFileName()[0]
            with open(path, 'r', encoding='utf-8-sig') as f1:
                settings.text = f1.read()
            self.next_window = True
        except FileNotFoundError:
            pass

    def set_text(self, path, text_id, text_language):
        with open(path, 'r', encoding='utf-8-sig') as f1:
            settings.text = f1.read()
            settings.text_language = text_language
            settings.text_id = text_id
        self.next_window = True
