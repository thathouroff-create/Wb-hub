import requests
import json
import os

# Используем прямые ID категорий для обхода блокировок поиска
# 600 - Электроника, 258 - Дом, 70 - Женщинам, 71 - Мужчинам
CATEGORIES = [
    {"id": 600, "name": "Электроника"},
    {"id": 258, "name": "Дом"},
    {"id": 70, "name": "Одежда"}
]

def get_deals():
    all_deals = []
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36',
        'Accept': '*/*',
        'Origin': 'https://www.wildberries.ru'
    }
    
    for cat in CATEGORIES:
        # Прямой URL каталога (он стабильнее поиска)
        url = f"https://catalog.wb.ru/catalog/repair10/v4/list?appType=1&cat={cat['id']}&curr=rub&dest=-1257786&sort=discount"
        
        try:
            print(f"Запрос категории: {cat['name']}...")
            res = requests.get(url, headers=headers, timeout=20)
            
            data = res.json()
            products = data.get('data', {}).get('products', [])
            
            print(f"Получено из WB: {len(products)} товаров")
            
            # Берем первые 10 товаров с лучшими скидками
            for p in products[:10]:
                all_deals.append({
                    "id": p['id'],
                    "name": p['name'],
                    "brand": p['brand'],
                    "price": p.get('salePriceU', 0) / 100,
                    "old_price": p.get('priceU', 0) / 100,
                    "discount": p.get('sale', 0),
                    "rating": p.get('rating', 0) / 10,
                    "reviews": p.get('feedbacks', 0),
                    "category": cat['name']
                })
        except Exception as e:
            print(f"Ошибка в {cat['name']}: {e}")
            
    return all_deals

if __name__ == "__main__":
    deals = get_deals()
    print(f"Итого отобрано: {len(deals)}")
    
    os.makedirs('data', exist_ok=True)
    with open('data/deals.json', 'w', encoding='utf-8') as f:
        json.dump(deals, f, indent=2, ensure_ascii=False)
