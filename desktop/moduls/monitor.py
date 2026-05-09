from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel

class MonitorModule(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)
        self.label = QLabel("Monitor Sahifasi Aktiv")
        layout.addWidget(self.label)