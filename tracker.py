import requests
import json
import os

# Настраиваем поиск по ключевым словам
# Можно добавлять любые фразы: "iphone", "инструменты для кожи", "кроссовки"
SEARCH_QUERIES = [
    {"query": "смартфон xiaomi", "min_rating": 45, "min_discount": 20},
    {"query": "набор инструментов", "min_rating": 45, "min_discount": 30},
    {"query": "кожа pueblo", "min_rating": 40, "min_discount": 10},
    {"query": "футболка мужская", "min_rating": 45, "min_discount": 50}
]

def get_deals():
    all_deals = []
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
    
    for item in SEARCH_QUERIES:
        query = item['query']
        # Универсальный API поиска WB
        url = f"https://search.wb.ru/exactmatch/ru/common/v4/search?appType=1&curr=rub&dest=-1257786&query={query}&resultset=catalog&sort=priceup"
        
        try:
            res = requests.get(url, headers=headers, timeout=15)
            data = res.json()
            products = data.get('data', {}).get('products', [])
            
            for p in products:
                # Фильтр по качеству и скидке
                if p.get('rating', 0) >= item['min_rating'] and p.get('sale', 0) >= item['min_discount']:
                    all_deals.append({
                        "id": p['id'],
                        "name": p['name'],
                        "brand": p['brand'],
                        "price": p['salePriceU'] / 100,
                        "old_price": p['priceU'] / 100,
                        "discount": p['sale'],
                        "rating": p['rating'] / 10,
                        "reviews": p['feedbacks'],
                        "query": query
                    })
        except Exception as e:
            print(f"Ошибка при поиске '{query}': {e}")
            
    return all_deals

if __name__ == "__main__":
    deals = get_deals()
    os.makedirs('data', exist_ok=True)
    with open('data/deals.json', 'w', encoding='utf-8') as f:
        json.dump(deals, f, indent=2, ensure_ascii=False)
    print(f"Найдено {len(deals)} товаров по вашим запросам.")
