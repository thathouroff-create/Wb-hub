import requests
import json
import os
import time

# Категории: Электроника, Дом, Одежда
SEARCH_QUERIES = ["смартфон", "пылесос", "кроссовки"]

def get_deals():
    all_deals = []
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36',
        'Accept': '*/*',
        'Host': 'search.wb.ru'
    }
    
    for query in SEARCH_QUERIES:
        # dest=-1257786 — это Москва. Это важно для отображения цен и наличия.
        url = f"https://search.wb.ru/exactmatch/ru/common/v4/search?appType=1&curr=rub&dest=-1257786&query={query}&resultset=catalog"
        
        try:
            res = requests.get(url, headers=headers, timeout=15)
            if res.status_code != 200: continue
            
            data = res.json()
            products = data.get('data', {}).get('products', [])
            
            print(f"По запросу '{query}' получено {len(products)} товаров")
            
            # Берем первые 5 товаров для проверки связи
            for p in products[:5]:
                all_deals.append({
                    "id": p['id'],
                    "name": p['name'],
                    "brand": p['brand'],
                    "price": p.get('salePriceU', 0) / 100,
                    "old_price": p.get('priceU', 0) / 100,
                    "discount": p.get('sale', 0),
                    "rating": p.get('rating', 0) / 10,
                    "reviews": p.get('feedbacks', 0)
                })
            time.sleep(2)
        except Exception as e:
            print(f"Ошибка {query}: {e}")
            
    return all_deals

if __name__ == "__main__":
    deals = get_deals()
    print(f"Итого в файл: {len(deals)} шт.")
    
    os.makedirs('data', exist_ok=True)
    with open('data/deals.json', 'w', encoding='utf-8') as f:
        json.dump(deals, f, indent=2, ensure_ascii=False)
