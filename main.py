import requests
from bs4 import BeautifulSoup
import json
from fake_headers import Headers
from tqdm import tqdm


def gen_headers():
    headers = Headers(browser='chrome', os='win')
    return headers.generate()


def parser_hh_ru():
    vacancy_file = {}

    ind = 0

    url = 'https://spb.hh.ru/search/vacancy?search_field=name&search_field=company_name&search_field=description&enable_snippets=false&L_save_area=true&area=1&area=2&text=Python+Django+Flask'

    response = requests.get(url=url, headers=gen_headers())

    if response.status_code:

        soup = BeautifulSoup(response.text, 'lxml')

        data = soup.find_all('div', class_='serp-item serp-item_link')

        for i in tqdm(data):
            link = i.find('a', class_='bloko-link').get('href')
            price = i.find('span', class_='bloko-header-section-2')
            if price is None:
                continue
            else:
                ind += 1
                price = i.find('span', class_='bloko-header-section-2').text.replace(u"\u202F", " ")
                name_company = i.find_all('div', class_='bloko-text')[0].text
                city = i.find_all('div', class_='bloko-text')[1].text.split(',')[0]

                vacancy_file.setdefault(f'vacancy_{ind}', {'link': link,
                                                           'price': price,
                                                           'name_company': name_company,
                                                           'city': city})
    return vacancy_file


def create_file():
    with open('vacancy_file.json', 'w', encoding='utf-8') as f:
        json.dump(parser_hh_ru(), f, ensure_ascii=False,  indent=4)


if __name__ == "__main__":
    parser_hh_ru()
    create_file()