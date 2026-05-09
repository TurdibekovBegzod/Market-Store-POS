class BarcodeModule:
    def __init__(self, ui):
        self.ui = ui
        self.setup_ui()

    def setup_ui(self):
        if hasattr(self.ui, 'btn_edit_sheet'):
            self.ui.btn_edit_sheet.clicked.connect(self.edit_google_id)
            
    def edit_google_id(self):
        print("Google Sheet ID tahrirlanmoqda...")