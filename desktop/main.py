import sys
import os
from PyQt6.QtWidgets import QApplication, QMainWindow
from PyQt6 import uic
from moduls import AppRouter # Router importi

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

class MarketApp(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi(os.path.join(BASE_DIR, "market.ui"), self)
        self.router = AppRouter(self)
        

        # 2. Modullarni router orqali olish
        self.init_signals()
        
        # 3. Default sahifa - Foydalanuvchi talabi
        self.router.route("/barcode")

    def init_signals(self):
        """Tugmalarni ulash - Har bir tugma faqat bir marta ulansin"""
        
        # Sidebar tugmalari
        if hasattr(self, 'btn_side_barcode'):
            self.btn_side_barcode.clicked.connect(lambda: self.router.route("/barcode"))

        
        if hasattr(self, 'btn_side_scanner'):
            self.btn_side_scanner.clicked.connect(lambda: self.router.route("/scanner"))

        if hasattr(self, 'btn_side_products'):
            self.btn_side_products.clicked.connect(self.on_products_menu_clicked)

        if hasattr(self, 'btn_sozlamalar'):
            self.btn_sozlamalar.clicked.connect(self.on_products_menu_clicked)

        # Monitor va Checking
        if hasattr(self, 'btn_side_monitor'):
            self.btn_side_monitor.clicked.connect(self.on_monitor_clicked)

        if hasattr(self, 'btn_side_checking'):
            self.btn_side_checking.clicked.connect(self.on_checking_clicked)
        
        self.router.template_edit_mod.template_saved_signal.connect(self.router.template_mod.refresh_data)
        
        # Tahrirlash/Qo'shish mantiqi
        if hasattr(self, 'btn_add_template'):
            # Plus (+) tugmasi bosilganda Routerning open_add_view funksiyasini chaqiradi
            self.btn_add_template.clicked.connect(self.router.open_add_view)

        if hasattr(self.router, 'template_edit_mod'):
            # self.load_templates funksiyasi mavjudligiga ishonch hosil qiling
            if hasattr(self, 'load_templates'):
                self.router.template_edit_mod.template_saved_signal.connect(self.load_templates)
                print("Signal muvaffaqiyatli bog'landi!")

        if hasattr(self, 'btn_asosiy_oyna'):
            try:
                # Avvalgi ulanishlarni tozalaymiz
                self.btn_asosiy_oyna.clicked.disconnect()
            except:
                pass

            self.btn_asosiy_oyna.clicked.connect(
                lambda: self.sidebar_stack.setCurrentWidget(self.page_barcode_scanner_Sozlamalar)
            )
            print("Signal: Asosiy oynaga qaytish (sidebar_stack orqali) muvaffaqiyatli ulandi!")
        # Saqlash tugatilganda refresh_data ni chaqirish
        self.router.template_edit_mod.template_saved_signal.connect(self.router.template_mod.refresh_data)
        # Rasm tanlash tugmasini ulash
        if hasattr(self, 'btn_select_photo'):
            self.btn_select_photo.clicked.connect(self.router.template_edit_mod.select_image)

        # Saqlash tugmasini ulash
        if hasattr(self, 'template_edit_save'):
            self.template_edit_save.clicked.connect(self.router.template_edit_mod.save_all_data)
    def edit_existing_product(self, product_data):
        """Qalamcha bosilganda ma'lumotlarni tahrirlash oynasiga yuboradi"""
        self.router.route("/products_menu")

        if hasattr(self.router, 'template_mod'):
            self.router.template_mod.edit_product(product_data)

    def on_products_menu_clicked(self):
        self.router.route("/products_menu")

    def on_monitor_clicked(self):
        self.router.route("/monitor")

    def on_checking_clicked(self):
        self.router.route("/checking")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MarketApp()
    window.show()
    sys.exit(app.exec())