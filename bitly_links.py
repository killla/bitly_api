import os
import requests
import argparse
from urllib.parse import urlparse

from dotenv import load_dotenv


URL_TEMPLATE = 'https://api-ssl.bitly.com/v4{}'


def create_bitlink(token, link):
    command = '/bitlinks'
    url = URL_TEMPLATE.format(command)
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
    url = URL_TEMPLATE.format(command)
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

    url = URL_TEMPLATE.format(command)
    response = requests.get(url, headers=headers)
    return response.ok


if __name__ == '__main__':
    load_dotenv()
    bitly_token = os.getenv('BITLY_TOKEN')

    parser = argparse.ArgumentParser(
        description='Подсчет переходов по ссылке. При передаче ссылке выдаст bitlink. При передаче bitlink выдаст количество переходов.'
    )
    parser.add_argument('link', help='ссылка или bitlink')
    args = parser.parse_args()
    user_link = args.link

    is_bitlink = check_bitlink(bitly_token, user_link)

    try:
        if is_bitlink:
            clicks_count = count_clicks(bitly_token, user_link)
            print('Количество кликов: ', clicks_count)
        else:
            bitlink = create_bitlink(bitly_token, user_link)
            print('Битлинк: ', bitlink)
    except requests.exceptions.HTTPError:
        print('Неверная ссылка')
