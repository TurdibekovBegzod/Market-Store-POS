import requests

BASE_URL = "http://127.0.0.1:8000/products"

def get_all_products():
    try:
        response = requests.get(f"{BASE_URL}/")
        return response.json() if response.status_code == 200 else []
    except:
        return []

def create_product(data):
    try:
        response = requests.post(f"{BASE_URL}/", json=data)
        return response.status_code in [200, 201]
    except:
        return False

def update_product(product_id, data):
    """ Mavjud mahsulotni tahrirlash (Qalamcha) """
    try:
        response = requests.put(f"{BASE_URL}/{product_id}", json=data)
        return response.status_code == 200
    except:
        return False

def delete_product(product_uid):
    try:
        response = requests.delete(f"{BASE_URL}/{product_uid}")
        return response.status_code in [200, 204]
    except:
        return False
 