class ScannerRouter:
    def __init__(self, ui):
        self.ui = ui

    def activate(self):
        self.ui.stacked_ong.setCurrentIndex(0)
        
        if hasattr(self.ui, 'stackedWidget'):
            self.ui.stackedWidget.setCurrentIndex(1)
        