class MonitorRouter:
    def __init__(self, ui):
        self.ui = ui

    def activate(self):
        self.ui.sidebar_stack.setCurrentIndex(1)        # Chap menyu 2-qavat
        self.ui.stacked_ong.setCurrentIndex(1)          # O'ng oyna page_6
        self.ui.settings_content_stack.setCurrentIndex(2) 