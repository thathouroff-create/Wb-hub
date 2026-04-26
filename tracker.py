import requests
import json
import os

print(">>> СТАРТ: Скрипт запущен")

def get_hh_data():
    # Темы, которые мы обсуждали
    queries = ["DevOps", "Python developer", "Системный администратор"]
    all_stats = []
    
    print(">>> Иду на HH.ru...")
    for q in queries:
        url = f"https://api.hh.ru/vacancies?text={q}&area=1&per_page=10"
        try:
            # Используем стандартный заголовок браузера
            headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
            res = requests.get(url, headers=headers, timeout=10)
            
            # Печатаем статус ответа, чтобы понять, что происходит
            print(f">>> Запрос '{q}', Статус: {res.status_code}")
            
            if res.status_code == 200:
                data = res.json()
                found = data.get('found', 0)
                all_stats.append({
                    "name": q,
                    "count": found,
                    "price": 150000, # Тестовая заглушка зарплаты
                    "brand": "HH.ru"
                })
        except Exception as e:
            print(f">>> ОШИБКА: {e}")
            
    # ФОЛБЭК: Если API нас забанил (0 записей), добавляем демо-данные
    if not all_stats:
        print(">>> API недоступен. Добавляю демо-данные, чтобы оживить сайт.")
        all_stats = [
            {"name": "API в блоке", "count": 0, "price": 0, "brand": "DEBUG"},
            {"name": "Тестовый DevOps", "count": 404, "price": 250000, "brand": "TEST"}
        ]
        
    return all_stats

if __name__ == "__main__":
    results = get_hh_data()
    # Создаем папку и сохраняем файл
    os.makedirs('data', exist_ok=True)
    with open('data/deals.json', 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    print(f">>> ИТОГО: Собрано {len(results)} записей. Файл обновлен.")
