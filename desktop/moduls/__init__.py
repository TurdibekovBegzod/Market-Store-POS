from moduls.sozlamalar import SozlamalarModule
from moduls.barcode import BarcodeModule
from .products import ProductsModule
from .products_template import ProductsTemplateModule
from .monitor import MonitorModule
from .checking import CheckingModule
from .template_edit import TemplateEditModule

class AppRouter:
    def __init__(self, ui):
        self.ui = ui
        self.selected_image_path = None
        
        # 1. Asosiy katta stack (barcode va products o'rtasida almashadi)
        self.stacked_main = ui.stacked_ong
        
        # 2. Ichki stack (page_products ichidagi shablon va tahrirlash oynasi)
        self.settings_stack = ui.settings_content_stack
        
        # 3. Sidebar stack (chap tomondagi tugmalar paneli)
        self.sidebar_stack = ui.sidebar_stack

        self.barcode_mod = BarcodeModule(ui)
        self.settings_mod = SozlamalarModule(ui)
        self.products_mod = ProductsModule(self.ui)
        self.template_mod = ProductsTemplateModule(ui)
        self.template_edit_mod = TemplateEditModule(ui)

        # Monitor va Checking modullari
        self.monitor_page = MonitorModule()
        self.checking_page = CheckingModule()

        # Sahifalarni asosiy stack-ga qo'shish (agar Designer-da qo'shilmagan bo'lsa)
        if self.stacked_main.indexOf(self.monitor_page) == -1:
            self.stacked_main.addWidget(self.monitor_page)
        if self.stacked_main.indexOf(self.checking_page) == -1:
            self.stacked_main.addWidget(self.checking_page)
         
        self.setup_connections()
        print("Router: Barcha ulanishlar va iyerarxiya muvaffaqiyatli sozlandi.")

    def setup_connections(self):
        """Asosiy menyu tugmalarini ulaymiz"""
        # Sidebar: Products bosilganda
        if hasattr(self.ui, 'btn_side_products'):
            self.ui.btn_side_products.clicked.connect(lambda: self.route("/products_menu"))
            
        # Sidebar: Barcode bosilganda
        if hasattr(self.ui, 'btn_side_barcode'):
            self.ui.btn_side_barcode.clicked.connect(lambda: self.route("/barcode")) 
 
        if hasattr(self.ui, 'btn_asosiy_oyna'):
            try:
                # Avvalgi ulanishlarni tozalash (dublikat bo'lmasligi uchun)
                self.ui.btn_asosiy_oyna.clicked.disconnect()
            except:
                pass
            
            self.ui.btn_asosiy_oyna.clicked.connect(lambda: self.route("/barcode_settings"))

                
        # Tahrirlash oynasidagi "Orqaga" tugmasi
        if hasattr(self.ui, 'template_edit_orqaga'):
            self.ui.template_edit_orqaga.clicked.connect(lambda: self.route("/products_menu"))

        if hasattr(self.ui, 'delete_2'):
            try:
                # Avvalgi barcha bog'lanishlarni uzamiz 
                self.ui.delete_2.clicked.disconnect()
            except:
                pass
            
            # Faqat o'chirish funksiyasiga bog'laymiz
            self.ui.delete_2.clicked.connect(self.template_edit_mod.delete_current_template)

        if hasattr(self.ui, 'btn_select_photo'):
            self.ui.btn_select_photo.clicked.connect(self.template_edit_mod.select_image)    
    def open_add_view(self):
        """ Yangi qo'shish """
        self.template_edit_mod.editing_product_id = None # ID-ni o'chirish shart!
        self.template_edit_mod.clear_fields()
        self.ui.template_edit_save.setText("Saqlash")
        self.route("/open_template_editor")

    def open_edit_view(self, product_data):
        """Qalamcha bosilganda ma'lumotni yuklab oynani ochadi"""
        # 1. Tahrirlash moduliga ID va ma'lumotni beramiz
        self.template_edit_mod.editing_product_id = product_data.get("id")
        self.template_edit_mod.load_template_data(product_data)
        
        # 2. Sahifaga o'tamiz
        self.route("/open_template_editor")

    def route(self, path):
        """Barcha sahifalarga yo'naltirish mantiqi"""
        print(f"Router: {path} yo'nalishi ochilmoqda...")

        if path == "/products_menu":
            # Asosiy stackni page_products sahifasiga o'tkazamiz
            self.stacked_main.setCurrentWidget(self.ui.page_products)
            
            # Ichki stackni ro'yxat sahifasiga (page_template) o'tkazamiz
            self.settings_stack.setCurrentWidget(self.ui.page_template)
            
            # Sidebar panelini almashtiramiz
            if hasattr(self.ui, 'page_products_monitor_cheking'):
                self.sidebar_stack.setCurrentWidget(self.ui.page_products_monitor_cheking)
            
            self.template_mod.refresh_data()

        # 2. TAHRIRLASH/QO'SHISH OYNASI
        elif path == "/open_template_editor":
            # Avval page_products ochiqligini ta'minlaymiz
            self.stacked_main.setCurrentWidget(self.ui.page_products)
            
            # Ichki stackda tahrirlash sahifasini ochamiz
            if hasattr(self.ui, 'page_templat_editor'):
                self.settings_stack.setCurrentWidget(self.ui.page_templat_editor)
                print("Router: Ichki tahrirlash formasi aktivlashtirildi.")

        elif path == "/barcode":
            self.stacked_main.setCurrentWidget(self.ui.page_barcode)
            if hasattr(self.ui, 'page_barcode_scanner_Sozlamalar'):
                self.sidebar_stack.setCurrentWidget(self.ui.page_barcode_scanner_Sozlamalar)

        # 4. MONITOR
        elif path == "/monitor":
            self.stacked_main.setCurrentWidget(self.monitor_page)
            
        # 5. CHECKING
        elif path == "/checking":
            self.stacked_main.setCurrentWidget(self.checking_page)

    def show_monitor(self):
        self.route("/monitor")

    def show_checking(self):
        self.route("/checking")