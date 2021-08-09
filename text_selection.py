from PyQt5.QtWidgets import QWidget, QPushButton, QFileDialog


class TextSelection(QWidget):
    def __init__(self, main):
        super().__init__(main)
        self.next_window = False
        self.previous_window = False
        self.toggle_full_screen = False
        self.rus_first_text = QPushButton("100 Символов", self)
        self.rus_second_text = QPushButton("200 Символов", self)
        self.rus_third_text = QPushButton("300 Символов", self)
        self.eng_first_text = QPushButton("100 Characters", self)
        self.eng_second_text = QPushButton("200 Characters", self)
        self.eng_third_text = QPushButton("300 Characters", self)
        self.my_text = QPushButton("Выбрать свой текст", self)
        self.configure_elements(1)

    def keyPressEvent(self, e):
        if e.key() == 16777216:
            self.previous_window = True
        if e.key() == 16777274:
            self.toggle_full_screen = True

    def configure_elements(self, ratio):
        self.rus_first_text.move(100 * ratio, 100 * ratio)
        self.rus_first_text.clicked.connect(lambda y: self.set_text(r'texts\rus_100.txt'))
        self.rus_first_text.setStyleSheet('''background-color: green; border-style: outset; border-width: 2px; 
        border-radius: 4px; border-color: blue; font: bold 18px; min-width: 10em; padding: 6px; color: orange;''')
        self.rus_second_text.move(100 * ratio, 200 * ratio)
        self.rus_second_text.clicked.connect(lambda y: self.set_text(r'texts\rus_200.txt'))
        self.rus_third_text.move(100 * ratio, 300 * ratio)
        self.rus_third_text.clicked.connect(lambda y: self.set_text(r'texts\rus_300.txt'))
        self.eng_first_text.move(100 * ratio, 100 * ratio)
        self.eng_first_text.clicked.connect(lambda y: self.set_text(r'texts\eng_100.txt'))
        self.eng_second_text.move(100 * ratio, 200 * ratio)
        self.eng_second_text.clicked.connect(lambda y: self.set_text(r'texts\eng_200.txt'))
        self.eng_third_text.move(100 * ratio, 300 * ratio)
        self.eng_third_text.clicked.connect(lambda y: self.set_text(r'texts\eng_300.txt'))
        self.my_text.move(100 * ratio, 400 * ratio)
        self.my_text.clicked.connect(self.get_text_file)

    def change_resolution(self, ratio):
        self.setFixedSize(1280 * ratio, 720 * ratio)
        self.configure_elements(ratio)

    def set_rus_texts(self):
        self.my_text.show()
        self.rus_first_text.show()
        self.rus_second_text.show()
        self.rus_third_text.show()
        self.eng_first_text.hide()
        self.eng_second_text.hide()
        self.eng_third_text.hide()

    def set_eng_texts(self):
        self.my_text.show()
        self.eng_first_text.show()
        self.eng_second_text.show()
        self.eng_third_text.show()
        self.rus_first_text.hide()
        self.rus_second_text.hide()
        self.rus_third_text.hide()

    def get_text_file(self):
        path = QFileDialog.getOpenFileName()[0]
        with open(path, 'r') as f1:
            with open(r'texts\buffer.txt', 'w') as f2:
                f2.write(f1.read())
        self.next_window = True

    def set_text(self, txt):
        with open(txt, 'r') as f1:
            with open(r'texts\buffer.txt', 'w') as f2:
                f2.write(f1.read())
        self.next_window = True
