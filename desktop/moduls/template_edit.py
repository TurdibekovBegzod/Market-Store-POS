from PyQt6.QtWidgets import QHBoxLayout, QLabel, QLineEdit, QPushButton, QDialog, QVBoxLayout,QFileDialog,QMessageBox
from PyQt6 import uic
from services.add_field import save_template_to_db
from services.add_field import save_template_to_db
from PyQt6.QtCore import QTimer
import os
from PyQt6.QtWidgets import QMessageBox,QFileDialog
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt, QTimer,pyqtSignal,QObject
from services.template import delete_template_from_db


CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
UI_PATH = os.path.join(os.path.dirname(CURRENT_DIR),  "field_add.ui")
class AttributeAddDialog(QDialog):
    def __init__(self):
        super().__init__()
        if not os.path.exists(UI_PATH):
            alt_path = os.path.join(CURRENT_DIR, "field_add.ui")
            path_to_load = alt_path if os.path.exists(alt_path) else UI_PATH
        else:
            path_to_load = UI_PATH
            
        try:
            uic.loadUi(path_to_load, self)
        except Exception as e:
            print(f"UI yuklashda xatolik: {path_to_load} topilmadi!")
            raise e        

class TemplateEditModule(QObject):
    template_saved_signal = pyqtSignal()
    def __init__(self, ui):
        super().__init__()
        self.ui = ui
        self.editing_product_id = None
        self.selected_image_path=None
        self.setup_connections()
        if hasattr(self.ui, 'btn_select_photo'): # Designer-dagi tugma nomi
            self.ui.btn_select_photo.clicked.connect(self.select_image)
        
        if hasattr(self.ui, 'template_edit_save'):
            self.ui.template_edit_save.clicked.connect(self.save_all_data) 

        self.ui.template_edit_save.setEnabled(False)
        self.ui.template_edit_save.setStyleSheet("background-color: #cccccc; color: #666666; border-radius: 5px;")
        
        self.ui.label_9.hide()

    def setup_connections(self):
        # 1. Matn o'zgarganda Save tugmasini yoqish (Nomlar rasmga mos)
        self.ui.input_name.textChanged.connect(self.enable_save_button)
        self.ui.input_description.textChanged.connect(self.enable_save_button)
        
        # 2. Tugmalar ulanishi
        # "add feild" tugmasi
        self.ui.template_edit_add_field.clicked.connect(self.open_add_dialog)
        
        # "save" tugmasi
        self.ui.template_edit_save.clicked.connect(self.save_all_data)
        
        # "Orqaga" tugmasi
        self.ui.template_edit_orqaga.clicked.connect(self.go_back_and_refresh)
        
        # 3. Rasmni tanlash (Rasmda nomi: image_button)
        if hasattr(self.ui, 'image_button'):
            self.ui.image_button.clicked.connect(self.select_image)
        
        # 4. O'chirish tugmasi (Rasmda nomi: delete_2)
        if hasattr(self.ui, 'delete_2'):
            try:
                # Takroriy ulanishlarni oldini olish uchun
                self.ui.delete_2.clicked.disconnect()
            except:
                pass
            self.ui.delete_2.clicked.connect(self.delete_current_template)
        else:
            print("XATO: delete_2 tugmasi UI ichida topilmadi!")
    
    def clear_fields(self):
        """Formani to'liq tozalash"""
        print("DEBUG: Tozalash boshlandi...")
        
        # 1. Tanlangan rasm yo'lini o'chirish
        self.selected_image_path = None
        
        # 2. Nomini tozalash (Rasmda: input_name)
        if hasattr(self.ui, 'input_name'):
            self.ui.input_name.setText("") 
            
        # 3. Tavsifni tozalash (Rasmda: input_description)
        # BU YERDA: self.ui.setPlainText emas, self.ui.input_description.setPlainText bo'ladi
        if hasattr(self.ui, 'input_description'):
            self.ui.input_description.setPlainText("") 
            
        # 4. Rasmni tozalash (Rasmda nomi image_button yoki image_label bo'lishi mumkin)
        # Skrinshotda ko'ringan label nomini yozing (masalan: image_label)
        if hasattr(self.ui, 'image_label'):
            self.ui.image_label.clear() 
            self.ui.image_label.setText("Rasm tanlanmagan")
            self.ui.image_label.setStyleSheet("border: 2px dashed #ccc; color: #888; background: #f0f0f0;")

        # 5. Atributlar (Agar ichki o'zgaruvchi bo'lsa)
        if hasattr(self, 'attributes_list'):
            self.attributes_list = []
            
        # 6. Layoutni tozalash (Rasmda: frame_add_adributs ichidagi layout)
        if hasattr(self.ui, 'frame_add_adributs'):
            layout = self.ui.frame_add_adributs.layout()
            if layout is not None:
                self.clear_layout(layout)
        # Tugmani o'chirib qo'yish va xira rang berish
        self.ui.template_edit_save.setEnabled(False)
        self.ui.template_edit_save.setStyleSheet("""
            QPushButton {
                background-color: #e0e0e0; 
                color: #aaaaaa; 
                border: 1px solid #d0d0d0;
                border-radius: 5px;
                font-weight: bold;
            }
        """)     
        if hasattr(self.ui, 'template_edit_save'):
            self.ui.template_edit_save.setEnabled(False)
            self.ui.template_edit_save.setStyleSheet("""
                QPushButton {
                    background-color: #e0e0e0; 
                    color: #aaaaaa; 
                    border-radius: 5px;
                    font-weight: bold;
                    border: 1px solid #d0d0d0;
                }
            """)   

        print("DEBUG: Hamma maydonlar tozalandi.")

    def clear_layout(self, layout):
        """Layout ichini butunlay bo'shatish"""
        if layout is None:
            return
            
        while layout.count():
            item = layout.takeAt(0)
            widget = item.widget()
            if widget is not None:
                widget.setParent(None) # Avval ota vidjetdan ajratamiz
                widget.deleteLater()   # Keyin o'chirishga yuboramiz
            elif item.layout() is not None:
                self.clear_layout(item.layout())
                
    def enable_save_button(self):
        """O'zgarish bo'lganda Save tugmasini yoqish va rangini o'zgartirish"""
        # 1. input_name ni emas, TUGMANI (template_edit_save) aktivlashtirish kerak
        if hasattr(self.ui, 'template_edit_save'):
        # Tugmani yoqish
            self.ui.template_edit_save.setEnabled(True)
            
            # To'q yashil va hover effektli dizayn
            self.ui.template_edit_save.setStyleSheet("""
                QPushButton {
                    background-color: #2e7d32;  
                    color: white; 
                    border-radius: 5px;
                    font-weight: bold;
                    border: none;
                    padding: 5px;
                }
                QPushButton:hover {
                    background-color: #1b5e20; 
                }
                QPushButton:pressed {
                    background-color: #144317;  
                }
            """)

    def select_image(self):
        file_path, _ = QFileDialog.getOpenFileName(self.ui, "Rasm tanlang", "", "Images (*.png *.jpg *.jpeg)")
        if file_path:
            self.selected_image_path = file_path
            pixmap = QPixmap(file_path)
            if hasattr(self.ui, 'image_label'):
                self.ui.image_label.setPixmap(pixmap.scaled(
                    self.ui.image_label.width(), self.ui.image_label.height(),
                    Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation
                ))
                self.ui.image_label.setText("")

    def save_all_data(self):
        """Ma'lumotni serverga yuborish"""
        # template_name_input -> input_name ga almashdi
        name = self.ui.input_name.text() if hasattr(self.ui, 'input_name') else ""
        
        # input_description o'z holicha qoldi (chunki rasmda ham shunday)
        desc = self.ui.input_description.toPlainText() if hasattr(self.ui, 'input_description') else ""
        
        attrs = []
        success = save_template_to_db({"name": name, "description": desc}, [], self.selected_image_path)
        
        if success:
            print("Muvaffaqiyatli saqlandi!")
            self.template_saved_signal.emit() # Ro'yxatni yangilashni so'raymiz
        else:
            print("Serverga saqlashda xato yuz berdi!")


    def open_add_dialog(self):
        """Kichkina dialog oynasini ochish"""
        self.dialog = AttributeAddDialog()
        self.dialog.btn_add_confirm.clicked.connect(self.confirm_and_add_row)
        self.dialog.exec()

    def confirm_and_add_row(self):
        """Dialogdan nomni olib asosiy UI ga qator qo'shish"""
        attr_name = self.dialog.line_edit_attr_name.text().strip()
        
        if attr_name:
            self.add_new_attribute_row(attr_name)
            self.dialog.accept() # Dialogni yopish
 
        self.enable_save_button()
    def add_new_attribute_row(self, label_text):
        """Faqat nom ko'rinadigan qator qo'shish"""
        row_layout = QHBoxLayout()
        row_layout.setSpacing(5) # Label va Tugma orasidagi masofa (5 piksel)
        row_layout.setContentsMargins(0, 0, 0, 0)
        
        lbl = QLabel(f"{label_text}") # Faqat nom
        lbl.setStyleSheet("font-weight: bold; color: #1a237e; background: #e8eaf6; padding: 5px; border-radius: 3px;")
        
        # O'chirish tugmasi
        del_btn = QPushButton("✕")
        del_btn.setFixedSize(25,25)
        del_btn.setStyleSheet("background-color: #ff5252; color: white; border-radius: 12px; border: none;")
        del_btn.clicked.connect(lambda: self.remove_row(row_layout))

        row_layout.addWidget(lbl)
        # row_layout.addStretch() # Bo'sh joy qo'shib, o'chirish tugmasini o'ngga suradi
        row_layout.addWidget(del_btn)
        row_layout.addStretch()

        if self.ui.frame_add_adributs.layout() is None:
            self.ui.frame_add_adributs.setLayout(QVBoxLayout())
        
        self.ui.frame_add_adributs.layout().addLayout(row_layout)
    def remove_row(self, layout):
        """Qatorni o'chirish"""
        for i in reversed(range(layout.count())): 
            widget = layout.itemAt(i).widget()
            if widget:
                widget.deleteLater()
        layout.deleteLater()

    def refresh_data(self):
        """Katalog sahifasini ID bo'yicha tartiblab yangilash"""
        print("DEBUG: Sahifa tartib bilan yangilanmoqda...")
        
        # 1. Mavjud kartochkalarni o'chirish (Layoutni tozalash)
        if hasattr(self.ui, 'gridLayout_templates'):
            layout = self.ui.gridLayout_templates
            while layout.count():
                child = layout.takeAt(0)
                if child.widget():
                    child.widget().deleteLater()
        
        # 2. Serverdan yangi ma'lumotlarni olish
        try:
            from services.template import get_all_templates
            templates = get_all_templates()
            
            if not templates:
                print("DEBUG: Ma'lumot topilmadi.")
                return

            # ---------------------------------------------------------
            # 3. MUHIM: Ma'lumotlarni ID bo'yicha tartiblaymiz
            # Bu qator kartochkalarni har doim o'z o'rnida turishini ta'minlaydi
            templates.sort(key=lambda x: x.get('id', 0))
            # ---------------------------------------------------------

            # 4. Tartiblangan ro'yxat bo'yicha kartochkalarni chizish
            for template in templates:
                self.add_template_card(template)
                
            print(f"DEBUG: {len(templates)} ta kartochka o'z o'rnida chizildi.")
                
        except Exception as e:
            print(f"DEBUG: refresh_data ichida xatolik: {e}")


    def show_temp_message(self, text, color="black"):
        """Xabarni chiqarish va 3 soniyadan keyin o'chirish"""
        if hasattr(self.ui, 'label_9'):
            self.ui.label_9.setText(text)
            self.ui.label_9.setStyleSheet(f"color: {color}; font-weight: bold;")
            self.ui.label_9.show()

    def show_temp_message(self, text, color="black"):
        """Xabarni chiqarish va 3 soniyadan keyin o'chirish"""
        if hasattr(self.ui, 'label_9'):
            self.ui.label_9.setText(text)
            self.ui.label_9.setStyleSheet(f"color: {color}; font-weight: bold;")
            self.ui.label_9.show()
    def save_all_data(self):
        """Ma'lumotlarni yig'ish va bazaga string formatida saqlash"""
        try:
            from services.template import update_product, save_template_to_db
        except ImportError:
            print("Xato: services.template fayli topilmadi!")
            return

        # 1. Ma'lumotlarni yig'ish va majburiy stringga o'tkazish
        name = str(self.ui.input_name.text().strip())
        description = str(self.ui.input_description.toPlainText().strip() or "")
        
        # Atributlarni yig'ish (get_all_attributes funksiyangizdan kelgan listni string listga aylantiramiz)
        raw_attrs = self.get_all_attributes() if hasattr(self, 'get_all_attributes') else []
        attributes = [str(a) for a in raw_attrs] if isinstance(raw_attrs, list) else []
        
        # Validatsiya
        if not name:
            self.show_temp_message("Nomini kiritish majburiy!", "red")
            return

        # 2. Payloadni shakllantirish
        # DIQQAT: Backend 422 bermasligi uchun attributes listini saqlab qolamiz, 
        # chunki services/_send_request uni o'zi to'g'ri formatlaydi.
        data_content = {
            "name": name,
            "description": description
        }

        # 3. Saqlash jarayoni
        try:
            # Tugmani bloklaymiz va stilini o'zgartiramiz (Hira kulrang)
            self.ui.template_edit_save.setEnabled(False)
            self.ui.template_edit_save.setStyleSheet("background-color: #e0e0e0; color: #aaaaaa; border-radius: 5px;")
            
            success = False
            current_id = getattr(self, 'editing_product_id', None)
            image_path = getattr(self, 'selected_image_path', None)

            if current_id:
                print(f"DEBUG: {current_id} IDli mahsulot yangilanmoqda...")
                # update_product(id, data, attributes, image_path)
                success = update_product(current_id, data_content, attributes, image_path)
            else:
                print("DEBUG: Yangi shablon yaratilmoqda...")
                # save_template_to_db(data, attributes, image_path)
                success = save_template_to_db(data_content, attributes, image_path)

            if success:
                self.show_temp_message("Muvaffaqiyatli saqlandi!", "green")
                
                # Agar signal bo'lsa, ro'yxatni yangilash
                if hasattr(self, 'template_saved_signal'):
                    self.template_saved_signal.emit()
                
                # 1.2 soniyadan keyin menyuga qaytish
                from PyQt6.QtCore import QTimer
                QTimer.singleShot(1200, lambda: self.router.route("/products_menu"))
            else:
                # Xato bo'lsa tugmani qayta yoqamiz va yashil qilamiz
                self.show_temp_message("Xato: Server qabul qilmadi!", "red")
                self.enable_save_button() # Biz boya yozgan funksiya

        except Exception as e:
            print(f"Kritik xato: {e}")
            self.show_temp_message(f"Xatolik: {str(e)}", "red")
            self.enable_save_button()
    def show_temp_message(self, text, color="black"):
        """Xabarni chiqarish va 3 soniyadan keyin o'chirish"""
        if hasattr(self.ui, 'label_9'):
            self.ui.label_9.setText(text)
            self.ui.label_9.setStyleSheet(f"color: {color}; font-weight: bold;")
            self.ui.label_9.show()
            
            QTimer.singleShot(3000, self.ui.label_9.hide)
        
    def show_temp_message(self, text, color="black"):
        """Label_9 da xabarni chiqarib, 3 soniyadan keyin yashiradi"""
        if hasattr(self.ui, 'label_9'):
            self.ui.label_9.setText(text)
            self.ui.label_9.setStyleSheet(f"color: {color}; font-weight: bold; background: transparent;")
            self.ui.label_9.show()
            
            # 3 soniyadan keyin yashirish
            QTimer.singleShot(3000, self.ui.label_9.hide)

    
    def get_all_attributes(self):
            """Barcha dinamik qo'shilgan atributlarni LIST ko'rinishida yig'ish"""
            attributes_list = [] # List yaratamiz
            layout = self.ui.frame_add_adributs.layout()
            if layout:
                for i in range(layout.count()):
                    row = layout.itemAt(i).layout()
                    if row:
                        # 0-element Label (atribut nomi), undan matnni olamiz
                        name = row.itemAt(0).widget().text().replace(":", "").strip()
                        if name:
                            attributes_list.append(name) # Faqat nomini Listga qo'shamiz
            return attributes_list # NATIJA: ["adad", "rangi"]
        
        # products_template.py ichida
    def open_add_view(self):
        """Yashil '+' tugmasi uchun"""
        # 1. Tahrirlash oynasidagi ma'lumotlarni tozalaymiz (inputlarni bo'shatamiz)
        # Bu yerda aynan o'sha input vidjetlariga murojaat qiling
        self.ui.template_name_input.clear()          # Mahsulot nomi inputini bo'shatish
        self.ui.template_edit_info_input.clear()   # Tavsif inputini bo'shatish
        self.ui.label_image.setText("Rasm tanlanmagan") # Rasmni placeholderga qaytarish
        
        self.editing_product_id = None 
        self.selected_image_path = None

        # 3. Keyin sahifaga o'tamiz
        self.ui.router.route("/open_template_editor")

    def clear_form(self):
        """Oynadagi barcha maydonlarni yangi mahsulot uchun tozalash"""
        # Matnli maydonlarni tozalash
        self.ui.template_name_input.clear()
        self.ui.input_description.clear()
        
        # Rasmni tozalash (Placeholder qo'yish)
        self.ui.label_image.setText("Rasm tanlanmagan")
        self.ui.label_image.setStyleSheet("border: 2px dashed #ccc; color: #888;")
        
        # O'zgaruvchilarni nolga tushirish
        self.editing_product_id = None  
        self.selected_image_path = None
        
        # Agar atributlar ro'yxati bo'lsa:
        if hasattr(self.ui, 'list_attributes'):
            self.ui.list_attributes.clear()

        print("DEBUG: Editor oynasi yangi mahsulot uchun tozalandi.")

    def open_edit_view(self, product_data):
        print(f"ROUTER: Qalamcha bosildi. ID: {product_data.get('id')}") 
        
        self.template_edit_mod.editing_product_id = product_data.get("id")
         
        # 2. Ma'lumotlarni inputlarga yuklaymiz
        self.template_edit_mod.load_template_data(product_data)
        
        # 3. Sahifani ochamiz
        self.route("/open_template_editor")




    def go_back_and_refresh(self):
            """Orqaga tugmasi bosilganda ma'lumotlarni yangilab qaytish"""
            print("Orqaga qaytish va kartalarni yangilash boshlandi...")
            
            # 1. Avval routerni mahsulotlar menyusiga yo'naltiramiz
            if hasattr(self.ui, 'router'):
                self.ui.router.route("/products_menu")
            
            # Routerda template_mod qaysi nomda ekanligini tekshiring
            router = getattr(self.ui, 'router', None)
            if router:
                # Agar routerda template_mod bo'lsa
                template_mod = getattr(router, 'template_mod', None)
                if template_mod and hasattr(template_mod, 'refresh_data'):
                    template_mod.refresh_data()
                else:
                    print("Xato: template_mod yoki refresh_data topilmadi")

    def load_template_data(self, data):
        """Tahrirlashga kirganda inputlarni to'ldirish"""
        self.clear_fields()
        
        self.editing_product_id = data.get("id")
        self.ui.input_name.setText(str(data.get("name", "")))
        self.ui.input_description.setPlainText(str(data.get("description", "")))
        
        attrs = data.get("attributes", [])
        if isinstance(attrs, list):
            for attr in attrs:
                self.add_new_attribute_row(attr)
        
        # Tugma matnini o'zgartirish
        self.ui.template_edit_save.setEnabled(False)
        self.ui.template_edit_save.setText("Save")


    def delete_current_template(self):
            """Hozirgi shablonni o'chirish"""
            print(f"DEBUG: O'chirish boshlandi. ID: {self.editing_product_id}")
            
            if not self.editing_product_id:
                print("Xato: ID topilmadi")
                return

            if delete_template_from_db(self.editing_product_id):
                print("Muvaffaqiyatli o'chirildi")
                self.template_saved_signal.emit() # Main.py dagi refreshni ishlatadi
                if hasattr(self.ui, 'router'):
                    self.ui.router.route("/products_menu")
            else:
                print("Server o'chirishni rad etdi")