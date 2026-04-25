import sys
from PyQt6.QtWidgets import QApplication, QMainWindow
from PyQt6 import uic
from . import moduls 

class MarketApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = uic.loadUi("market.ui", self)
        
        # FastAPI-like Router Hub
        self.app_router = moduls.AppRouter(self.ui)
        
        # Navigatsiya xaritasi
        self.nav_map = {
    self.ui.btn_side_barcode: "/barcode",
    self.ui.btn_scanner_2: "/scanner",
    self.ui.btn_sozlamalar: "/products",      # Sozlamalar bosilsa asosiy oyna
    self.ui.btn_side_products: "/products",   # Products tugmasi
    self.ui.btn_side_monitor: "/monitor",     # Monitor tugmasi
    self.ui.btn_side_checking: "/checking"    # Checking tugmasi
}

        self.setup_ui_events()
        # Default route
        self.handle_navigation(self.ui.btn_side_barcode, "/barcode")

    def setup_ui_events(self):
        for btn, path in self.nav_map.items():
            btn.clicked.connect(lambda checked, b=btn, p=path: self.handle_navigation(b, p))
        
        # Settings ichidagi tablar
        self.ui.btn_tab_product.clicked.connect(lambda: self.app_router.products.switch_tab(1))
        self.ui.btn_tab_arxiv.clicked.connect(lambda: self.app_router.products.switch_tab(2))
        self.ui.btn_tab_template.clicked.connect(lambda: self.app_router.products.switch_tab(0))
        self.ui.pushButton_4.clicked.connect(lambda: self.app_router.products.switch_tab(3))
        
        # Orqaga qaytish
        self.ui.btn_asosiy_oyna.clicked.connect(lambda: self.ui.btn_side_barcode.click())

    def handle_navigation(self, btn, path):
        self.app_router.route(path)
    
        for side_btn in self.nav_map.keys():
            # Agar bosilgan tugma bo'lsa active=True, bo'lmasa False
            is_active = (side_btn == btn)
            side_btn.setProperty("active", is_active)
        
        # side_btn.style().unpolish(side_btn)
        # side_btn.style().polish(side_btn)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MarketApp()
    window.show()
    sys.exit(app.exec())