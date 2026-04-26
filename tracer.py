import requests
import json
import os

# Настройки фильтров
CONFIG = [
    {"id": 600, "name": "Электроника", "min_rating": 45, "min_reviews": 200, "min_discount": 30},
    {"id": 258, "name": "Дом", "min_rating": 45, "min_reviews": 100, "min_discount": 50},
    {"id": 70, "name": "Одежда", "min_rating": 43, "min_reviews": 300, "min_discount": 70}
]

def get_deals():
    all_deals = []
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
    
    for cat in CONFIG:
        # API каталога WB с сортировкой по скидке
        url = f"https://catalog.wb.ru/catalog/repair10/v4/list?appType=1&cat={cat['id']}&curr=rub&dest=-1257786&sort=discount"
        try:
            res = requests.get(url, headers=headers, timeout=15)
            data = res.json()
            products = data.get('data', {}).get('products', [])
            
            for p in products:
                # Фильтруем по качеству
                if p.get('rating', 0) >= cat['min_rating'] and p.get('feedbacks', 0) >= cat['min_reviews']:
                    if p.get('sale', 0) >= cat['min_discount']:
                        all_deals.append({
                            "id": p['id'],
                            "name": p['name'],
                            "brand": p['brand'],
                            "price": p['salePriceU'] / 100,
                            "old_price": p['priceU'] / 100,
                            "discount": p['sale'],
                            "rating": p['rating'] / 10,
                            "reviews": p['feedbacks'],
                            "category": cat['name']
                        })
        except Exception as e:
            print(f"Ошибка в категории {cat['name']}: {e}")
            
    return all_deals

if __name__ == "__main__":
    deals = get_deals()
    os.makedirs('data', exist_ok=True)
    with open('data/deals.json', 'w', encoding='utf-8') as f:
        json.dump(deals, f, indent=2, ensure_ascii=False)
    print(f"Найдено {len(deals)} предложений.")
