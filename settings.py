import sys
from PyQt5.QtWidgets import QDesktopWidget, QApplication


text = 'text'
text_language = 0
text_id = None
volume_level = 50
app = QApplication(sys.argv)
resolution = QDesktopWidget().availableGeometry()
resolution_ratio = resolution.width() / 1280
codes = {'~': [1, 1], '`': [1, 1], 'ё': [1, 1], '1': [2, 2], '!': [2, 2], '2': [3, 3], '@': [3, 3], '"': [3, 36],
         '3': [4, 4], '#': [4, 4], '№': [4, 4], '$': [5, 5], '4': [5, 5], ';': [5, 35], '5': [6, 6], '%': [6, 6],
         '6': [7, 7], '^': [7, 7], ':': [7, 35], '7': [8, 8], '&': [8, 8], '?': [8, 46], '8': [9, 9], '*': [9, 9],
         '9': [10, 10], '(': [10, 10], '0': [11, 11], ')': [11, 11], '-': [12, 12], '_': [12, 12], '+': [13, 13],
         '=': [13, 13], 'q': [14, 14], 'й': [14, 14], 'w': [15, 15], 'ц': [15, 15], 'e': [16, 16], 'у': [16, 16],
         'r': [17, 17], 'к': [17, 17], 't': [18, 18], 'е': [18, 18], 'y': [19, 19], 'н': [19, 19], 'u': [20, 20],
         'г': [20, 20], 'i': [21, 21], 'ш': [21, 21], 'o': [22, 22], 'щ': [22, 22], 'p': [23, 23], 'з': [23, 23],
         '[': [24, 24], '{': [24, 24], 'х': [24, 24], ']': [25, 25], '}': [25, 25], 'ъ': [25, 25], 'a': [26, 26],
         'ф': [26, 26], 's': [27, 27], 'ы': [27, 27], 'd': [28, 28], 'в': [28, 28], 'f': [29, 29], 'а': [29, 29],
         'g': [30, 30], 'п': [30, 30], 'h': [31, 31], 'р': [31, 31], 'j': [32, 32], 'о': [32, 32], 'k': [33, 33],
         'л': [33, 33], 'l': [34, 34], 'д': [34, 34], 'ж': [35, 35], 'э': [36, 36], '\'': [36, 36], 'z': [37, 37],
         'я': [37, 37], 'x': [38, 38], 'ч': [38, 38], 'c': [39, 39], 'с': [39, 39], 'v': [40, 40], 'м': [40, 40],
         'b': [41, 41], 'и': [41, 41], 'n': [42, 42], 'т': [42, 42], 'm': [43, 43], 'ь': [43, 43], '<': [44, 44],
         ',': [46, 44], 'б': [44, 44], '>': [45, 45], '.': [46, 45], 'ю': [45, 45], '/': [46, 46], ' ': [47, 47]}
