from PyQt6.QtWidgets import QHBoxLayout, QLabel, QLineEdit
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Optional
from services.product import update_product, create_product

class ProductRouter:
    def __init__(self, ui):
        self.ui = ui
        self.dynamic_widgets = {}
        self.editing_product_id = None
        self.setup_signals()

    def setup_signals(self):
        self.ui.combo_select_template.currentIndexChanged.connect(self.generate_fields)
        self.ui.btn_save_product.clicked.connect(self.save_product)

    def activate(self):
        self.ui.sidebar_stack.setCurrentIndex(1)
        self.ui.stacked_ong.setCurrentIndex(1)
        self.ui.settings_content_stack.setCurrentIndex(1)

    def switch_tab(self, index):
        self.ui.settings_content_stack.setCurrentIndex(index)

    def generate_fields(self):
        pass

    def save_product(self):
        """ Saqlash tugmasi bosilganda (Ham Yangi qo'shish, ham Tahrirlash uchun) """
        import requests # Yoki fayl tepasiga yozing
        
        name = self.ui.line_product_name.text()
        price = self.ui.line_product_price.text()
        info = self.ui.text_product_info.toPlainText() # Info qismini ham olamiz
        
        # Ma'lumotlar paketi
        payload = {
            "name": name,
            "price": float(price) if price else 0.0,
            "info": info
        }

        try:
            if self.editing_product_id:
                # TAHRIRLASH (PUT so'rovi)
                url = f"http://localhost:8000/products/{self.editing_product_id}"
                response = requests.put(url, json=payload)
                if response.status_code == 200:
                    print("Muvaffaqiyatli tahrirlandi")
            else:
                # YANGI QO'SHISH (POST so'rovi)
                url = "http://localhost:8000/products/"
                response = requests.post(url, json=payload)
                if response.status_code == 200:
                    print("Yangi mahsulot qo'shildi")

            # Amaliyot tugagach, formani tozalaymiz
            self.clear_fields()
            
        except Exception as e:
            print(f"Xatolik yuz berdi: {e}")

    def clear_fields(self):
        """ Maydonlarni tozalash va rejimni qayta tiklash """
        self.editing_product_id = None
        self.ui.line_product_name.clear()
        self.ui.line_product_price.clear()
        self.ui.text_product_info.clear()
        self.ui.btn_save_product.setText("Saqlash")

    def edit_product(self, product_data):
        """ Qalamcha bosilganda shu funksiya chaqiriladi """
        self.editing_product_id = product_data['id'] # ID ni saqlab qolamiz
        self.activate() # Tabni ochamiz
        
        # Maydonlarni mavjud ma'lumotlar bilan to'ldiramiz
        # Eslatma: ui elementlari nomlarini o'zingiznikiga moslang
        self.ui.line_product_name.setText(product_data['name'])
        self.ui.line_product_price.setText(str(product_data['price']))
        self.ui.text_product_info.setPlainText(product_data.get('info', ''))
        
        # Tugma matnini o'zgartirish (ixtiyoriy, foydalanuvchiga tushunarli bo'lishi uchun)
        self.ui.btn_save_product.setText("O'zgarishlarni saqlash")

    def save_product(self):
        """ Saqlash tugmasi bosilganda: Tahrirlash yoki Yangi qo'shish """
        
        # 1. Ma'lumotlarni yig'ish
        name = self.ui.line_product_name.text()
        price = self.ui.line_product_price.text()
        info = self.ui.text_product_info.toPlainText()
        
        payload = {
            "name": name,
            "price": float(price) if price else 0.0,
            "info": info
        }

        # 2. Rejimni tekshirish va Serverga yuborish
        if self.editing_product_id:
            # TAHRIRLASH REJIMI
            success = update_product(self.editing_product_id, payload)
            if success:
                print("Muvaffaqiyatli tahrirlandi")
            else:
                print("Tahrirlashda xatolik yuz berdi")
        else:
            # YANGI QO'SHISH REJIMI
            success = create_product(payload)
            if success:
                print("Yangi mahsulot muvaffaqiyatli qo'shildi")
            else:
                print("Qo'shishda xatolik yuz berdi")

        # 3. Agar ish muvaffaqiyatli bo'lsa, formani tozalash
        if success:
            self.reset_ui()

    def reset_ui(self):
        """ UI elementlarini va rejimni boshlang'ich holatga qaytarish """
        self.editing_product_id = None
        self.ui.line_product_name.clear()
        self.ui.line_product_price.clear()
        self.ui.text_product_info.clear()
        self.ui.btn_save_product.setText("Saqlash")