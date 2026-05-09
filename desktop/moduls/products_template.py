import requests
from PyQt6.QtWidgets import QFrame, QVBoxLayout, QLabel, QPushButton, QHBoxLayout
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt
from services.template import get_all_templates 

class TemplateCard(QFrame):
    def __init__(self, data, router):
        super().__init__()
        self.data = data
        self.router = router
        self.setup_ui()

    def setup_ui(self):
        self.setFixedSize(240, 320) 
        layout = QVBoxLayout(self)
        
        header = QHBoxLayout()
        name = self.data.get('name', 'Nomsiz')
        self.name_label = QLabel(f"name: {name}")
        self.name_label.setStyleSheet("font-weight: bold; color: #1a237e; border: none;")
        
        self.edit_btn = QPushButton("✎")
        self.edit_btn.setFixedSize(30, 30)
        self.edit_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.edit_btn.clicked.connect(self.go_to_edit)
        
        header.addWidget(self.name_label)
        header.addStretch()
        header.addWidget(self.edit_btn)
        layout.addLayout(header)

        info = self.data.get('description', '')
        self.info_label = QLabel(f"info: {info}")
        self.info_label.setWordWrap(True)
        self.info_label.setStyleSheet("""
            background-color: #e3f2fd; 
            border-radius: 8px; 
            padding: 5px; 
            border: none;
            color: #0d47a1;
        """)
        layout.addWidget(self.info_label)

        # 3. Rasm

        
        self.image_label = QLabel()
        self.image_label.setFixedSize(220, 160) 
        self.image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.image_label.setStyleSheet("""
            background-color: white; 
            border: 1px solid #dcedc8; 
            border-radius: 8px;
            color: #757575; /* Default tekst rangi */
            font-size: 14px;
        """)
        
        image_url = self.data.get('image')
        pixmap = QPixmap()
        
        if image_url:
            try:
                if image_url.startswith('http'):
                    full_url = image_url
                else:
                    clean_path = image_url if image_url.startswith('/') else f"/{image_url}"
                    full_url = f"http://localhost:8000{clean_path}"

                print(f"DEBUG: Rasm yuklanmoqda: {full_url}")
                
                # Rasmni yuklab olamiz
                img_data = requests.get(full_url, timeout=5).content
                pixmap.loadFromData(img_data)
                
                if not pixmap.isNull():
                    self.image_label.setPixmap(pixmap.scaled(
                        220, 160, 
                        Qt.AspectRatioMode.KeepAspectRatio, 
                        Qt.TransformationMode.SmoothTransformation
                    ))
                else:
                    self.image_label.setText("Rasm formati xato")
                    
            except Exception as e:
                print(f"DEBUG ERROR: Rasm yuklashda xatolik: {e}")
                self.image_label.setText("Xatolik yuz berdi")
        else:
            print("DEBUG: Mahsulotda rasm yo'q.")
            self.image_label.setText("Rasm yo'q")
            
        layout.addWidget(self.image_label)

    def go_to_edit(self):
    # Routerga ma'lumotni (self.data) berib yuboramiz
        self.router.open_edit_view(self.data)

class AddTemplateCard(QFrame):
    def __init__(self, router):
        super().__init__()
        self.router = router
        self.setup_ui()

    def setup_ui(self):
        self.setFixedSize(240, 320)
        layout = QVBoxLayout(self)
        
        self.add_btn = QPushButton("+")
        self.add_btn.setFixedSize(100, 100)
        self.add_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        
        self.add_btn.setStyleSheet("""
            QPushButton {
                background-color: #4caf50;
                color: white;
                font-size: 60px;
                font-weight: bold;
                border-radius: 50px;
                border: none;
                
                                   
            }
            QPushButton:hover {
                background-color: #45a049;
            }
        """)
        
        self.add_btn.clicked.connect(self.router.open_add_view)
        
        layout.addStretch()
        layout.addWidget(self.add_btn, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addStretch()

        self.setStyleSheet("""
            QFrame {
                background-color: transparent;
                border: 2px dashed #4caf50;
                border-radius: 15px;
            }
        """)        

class ProductsTemplateModule:
    def __init__(self, ui):
        self.ui = ui

    def refresh_data(self):
        print("Bazadan ma'lumot olish boshlandi...")
        try:
            data = get_all_templates()
            
            if isinstance(data, dict):
                templates_list = data.get('templates', [])
                
                if templates_list:
                    print(f"Bazadan {len(templates_list)} ta ma'lumot topildi.")
                    self.load_templates(templates_list)
                else:
                    # Agar 'templates' bo'sh bo'lsa yoki topilmasa
                    print("Ma'lumotlar ro'yxati bo'sh yoki 'templates' kaliti topilmadi!")
                    self.load_templates([]) # Ekranni tozalash uchun
            
            elif isinstance(data, list):
                self.load_templates(data)
                
        except Exception as e:
            print(f"Refresh data xatosi: {e}")

    def load_templates(self, template_list):
        grid = self.ui.gridLayout_templates
        
        # 1. Gridni tozalash
        while grid.count():
            item = grid.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()

        count = 0
        for index, data in enumerate(template_list):
            card = TemplateCard(data, self.ui.router)
            grid.addWidget(card, index // 3, index % 3)
            count = index + 1

        add_card = AddTemplateCard(self.ui.router)
        grid.addWidget(add_card, count // 3, count % 3)
        
        print(f"Jami {count} ta andoza va 1 ta qo'shish tugmasi yuklandi.")

    def open_add_view(self):
        """Yashil '+' tugmasi bosilganda oynani tozalab ochish"""
        if hasattr(self, 'template_editor'):
            self.template_editor.clear_form() 
        
        self.ui.router.route("/open_template_editor")