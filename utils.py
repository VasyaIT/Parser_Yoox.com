import csv
import json
from typing import Any, Iterable, Sequence, Dict, List

from bs4 import BeautifulSoup
from fake_useragent import FakeUserAgent

from config import GenderTypes

# fua = FakeUserAgent().random

ALL_LINKS = List[Dict[GenderTypes, List[str]]]

HEADERS = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,'
              'image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'User-Agent': "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.106 Safari/537.36"
}


def write_in_json(file: str, mode: str, data: Iterable[Any]) -> None:
    with open(file, mode, encoding='utf-8') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)


def write_in_file(file: str, data: Any) -> None:
    with open(file, 'a', encoding='utf-8') as f:
        f.write(data)


def write_in_csv(file: str, data: Iterable[Any]) -> None:
    with open(file, "a", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(data)


def get_insert_data(soup: BeautifulSoup, gender: str) -> Dict[str, str | int | Sequence[str]]:
    data = dict()

    product_id = (soup.find('div', class_='Details_code10__1V6sY')
                  .find(class_='MuiBody2-body2 MuiBody2-wide').text.strip())
    data['id'] = product_id.split(':')[1].strip()
    data['brand'] = soup.find('h1', class_='MuiTitle3-title3').find('a').text.strip()
    data['category'] = (soup.find('h2', class_='MuiBody1-body1 ItemInfo_microcat__ffpIA')
                        .find('a').text.strip())
    data['description'] = (soup.find('div', class_='Details_details__0Zm5h')
                           .find(class_='MuiBody1-body1 MuiBody1-wide').text.strip())
    data['price'] = (
        (soup.find('div', class_='MuiTitle4-title4 ItemInfo_currentPrice__n4v78')
         .find_next().find_next().text.split('$')[1].strip())
    )
    data['colors'] = [
        color.get('title').strip()
        for color in soup.find_all('div', class_='ColorPicker_color-sample__IyQPv')
    ]
    data['sizes'] = [
        size.text.strip()
        for size in soup.find_all('span', class_='MuiBody1-body1 SizePicker_size-title__0ILZs')
    ]

    data['images'] = [
        image.find('img').get('src')
        for image in soup.find('div', class_='jss1').find_all(class_='jss1')
    ]
    data['gender'] = gender

    return data
