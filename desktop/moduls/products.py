class ProductsModule:
    def __init__(self, ui):
        self.ui = ui

    def open_page(self):
        
        if hasattr(self.ui, 'stacked_ong'):
            # page_products yuqori tugmalar bor sahifa ochiladi
            self.ui.stacked_ong.setCurrentIndex(1)
        

    def show_template_content(self):
        if hasattr(self.ui, 'settings_content_stack'):
            self.ui.settings_content_stack.setCurrentIndex(0)
            
    def show_product_content(self):
        if hasattr(self.ui, 'settings_content_stack'):
            self.ui.settings_content_stack.setCurrentIndex(1)

    def open_edit_view(self):
        # Bu yerda routerni chaqiramiz (agar main.py dagi router bu klassga uzatilgan bo'lsa)
        if hasattr(self.ui, 'router'):
            self.ui.router.route("/open_template_editor")        