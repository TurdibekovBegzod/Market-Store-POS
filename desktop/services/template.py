import requests
import os

BASE_URL = "http://localhost:8000/product-templates"

import requests
import os
import json

def _send_request(method, url, data, attributes, image_path=None):
    """
    Barcha requestlar uchun yagona umumiy funksiya.
    422 xatosini oldini olish uchun ma'lumotlarni to'g'ri formatlaydi.
    """
    opened_files = [] # Windowsda fayllarni yopish uchun ro'yxat
    
    try:
        # 1. Matnli oddiy maydonlar (Payload)
        # Barchasini majburiy stringga o'tkazamiz
        payload = {
            "name": str(data.get("name", "")),
            "description": str(data.get("description", ""))
        }
        
        # 2. Files va Murakkab maydonlar (Multipart/form-data)
        # FastAPI attributes: List[str] = Form(...) kutsa, har birini alohida qo'shish kerak
        multi_dict = []
        
        if isinstance(attributes, list) and len(attributes) > 0:
            for attr in attributes:
                # Har bir atributni alohida 'attributes' kaliti bilan qo'shamiz
                multi_dict.append(('attributes', (None, str(attr))))
        else:
            # Agar bo'sh bo'lsa, backend validatsiya xatosi (422) bermasligi uchun
            # Swagger/FastAPI modeliga qarab bo'sh string yuboramiz
            multi_dict.append(('attributes', (None, "")))

        # 3. Rasm tekshiruvi
        if image_path and os.path.exists(image_path):
            try:
                f = open(image_path, 'rb')
                opened_files.append(f)
                # 'image' nomi backenddagi UploadFile argumenti bilan bir xil bo'lishi shart
                file_name = os.path.basename(image_path)
                multi_dict.append(('image', (file_name, f, 'image/jpeg')))
            except Exception as img_err:
                print(f"DEBUG: Rasmni o'qishda xatolik: {img_err}")

        print(f"DEBUG: {method} so'rovi yuborilmoqda: {url}")

        # 4. So'rovni yuborish
        # data=payload (oddiy stringlar), files=multi_dict (list va rasm)
        response = requests.request(
            method=method, 
            url=url, 
            data=payload, 
            files=multi_dict, 
            timeout=15
        )
        
        if response.status_code in [200, 201, 204]:
            print(f"SUCCESS: {method} muvaffaqiyatli yakunlandi.")
            return True
        else:
            # Xatolik yuz bersa server qaytargan xabarni to'liq ko'ramiz
            print(f"XATO ({method}) [{response.status_code}]: {response.text}")
            return False
            
    except requests.exceptions.RequestException as e:
        print(f"TARMOQ XATOSI (Serverga ulanib bo'lmadi): {e}")
        return False
    except Exception as e:
        print(f"KUTILMAGAN XATO: {e}")
        return False
        
    finally:
        # Windowsda 'PermissionError' bermasligi uchun fayllarni albatta yopamiz
        for f in opened_files:
            try:
                f.close()
            except:
                pass

# --- ASOSIY FUNKSIYALAR ---

def get_all_templates():
    """Barcha shablonlarni olish"""
    try:
        response = requests.get(BASE_URL, timeout=10)
        return response.json() if response.status_code == 200 else []
    except:
        return []

def save_template_to_db(data, attributes, image_path=None):
    """Yangi shablon yaratish (POST)"""
    return _send_request("POST", f"{BASE_URL}/", data, attributes, image_path)

def update_product(template_id, data, attributes, image_path=None):
    """Mavjudini tahrirlash (PUT)"""
    url = f"{BASE_URL}/{template_id}"
    return _send_request("PUT", url, data, attributes, image_path)

def delete_template_from_db(template_id):
    """Shablonni o'chirish (DELETE)"""
    try:
        response = requests.delete(f"{BASE_URL}/{template_id}", timeout=10)
        return response.status_code in [200, 204]
    except Exception as e:
        print(f"O'chirishda xato: {e}")
        return False