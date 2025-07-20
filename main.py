import requests
import json
import os

SEEN_FILE = 'seen.json'
TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")


def load_seen():
    try:
        with open(SEEN_FILE, 'r') as f:
            return set(json.load(f))
    except FileNotFoundError:
        return set()


def save_seen(seen):
    with open(SEEN_FILE, 'w') as f:
        json.dump(list(seen), f)


def get_vacancies():
    url = 'https://api.hh.ru/vacancies'
    params = {
        'text': 'product manager',
        'area': 1,
        'search_period': 1,
        'per_page': 50
    }
    headers = {
        'User-Agent': 'VacancyTelegramBot/1.0 (+contact@example.com)'
    }

    resp = requests.get(url, params=params, headers=headers)
    resp.raise_for_status()
    data = resp.json()

    return {item['alternate_url'] for item in data['items']}


def send_telegram_message(text):
    url = f'https://api.telegram.org/bot{TOKEN}/sendMessage'
    data = {'chat_id': CHAT_ID, 'text': text}
    requests.post(url, data=data)


def main():
    seen = load_seen()
    current = get_vacancies()
    new = current - seen

    if new:
        for url in new:
            send_telegram_message(url)
    else:
        send_telegram_message("Новых вакансий нет")

    save_seen(current)


if __name__ == "__main__":
    main()
