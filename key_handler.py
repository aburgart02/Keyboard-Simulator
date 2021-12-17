from settings import keys


def key_processing(window, e):
    if e.key() == keys['ESC_KEY']:
        window.previous_window = True
        window.application.switch_windows()
    if e.key() == keys['F11_KEY']:
        window.change_resolution(1) if window.application.isFullScreen() \
            else window.change_resolution(window.application.resolution_ratio)
        e.ignore()
