class SettingsManager:
    def __init__(self, ui):
        self.ui = ui

    def activate(self):
        self.ui.sidebar_stack.setCurrentIndex(1) # Admin menyu
        self.ui.stacked_ong.setCurrentIndex(1)   # page_6