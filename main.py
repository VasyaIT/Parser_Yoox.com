from typing import List, Dict

from time import sleep

from requests import get
from bs4 import BeautifulSoup

from utils import ALL_LINKS, HEADERS, get_insert_data
from config import BRANDS, GenderTypes
from services import insert_product
from db.db import recreate_tables
from exceptions import NotLinksException


def get_all_links(
        url: str, gender: GenderTypes
) -> Dict[GenderTypes, Dict[str, List[str]]] | Dict[None, None]:
    response = get(url, headers=HEADERS)
    sleep(2)

    soup = BeautifulSoup(response.text, "lxml")
    all_products = soup.find_all('div', class_='col-8-24')

    products_dict = dict()
    product_dict = dict()
    for product in all_products:
        href = product.find('div', class_='itemImg text-center img-separator')
        all_sizes = product.find_all(class_='aSize')
        try:
            product_url = 'https://www.yoox.com' + href.find('a').get('href')
        except AttributeError:
            continue
        try:
            sizes = [size.text.strip() for size in all_sizes]
        except AttributeError:
            continue

        if '#' in product_url:
            product_url = product_url.replace('#', '?')
        product_dict[product_url] = sizes

    if product_dict:
        products_dict[gender.value] = product_dict
    return products_dict


def get_data(gender_links: ALL_LINKS):
    print('Начинается сбор данных')

    data = list()
    counter = 1

    for d in gender_links:
        for key, value in d.items():
            for url, sizes in value.items():
                r = get(url, headers=HEADERS)
                sleep(2)

                soup = BeautifulSoup(r.text, "lxml")
                data.append(get_insert_data(soup, key, sizes))

                print(f'Объект #{counter} добавился успешно')
                counter += 1

    insert_product(data)
    print('Cбор данных успешно завершён')


def collect_links(launch: int) -> ALL_LINKS | NotLinksException:
    all_links = list()

    for brand in BRANDS:
        if launch == 0:
            for women in range(1, 4):
                page_links = get_all_links(
                    f'https://www.yoox.com/us/women/shoponline/?d={brand}&page={women}',
                    GenderTypes.women
                )
                all_links.append(page_links)
                print(f'Собраны все ссылки со страницы {women} бренда {brand} у женщин')

        if launch == 1:
            for men in range(1, 4):
                page_links = get_all_links(
                    f'https://www.yoox.com/us/men/shoponline/?d={brand}&page={men}', GenderTypes.men
                )
                all_links.append(page_links)
                print(f'Собраны все ссылки со страницы {men} бренда {brand} у мужчин')

        if launch == 2:
            for boys in range(1, 3):
                page_links = get_all_links(
                    f'https://www.yoox.com/us/boy/collections/junior/shoponline/?dept=collboy_junior&d={brand}&page={boys}',
                    GenderTypes.boys
                )
                all_links.append(page_links)
                print(f'Собраны все ссылки со страницы {boys} бренда {brand} у мальчиков')
        if launch == 3:
            for girls in range(1, 3):
                page_links = get_all_links(
                    f'https://www.yoox.com/us/girl/collections/junior/shoponline/?dept=collgirl_junior&d={brand}&page={girls}',
                    GenderTypes.girls
                )
                all_links.append(page_links)
                print(f'Собраны все ссылки со страницы {girls} бренда {brand} у девочек')

    print('Сбор ссылок завершён')

    if all_links:
        return all_links
    raise NotLinksException()


def main(launch: int):
    recreate_tables() if launch == 0 else None
    all_links = collect_links(launch)
    get_data(all_links)


if __name__ == '__main__':
    print('Программа запущена')
    try:
        while True:
            pass
    except KeyboardInterrupt:
        print('Прогрмма остановлена')
