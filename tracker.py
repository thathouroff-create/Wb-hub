import requests
import json
import os

def get_deals():
    all_deals = []
    # Используем публичный API для получения прокси, чтобы не светить свой IP
    proxy_url = "https://api.proxyscrape.com/v2/?request=displayproxies&protocol=http&timeout=10000&country=all&ssl=all&anonymity=all"
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36',
        'Accept': '*/*',
        'Referer': 'https://www.wildberries.ru/'
    }

    # Категории для теста (Электроника и Дом)
    cat_ids = [600, 258]
    
    for cid in cat_ids:
        url = f"https://catalog.wb.ru/catalog/repair10/v4/list?appType=1&cat={cid}&curr=rub&dest=-1257786&sort=discount"
        
        try:
            print(f"Пробую пробить категорию {cid}...")
            # Пытаемся сделать запрос напрямую
            res = requests.get(url, headers=headers, timeout=15)
            
            # Если получили пустой ответ (твоя ошибка), пробуем через прокси
            if not res.text or res.status_code != 200:
                print("Прямой запрос заблокирован. Ищу прокси...")
                # Тут могла бы быть логика с прокси, но для начала попробуем 
                # сменить домен на 'card.wb.ru', он иногда работает лучше
                url = url.replace("catalog.wb.ru", "card.wb.ru")
                res = requests.get(url, headers=headers, timeout=15)

            data = res.json()
            products = data.get('data', {}).get('products', [])
            
            for p in products[:10]:
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
            print(f"Нашел {len(products)} товаров.")
        except Exception as e:
            print(f"Ошибка на {cid}: {e}")
            
    return all_deals

if __name__ == "__main__":
    deals = get_deals()
    os.makedirs('data', exist_ok=True)
    with open('data/deals.json', 'w', encoding='utf-8') as f:
        json.dump(deals, f, indent=2, ensure_ascii=False)
    print(f"Итого сохранено: {len(deals)}")
