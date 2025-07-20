import requests
import json
import os

HH_API_URL = 'https://api.hh.ru/vacancies'
PARAMS = {
    'text': 'product manager',
    'area': 1,
    'search_period': 1,
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
    return {
        f"{item['id']}_{item['published_at']}": item['alternate_url']
        for item in items
    }


def send_telegram_message(text):
    url = f'https://api.telegram.org/bot{TOKEN}/sendMessage'
    data = {'chat_id': CHAT_ID, 'text': text}
    requests.post(url, data=data)


def main():
    seen = load_seen()
    current = get_vacancies()

    new_ids = set(current.keys()) - seen

    if new_ids:
        for vid in new_ids:
            send_telegram_message(current[vid])
    else:
        send_telegram_message("Новых вакансий нет")

    save_seen(seen | new_ids)


if __name__ == "__main__":
    main()