from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel

class CheckingModule(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)
        self.label = QLabel("Checking Sahifasi Aktiv")
        layout.addWidget(self.label)