import random
import json
import os.path
import settings
from key_handler import key_processing
from settings import rus_button_names, eng_button_names
from PyQt5.QtWidgets import QWidget, QPushButton, QFileDialog
from PyQt5.QtCore import QSize
from PyQt5.QtGui import QIcon
from functools import partial
import styles


class TextSelection(QWidget):
    def __init__(self, main):
        super().__init__(main)
        self.application = main
        self.next_window = False
        self.previous_window = False
        self.rus_texts = []
        self.eng_texts = []
        self.initialize_rus_texts()
        self.initialize_eng_texts()
        self.mark_picture = QIcon(os.path.join('materials', 'mark.png'))
        self.cross_picture = QIcon(os.path.join('materials', 'cross.png'))
        self.assign_buttons()
        self.configure_elements(1)

    def keyPressEvent(self, e):
        key_processing(self, e)

    def initialize_rus_texts(self):
        for name in rus_button_names:
            button = QPushButton(name, self)
            self.rus_texts.append(button)

    def initialize_eng_texts(self):
        for name in eng_button_names:
            button = QPushButton(name, self)
            self.eng_texts.append(button)

    def configure_elements(self, ratio):
        with open(os.path.join('progress', 'progress.txt'), 'r') as f:
            statistics = json.load(f)
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
                    self.set_icon(button, count, ratio, statistics['rus_progress'], statistics['eng_progress'])
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
            self.rus_texts[k].clicked.connect(partial(self.set_text, os.path.join(
                'texts', 'rus_texts', 't' + str(k) + '.txt'), k, 0))
            self.rus_texts[k].setAutoDefault(True)
        for k in range(len(self.eng_texts) - 2):
            self.eng_texts[k].clicked.connect(partial(self.set_text, os.path.join(
                'texts', 'eng_texts', 't' + str(k) + '.txt'), k, 1))
            self.eng_texts[k].setAutoDefault(True)
        self.rus_texts[len(self.rus_texts) - 1].clicked.connect(self.get_text_file)
        self.rus_texts[len(self.rus_texts) - 1].setAutoDefault(True)
        self.eng_texts[len(self.eng_texts) - 1].clicked.connect(self.get_text_file)
        self.eng_texts[len(self.eng_texts) - 1].setAutoDefault(True)
        self.rus_texts[len(self.rus_texts) - 2].clicked.connect(lambda x: self.create_text(os.path.join(
            'texts', 'rus_texts', 'rus_words.txt'), 0))
        self.rus_texts[len(self.rus_texts) - 2].setAutoDefault(True)
        self.eng_texts[len(self.eng_texts) - 2].clicked.connect(lambda x: self.create_text(os.path.join(
            'texts', 'eng_texts', 'eng_words.txt'), 1))
        self.eng_texts[len(self.eng_texts) - 2].setAutoDefault(True)

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
        self.application.switch_windows()

    def get_text_file(self):
        try:
            path = QFileDialog.getOpenFileName()[0]
            with open(path, 'r', encoding='utf-8-sig') as f1:
                settings.text = f1.read()
            self.next_window = True
            self.application.switch_windows()
        except FileNotFoundError:
            pass

    def set_text(self, path, text_id, text_language):
        with open(path, 'r', encoding='utf-8-sig') as f1:
            settings.text = f1.read()
            settings.text_language = text_language
            settings.text_id = text_id
        self.next_window = True
        self.application.switch_windows()
