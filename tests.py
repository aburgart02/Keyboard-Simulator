import sys
import os.path
import settings
import json
from PyQt5 import QtGui
from PyQt5.QtCore import QEvent, Qt
from PyQt5.QtWidgets import QApplication
from main_window import MainWindow
from keyboard_simulator import KeyboardSimulator
from settings_window import Settings
from print_mode_selection import PrintModeSelection
from progress_window import Progress
from text_selection import TextSelection
from input_field import RightField


app = QApplication(sys.argv)
main_window = MainWindow()
keyboard_simulator_window = KeyboardSimulator(main_window)
settings_window = Settings(main_window)
print_mode_selection_window = PrintModeSelection(main_window)
progress_window = Progress(main_window)
text_selection_window = TextSelection(main_window)


class TestMainWindow:
    def test_main_window_sizes(self):
        assert main_window.size().width() == 1280 and main_window.size().height() == 720

    def test_background_loading(self):
        assert type(main_window.background) is QtGui.QImage

    def test_toggle_full_screen_on_off(self):
        main_window.change_main_window_resolution()
        assert main_window.isFullScreen()
        main_window.change_main_window_resolution()
        assert not main_window.isFullScreen()

    def test_timer_activity(self):
        assert main_window.global_timer.isActive()


class TestSettings:
    def test_volume_addition(self):
        volume_level = settings.volume_level
        settings_window.change_volume(True)
        assert volume_level < settings.volume_level

    def test_volume_reduction(self):
        volume_level = settings.volume_level
        settings_window.change_volume(False)
        assert volume_level > settings.volume_level

    def test_next_background_file_setting(self):
        background_file = settings_window.background_file
        settings_window.set_background_file_name(True)
        assert background_file is not settings_window.background_file

    def test_previous_background_file_setting(self):
        background_file = settings_window.background_file
        settings_window.set_background_file_name(False)
        assert background_file is not settings_window.background_file


class TestProgress:
    def test_languages_progress_getting(self):
        with open(os.path.join('progress', 'progress.txt'), 'r') as f:
            data = f.readlines()
        progress_window.get_progress_data()
        assert progress_window.rus_progress == sum(json.loads(data[0])) \
               and progress_window.eng_progress == sum(json.loads(data[1]))

    def test_highest_speed_getting(self):
        with open(os.path.join('progress', 'progress.txt'), 'r') as f:
            data = f.readlines()
        progress_window.get_progress_data()
        assert progress_window.rus_max_speed == json.loads(data[2]) \
               and progress_window.eng_max_speed == json.loads(data[3])


class TestPrintModeSelection:
    def test_russian_keyboard_layout_selection(self):
        print_mode_selection_window.first_text_button.click()
        assert print_mode_selection_window.keyboard_layout == 'rus'

    def test_english_keyboard_layout_selection(self):
        print_mode_selection_window.second_text_button.click()
        assert print_mode_selection_window.keyboard_layout == 'eng'

    def test_toggle_error_ignoring_mode_on(self):
        print_mode_selection_window.change_mode()
        assert settings.print_mode is True

    def test_toggle_error_ignoring_mode_off(self):
        print_mode_selection_window.change_mode()
        assert settings.print_mode is False


class TestTextSelection:
    def test_text_creation(self):
        text_selection_window.create_text(os.path.join('texts', 'eng_texts', 'eng_words.txt'), 1)
        assert len(settings.text.split()) == 30

    def test_russian_text_button_initialization(self):
        text_selection_window.initialize_rus_texts()
        assert len(text_selection_window.rus_texts) == 15

    def test_english_text_button_initialization(self):
        text_selection_window.initialize_eng_texts()
        assert len(text_selection_window.eng_texts) == 15

    def test_text_setting(self):
        with open(os.path.join('texts', 'eng_texts', 't1.txt'), 'r') as f:
            text = f.read()
        text_selection_window.set_text(os.path.join('texts', 'eng_texts', 't1.txt'), 1, 1)
        assert settings.text == text and settings.text_language == 1 and settings.text_id == 1


class TestKeyboardSimulator:
    def test_timer_activity(self):
        assert keyboard_simulator_window.global_timer.isActive()

    def test_printing_finish(self):
        keyboard_simulator_window.finish_printing()
        assert keyboard_simulator_window.statistics_recorder is not None

    def test_keyboard_picture_slot(self):
        keyboard_simulator_window.set_keyboard_picture()
        assert keyboard_simulator_window.pixmap is not None


