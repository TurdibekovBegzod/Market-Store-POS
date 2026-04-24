import os
import sys
from PyQt6.QtWidgets import QApplication, QMainWindow
from PyQt6 import uic
base_dir = os.path.dirname(os.path.abspath(__file__))
ui_path = os.path.join(base_dir, "market.ui")
class BarcodeApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = uic.loadUi(ui_path, self)
        
        self.sidebar_buttons = [
            self.ui.btn_barcode, 
            self.ui.btn_scanner, 
            self.ui.pushButton_5
        ]
        
        # 1. Barcode, Scanner, Sozlamalar tugmalarini sahifalarga bog'lash
        self.ui.btn_barcode.clicked.connect(lambda: self.update_ui(self.ui.btn_barcode, 0))
        self.ui.btn_scanner.clicked.connect(lambda: self.update_ui(self.ui.btn_scanner, 1))
        self.ui.pushButton_5.clicked.connect(lambda: self.update_ui(self.ui.pushButton_5, 2))

        # 2. Edit va Yuklash tugmalarini bog'lash
        self.ui.btn_edit.clicked.connect(self.handle_edit)
        self.ui.btn_yuklash.clicked.connect(self.handle_upload)

        # Dastur ochilganda Barcode sahifasi aktiv bo'lsin
        self.update_ui(self.ui.btn_barcode, 0)
        
    def update_ui(self, clicked_button, page_index):
        for btn in self.sidebar_buttons:
            btn.setProperty("active", "false")
        
        # Bosilgan activ 
        clicked_button.setProperty("active", "true")
        
        for btn in self.sidebar_buttons:
            btn.style().unpolish(btn)
            btn.style().polish(btn)
            btn.update()
        
        # Sahifani almashtirish
        self.ui.stackedWidget.setCurrentIndex(page_index)
  
    def handle_edit(self):
        sheet_id = self.ui.lineEdit_edit.text()
        if sheet_id:
            print(f"Google Sheet ID saqlandi: {sheet_id}")
        else:
            print("Iltimos, Google Sheet ID kiriting!")

    def handle_upload(self):
        creds_path = self.ui.lineEdit_yukash.text()
        if creds_path:
            print(f"Credentials fayli yuklanmoqda: {creds_path}")
        else:
            print("Fayl yo'li ko'rsatilmadi!")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = BarcodeApp()
    window.show()
    sys.exit(app.exec())