from PyQt5.QtWidgets import (QApplication, QWidget, QFrame, QMainWindow, QScrollArea, QPushButton, 
							 QLabel, QHBoxLayout, QVBoxLayout, QFormLayout, QFileDialog, QListWidgetItem,
							 QListWidget, QStylePainter, QStyle, QStyleOptionButton, QProxyStyle, QDialog, QLineEdit, QSpinBox, QComboBox, QMessageBox, QStackedWidget, QGraphicsDropShadowEffect, QSizePolicy)
from PyQt5.QtCore import (Qt, pyqtSignal, pyqtSlot, QEvent, QThread, QSize, QTimer)
from PyQt5.QtGui import (QFontMetrics, QFont, QIcon, QCursor) 
from random import choice
from Utils.database import *
from pynput.keyboard import Key, Listener, GlobalHotKeys, Controller, HotKey
from time import sleep
from sys import argv, exit
