from typing import List, Dict

from time import sleep

from requests import get
from bs4 import BeautifulSoup
from selenium import webdriver

from utils import ALL_LINKS, HEADERS, get_insert_data
from config import BRANDS, GenderTypes
from services import insert_product
from db.db import recreate_db_and_tables
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

        product_list.append(product_url)
    if product_list:
        product_dict[gender.value] = product_list
        return product_dict


async def get_data(gender_links: ALL_LINKS):
    print('Начинается сбор данных')
    options = webdriver.EdgeOptions()

    try:
        driver = webdriver.Edge(options=options)
        data = list()
        counter = 1

        for d in gender_links:
            for key, value in d.items():
                for url in value:
                    driver.get(url)
                    sleep(4)

                    soup = BeautifulSoup(driver.page_source, "lxml")
                    data.append(get_insert_data(soup, key))

                    print(f'Объект #{counter} добавился успешно')
                    counter += 1

        await insert_product(data)
        print('Cбор данных успешно завершён')
    except Exception as e:
        print(e)
    finally:
        driver.close()
        driver.quit()


def collect_links() -> List[ALL_LINKS] | NotLinksException:
    women_links = list()
    men_links = list()
    boys_links = list()
    girls_links = list()

    for i in BRANDS:
        for women in range(1, 3):
            page_links = get_all_links(f'https://www.yoox.com/ru/%D0%B4%D0%BB%D1%8F%20%D0%B6%D0%B5%D0%BD%D1%89%D0%B8%D0%BD/shoponline/?d={i}&page={women}', GenderTypes.women)
            women_links.append(page_links) if page_links else None
            print(f'Собраны все ссылки со страницы {women} бренда {i} у женщин')

        for men in range(1, 3):
            page_links = get_all_links(f'https://www.yoox.com/ru/%D0%B4%D0%BB%D1%8F%20%D0%BC%D1%83%D0%B6%D1%87%D0%B8%D0%BD/shoponline/?d={i}&page={men}', GenderTypes.men)
            men_links.append(page_links) if page_links else None
            print(f'Собраны все ссылки со страницы {men} бренда {i} у мужчин')

        for boys in range(1, 3):
            page_links = get_all_links(f'https://www.yoox.com/ru/%D0%B4%D0%BB%D1%8F%20%D0%BC%D0%B0%D0%BB%D1%8C%D1%87%D0%B8%D0%BA%D0%BE%D0%B2/%D0%BF%D0%BE%D0%B4%D1%80%D0%BE%D1%81%D1%82%D0%BA%D0%B8/shoponline/?dept=collboy_junior&d={i}&page={boys}', GenderTypes.boys)
            boys_links.append(page_links) if page_links else None
            print(f'Собраны все ссылки со страницы {boys} бренда {i} у мальчиков')

        for girls in range(1, 3):
            page_links = get_all_links(f'https://www.yoox.com/ru/%D0%B4%D0%BB%D1%8F%20%D0%B4%D0%B5%D0%B2%D0%BE%D1%87%D0%B5%D0%BA/%D0%BF%D0%BE%D0%B4%D1%80%D0%BE%D1%81%D1%82%D0%BA%D0%B8/shoponline/?dept=collgirl_junior&d={i}&page={girls}', GenderTypes.girls)
            girls_links.append(page_links) if page_links else None
            print(f'Собраны все ссылки со страницы {girls} бренда {i} у девочек')

    print('Сбор ссылок завершён')

    if all_links := [array for array in (women_links, men_links, boys_links, girls_links) if array]:
        return all_links
    raise NotLinksException()


async def main(launch: int):
    await recreate_db_and_tables() if launch == 0 else None
    all_links = collect_links()
    await get_data(all_links[launch])


if __name__ == '__main__':
    print('Программа запущена')
    try:
        while True:
            pass
    except KeyboardInterrupt:
        print('Прогрмма остановлена')
