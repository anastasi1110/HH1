import requests
import json
import os

HH_API_URL = 'https://api.hh.ru/vacancies'
PARAMS = {
    'text': 'product manager',
    'area': 1,  # Москва
    'search_period': 1,  # Опубликованы за сутки
    'per_page': 50
}

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
    resp = requests.get(HH_API_URL, params=PARAMS)
    resp.raise_for_status()
    items = resp.json().get('items', [])
    return {item['alternate_url'] for item in items}


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