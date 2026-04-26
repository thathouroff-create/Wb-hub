import requests
import json
import os
import time

# Категории: Электроника, Дом, Одежда
SEARCH_QUERIES = ["смартфон", "наушники", "пылесос", "инструменты", "кроссовки", "худи"]

def get_deals():
    all_deals = []
    # Обновленный агент, чтобы не злить систему
    headers = {
        'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1',
        'Accept': '*/*',
        'Host': 'search.wb.ru'
    }
    
    for query in SEARCH_QUERIES:
        url = f"https://search.wb.ru/exactmatch/ru/common/v4/search?appType=1&curr=rub&dest=-1257786&query={query}&resultset=catalog&sort=discount"
        
        try:
            print(f"Сканирую категорию: {query}")
            res = requests.get(url, headers=headers, timeout=15)
            
            if res.status_code == 429:
                print(f"Лимит исчерпан для {query}. Ждем...")
                continue
                
            data = res.json()
            products = data.get('data', {}).get('products', [])
            
            # Фильтруем: рейтинг 4.5+ и скидка от 40%
            for p in products:
                if p.get('rating', 0) >= 45 and p.get('sale', 0) >= 40:
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
            
            time.sleep(3) # Пауза между запросами
            
        except Exception as e:
            print(f"Ошибка на {query}: {e}")
            
    return all_deals

if __name__ == "__main__":
    deals = get_deals()
    print(f"Успех! Найдено {len(deals)} отличных товаров.")
    
    os.makedirs('data', exist_ok=True)
    with open('data/deals.json', 'w', encoding='utf-8') as f:
        json.dump(deals, f, indent=2, ensure_ascii=False)
