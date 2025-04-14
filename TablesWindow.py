from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QTableWidget, QTableWidgetItem, QPushButton,
    QMessageBox, QHBoxLayout, QSpacerItem, QSizePolicy, QFormLayout, QLineEdit
)
from PyQt5.QtCore import Qt

class TablesWindow(QWidget):
    def __init__(self, id_):
        super().__init__()
        self.id_ = id_
        self.setWindowTitle("Stoły Rundy")
        self.setGeometry(350, 200, 1200, 600)
