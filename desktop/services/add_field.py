import requests

BASE_URL = "http://localhost:8000/product-templates/"

def save_template_to_db(data):
    """Yangi andozani serverga yuborish"""
    try:
        response = requests.post(f"{BASE_URL}", json=data, timeout=5)
        return response.status_code in[ 200.201]
    except Exception as e:
        print(f"API xatosi: {e}")
        return False
    
import requests

def save_product_template(data, image_path=None):
    url = "http://localhost:8000/product-templates/" # Server manzilingiz
    
    # 1. Matnli ma'lumotlarni tayyorlaymiz (JSON emas, oddiy lug'at)
    payload = {
        "name": data.get('name'),
        "description": data.get('description'),
        "attributes": data.get('attributes') # Agar server list kutsa, json.dumps kerak bo'lishi mumkin
    }
    
    files = []
    # 2. Agar rasm yo'li bo'lsa, uni fayl sifatida ochamiz
    if image_path:
        # 'image' kaliti serverdagi API kutayotgan nom bilan bir xil bo'lishi kerak
        files = [('image', (open(image_path, 'rb')))]
    
    try:
        # MUHIM: data=payload (json emas) va files=files
        response = requests.post(url, data=payload, files=files)
        
        if response.status_code in [200, 201]:
            print("Muvaffaqiyatli saqlandi!")
            return True
        else:
            print(f"Xato: {response.text}")
            return False
    except Exception as e:
        print(f"Ulanishda xato: {e}")
        return False
