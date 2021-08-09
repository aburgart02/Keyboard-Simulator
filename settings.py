import sys
from PyQt5.QtWidgets import QDesktopWidget, QApplication


app = QApplication(sys.argv)
resolution = QDesktopWidget().availableGeometry()
resolution_ratio = resolution.width() / 1280
