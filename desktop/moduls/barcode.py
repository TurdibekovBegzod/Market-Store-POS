class BarcodeRouter:
    def __init__(self, ui):
        self.ui = ui

    def activate(self):
        self.ui.sidebar_stack.setCurrentIndex(0)
        self.ui.stacked_ong.setCurrentIndex(0)
        if hasattr(self.ui, 'stackedWidget'):
            self.ui.stackedWidget.setCurrentIndex(0)
        print("Barcode Router: activated")

    def activate(self):
        self.ui.sidebar_stack.setCurrentIndex(0) 
        self.ui.stacked_ong.setCurrentIndex(0) 
        if hasattr(self.ui, 'stackedWidget'):
            self.ui.stackedWidget.setCurrentIndex(0)        