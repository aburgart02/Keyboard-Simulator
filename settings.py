import sys
from PyQt5.QtWidgets import QDesktopWidget, QApplication


text = 'text'
volume_level = 50
app = QApplication(sys.argv)
resolution = QDesktopWidget().availableGeometry()
resolution_ratio = resolution.width() / 1280
