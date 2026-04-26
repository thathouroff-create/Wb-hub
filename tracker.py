import requests
import json
import os

def get_hh_data():
    queries = ["DevOps", "Python developer", "Системный администратор"]
    all_stats = []
    
    for q in queries:
        # API HH: поиск вакансий по Москве (area=1)
        url = f"https://api.hh.ru/vacancies?text={q}&area=1&per_page=50"
        try:
            res = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'}, timeout=15)
            if res.status_code == 200:
                data = res.json()
                found = data.get('found', 0)
                items = data.get('items', [])
                
                # Считаем среднюю вилку зарплат "от"
                salaries = [i['salary']['from'] for i in items if i.get('salary') and i['salary'].get('from')]
                avg_sal = int(sum(salaries) / len(salaries)) if salaries else 0
                
                all_stats.append({
                    "name": q,
                    "count": found,
                    "price": avg_sal, # Используем поле price для совместимости с index.html
                    "brand": "HH.ru",
                    "discount": 0 # Для HH это не актуально, но поле оставим
                })
        except Exception as e:
            print(f"Ошибка HH на {q}: {e}")
    return all_stats

if __name__ == "__main__":
    data = get_hh_data()
    os.makedirs('data', exist_ok=True)
    with open('data/deals.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
