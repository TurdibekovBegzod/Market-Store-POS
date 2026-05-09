class SozlamalarModule:
    def __init__(self, ui):
        self.ui = ui

    def set_product_active(self):
        if hasattr(self.ui, 'settings_content_stack'):
            self.ui.settings_content_stack.setCurrentIndex(0) 
