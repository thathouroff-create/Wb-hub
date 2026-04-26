import requests
import json
import os

# Эта строка ДОЛЖНА появиться в логах первой
print(">>> СТАРТ: Скрипт запущен и начал работу")

def get_hh_data():
    print(">>> Иду на HH.ru...")
    queries = ["DevOps", "Python developer", "Системный администратор"]
    all_stats = []
    
    for q in queries:
        url = f"https://api.hh.ru/vacancies?text={q}&area=1&per_page=10"
        try:
            res = requests.get(url, headers={'User-Agent': 'HH-User-Agent'}, timeout=15)
            if res.status_code == 200:
                data = res.json()
                found = data.get('found', 0)
                print(f">>> Нашел {found} вакансий для: {q}")
                all_stats.append({
                    "name": q,
                    "count": found,
                    "price": 180000, # Ставим среднюю заглушку для теста
                    "brand": "HH.ru"
                })
        except Exception as e:
            print(f">>> ОШИБКА на запросе {q}: {e}")
    return all_stats

# ВОТ ЭТОТ БЛОК — ЭТО «КЛЮЧ В ЗАЖИГАНИИ»
if __name__ == "__main__":
    results = get_hh_data()
    print(f">>> ИТОГО: Собрано {len(results)} записей")
    
    os.makedirs('data', exist_ok=True)
    with open('data/deals.json', 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    print(">>> ФАЙЛ deals.json ОБНОВЛЕН. Скрипт завершен успешно.")
