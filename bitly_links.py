import os
import requests
from urllib.parse import urlparse

from dotenv import load_dotenv


load_dotenv()
url_template = 'https://api-ssl.bitly.com/v4{}'
BITLY_TOKEN = os.getenv("TOKEN")


def create_bitlink(token, link):
    command = '/bitlinks'
    url = url_template.format(command)
    payload = {
        'long_url': link,
    }
    headers = {
        'Authorization': f'Bearer {token}'
    }

    response = requests.post(url, headers=headers, json=payload)
    response.raise_for_status()
    short_link = response.json()['link']
    return short_link


def count_clicks(token, link):
    parsed_link = urlparse(link)
    command = f'/bitlinks/{parsed_link.netloc}{parsed_link.path}/clicks/summary'
    url = url_template.format(command)
    headers = {
        'Authorization': f'Bearer {token}'
    }

    response = requests.get(url, headers=headers)
    response.raise_for_status()
    total_clicks = response.json()['total_clicks']
    return total_clicks


def check_bitlink(token, link):
    parsed_link = urlparse(link)
    command = f'/bitlinks/{parsed_link.netloc}{parsed_link.path}'
    headers = {
        'Authorization': f'Bearer {token}'
    }

    url = url_template.format(command)
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return response.ok


if __name__ == "__main__":
    user_input = input('Введите ссылку: ').strip()
    is_bitlink = False

    try:
        is_bitlink = check_bitlink(BITLY_TOKEN, user_input)
    except requests.exceptions.HTTPError:
        is_bitlink = False

    if is_bitlink:
        try:
            clicks_count = count_clicks(BITLY_TOKEN, user_input)
            print('Количество кликов: ', clicks_count)
        except requests.exceptions.HTTPError:
            print('Неверная ссылка')
    else:
        try:
            bitlink = create_bitlink(BITLY_TOKEN, user_input)
            print('Битлинк: ', bitlink)
        except requests.exceptions.HTTPError:
            print('Неверная ссылка')
