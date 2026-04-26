import requests
import json
import os

# Ослабляем фильтры для теста: ищем скидки от 10% и любой рейтинг
SEARCH_QUERIES = [
    {"query": "xiaomi", "min_rating": 0, "min_discount": 10},
    {"query": "кожа", "min_rating": 0, "min_discount": 5},
    {"query": "инструменты", "min_rating": 0, "min_discount": 10}
]

def get_deals():
    all_deals = []
    # Важно: используем заголовки, чтобы WB не принял нас за робота
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36',
        'Accept': '*/*',
        'Accept-Language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7'
    }
    
    for item in SEARCH_QUERIES:
        query = item['query']
        # Проверенный URL для поиска (без лишних параметров)
        url = f"https://search.wb.ru/exactmatch/ru/common/v4/search?appType=1&curr=rub&dest=-1257786&query={query}&resultset=catalog"
        
        try:
            res = requests.get(url, headers=headers, timeout=20)
            if res.status_code != 200:
                print(f"Ошибка API: {res.status_code} для запроса {query}")
                continue
                
            data = res.json()
            products = data.get('data', {}).get('products', [])
            print(f"Запрос '{query}': найдено {len(products)} товаров всего.")
            
            for p in products:
                rating = p.get('rating', 0)
                discount = p.get('sale', 0)
                
                # Если товар подходит под наши (теперь слабые) фильтры
                if rating >= item['min_rating'] and discount >= item['min_discount']:
                    all_deals.append({
                        "id": p['id'],
                        "name": p['name'],
                        "brand": p['brand'],
                        "price": p.get('salePriceU', 0) / 100,
                        "old_price": p.get('priceU', 0) / 100,
                        "discount": discount,
                        "rating": rating,
                        "reviews": p.get('feedbacks', 0)
                    })
        except Exception as e:
            print(f"Ошибка в скрипте: {e}")
            
    return all_deals

if __name__ == "__main__":
    deals = get_deals()
    print(f"Итого отобрано для сайта: {len(deals)} товаров.")
    
    os.makedirs('data', exist_ok=True)
    with open('data/deals.json', 'w', encoding='utf-8') as f:
        json.dump(deals, f, indent=2, ensure_ascii=False)
