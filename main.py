from typing import List, Dict

from time import sleep

from requests import get
from bs4 import BeautifulSoup

from utils import ALL_LINKS, HEADERS, get_insert_data
from config import BRANDS, GenderTypes
from services import insert_product
from db.db import recreate_tables
from exceptions import NotLinksException


def get_all_links(url: str, gender: GenderTypes) -> Dict[GenderTypes, List[str]] | None:
    response = get(url, headers=HEADERS)
    sleep(2)

    soup = BeautifulSoup(response.text, "lxml")
    all_products = soup.find_all('div', class_='col-8-24')

    product_dict = dict()
    product_list = list()
    for product in all_products:
        href = product.find('div', class_='itemImg text-center img-separator')
        try:
            product_url = 'https://www.yoox.com' + href.find('a').get('href')
        except AttributeError:
            continue

        if '#' in product_url:
            product_url = product_url.replace('#', '?')
        product_list.append(product_url)
    if product_list:
        product_dict[gender.value] = product_list
        return product_dict


async def get_data(gender_links: ALL_LINKS):
    print('Начинается сбор данных')

    data = list()
    counter = 1

    for d in gender_links:
        for key, value in d.items():
            for url in value:
                r = get(url, headers=HEADERS)
                sleep(2)

                soup = BeautifulSoup(r.text, "lxml")
                data.append(get_insert_data(soup, key))

                print(f'Объект #{counter} добавился успешно')
                counter += 1

    await insert_product(data)
    print('Cбор данных успешно завершён')


def collect_links() -> List[ALL_LINKS] | NotLinksException:
    women_links = list()
    men_links = list()
    boys_links = list()
    girls_links = list()

    for brand in BRANDS:
        for women in range(1, 4):
            page_links = get_all_links(
                f'https://www.yoox.com/us/women/shoponline/?d={brand}&page={women}',
                GenderTypes.women
            )
            women_links.append(page_links) if page_links else None
            print(f'Собраны все ссылки со страницы {women} бренда {brand} у женщин')

        for men in range(1, 4):
            page_links = get_all_links(
                f'https://www.yoox.com/us/men/shoponline/?d={brand}&page={men}', GenderTypes.men
            )
            men_links.append(page_links) if page_links else None
            print(f'Собраны все ссылки со страницы {men} бренда {brand} у мужчин')

        for boys in range(1, 3):
            page_links = get_all_links(
                f'https://www.yoox.com/us/boy/collections/junior/shoponline/?dept=collboy_junior&d={brand}&page={boys}',
                GenderTypes.boys
            )
            boys_links.append(page_links) if page_links else None
            print(f'Собраны все ссылки со страницы {boys} бренда {brand} у мальчиков')

        for girls in range(1, 3):
            page_links = get_all_links(
                f'https://www.yoox.com/us/girl/collections/junior/shoponline/?dept=collgirl_junior&d={brand}&page={girls}',
                GenderTypes.girls
            )
            girls_links.append(page_links) if page_links else None
            print(f'Собраны все ссылки со страницы {girls} бренда {brand} у девочек')

    print('Сбор ссылок завершён')

    if all_links := [array for array in (women_links, men_links, boys_links, girls_links) if array]:
        return all_links
    raise NotLinksException()


async def main(launch: int):
    await recreate_tables() if launch == 0 else None
    all_links = collect_links()
    await get_data(all_links[launch])


if __name__ == '__main__':
    print('Программа запущена')
    try:
        while True:
            pass
    except KeyboardInterrupt:
        print('Прогрмма остановлена')
