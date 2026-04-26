import requests
import json
import os

def get_hh_stats():
    # Ищем вакансии для системных инженеров и разработчиков
    queries = ["DevOps", "Python developer", "Системный администратор"]
    results = []
    
    for q in queries:
        url = f"https://api.hh.ru/vacancies?text={q}&area=1&per_page=10"
        res = requests.get(url, headers={'User-Agent': 'HH-User-Agent'})
        if res.status_code == 200:
            data = res.json()
            # Берем среднюю зарплату и количество вакансий
            count = data.get('found', 0)
            items = data.get('items', [])
            avg_salary = 0
            valid_salaries = 0
            
            for i in items:
                sal = i.get('salary')
                if sal and sal.get('from'):
                    avg_salary += sal.get('from')
                    valid_salaries += 1
            
            results.append({
                "query": q,
                "count": count,
                "avg_salary": int(avg_salary / valid_salaries) if valid_salaries > 0 else 0
            })
    return results

if __name__ == "__main__":
    stats = get_hh_stats()
    os.makedirs('data', exist_ok=True)
    with open('data/deals.json', 'w', encoding='utf-8') as f:
        json.dump(stats, f, indent=2, ensure_ascii=False)