class TestInputField:
    def test_letter_adding(self):
        right_input_field = RightField(keyboard_simulator_window, 'do test')
        key = QtGui.QKeyEvent(QEvent.KeyPress, Qt.Key_A, Qt.NoModifier)
        right_input_field.keyPressEvent(key)
        assert right_input_field.word == 'a'

    def test_letter_number_increasing(self):
        right_input_field = RightField(keyboard_simulator_window, 'do test')
        key = QtGui.QKeyEvent(QEvent.KeyPress, Qt.Key_A, Qt.NoModifier)
        right_input_field.keyPressEvent(key)
        assert right_input_field.letter_number == 1

    def test_right_word_printed(self):
        right_input_field = RightField(keyboard_simulator_window, 'do test')
        key = QtGui.QKeyEvent(QEvent.KeyPress, Qt.Key_D, Qt.NoModifier)
        right_input_field.keyPressEvent(key)
        key = QtGui.QKeyEvent(QEvent.KeyPress, Qt.Key_O, Qt.NoModifier)
        right_input_field.keyPressEvent(key)
        key = QtGui.QKeyEvent(QEvent.KeyPress, Qt.Key_Space, Qt.NoModifier)
        right_input_field.keyPressEvent(key)
        assert right_input_field.word == ''

    def test_right_word_printed_word_number_increasing(self):
        right_input_field = RightField(keyboard_simulator_window, 'do test')
        key = QtGui.QKeyEvent(QEvent.KeyPress, Qt.Key_D, Qt.NoModifier)
        right_input_field.keyPressEvent(key)
        key = QtGui.QKeyEvent(QEvent.KeyPress, Qt.Key_O, Qt.NoModifier)
        right_input_field.keyPressEvent(key)
        key = QtGui.QKeyEvent(QEvent.KeyPress, Qt.Key_Space, Qt.NoModifier)
        right_input_field.keyPressEvent(key)
        assert right_input_field.word_number == 1

    def test_wrong_word_printed_errors_are_critical(self):
        right_input_field = RightField(keyboard_simulator_window, 'do test')
        key = QtGui.QKeyEvent(QEvent.KeyPress, Qt.Key_D, Qt.NoModifier)
        right_input_field.keyPressEvent(key)
        key = QtGui.QKeyEvent(QEvent.KeyPress, Qt.Key_A, Qt.NoModifier)
        right_input_field.keyPressEvent(key)
        key = QtGui.QKeyEvent(QEvent.KeyPress, Qt.Key_Space, Qt.NoModifier)
        right_input_field.keyPressEvent(key)
        assert right_input_field.word == 'da'

    def test_wrong_word_printed_errors_are_critical_word_number_increasing(self):
        right_input_field = RightField(keyboard_simulator_window, 'do test')
        key = QtGui.QKeyEvent(QEvent.KeyPress, Qt.Key_D, Qt.NoModifier)
        right_input_field.keyPressEvent(key)
        key = QtGui.QKeyEvent(QEvent.KeyPress, Qt.Key_A, Qt.NoModifier)
        right_input_field.keyPressEvent(key)
        key = QtGui.QKeyEvent(QEvent.KeyPress, Qt.Key_Space, Qt.NoModifier)
        right_input_field.keyPressEvent(key)
        assert right_input_field.word_number == 0

    def test_wrong_word_printed_error_ignoring_mode(self):
        settings.print_mode = True
        right_input_field = RightField(keyboard_simulator_window, 'do test')
        key = QtGui.QKeyEvent(QEvent.KeyPress, Qt.Key_D, Qt.NoModifier)
        right_input_field.keyPressEvent(key)
        key = QtGui.QKeyEvent(QEvent.KeyPress, Qt.Key_A, Qt.NoModifier)
        right_input_field.keyPressEvent(key)
        key = QtGui.QKeyEvent(QEvent.KeyPress, Qt.Key_Space, Qt.NoModifier)
        right_input_field.keyPressEvent(key)
        assert right_input_field.word == ''

    def test_error_count_adding(self):
        right_input_field = RightField(keyboard_simulator_window, 'do test')
        key = QtGui.QKeyEvent(QEvent.KeyPress, Qt.Key_A, Qt.NoModifier)
        right_input_field.keyPressEvent(key)
        assert right_input_field.errors == 1
