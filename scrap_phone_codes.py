import json
import re
from datetime import datetime
from pathlib import Path

import requests
from bs4 import BeautifulSoup


DOMAIN = 'https://codificator.ru'
FILEPATH_JSON = Path('phone_codes.json')


def ask_user(question: str) -> bool:
    answer = input(f'{question}: ')
    while True:
        if answer == 'y':
            return True
        elif answer == 'n':
            return False
        else:
            answer = input('Enter y(es) or n(o): ')


def is_update_needed(date_website: datetime) -> bool:
    if FILEPATH_JSON.exists():
        with open(FILEPATH_JSON, 'r', encoding='utf-8') as f:
            date_infile = datetime.strptime(json.load(f)['last_update'], '%d.%m.%Y')
        print(f'Date on website  : {date_website.strftime("%d.%m.%Y")}\n'
              f'Date in json file: {date_infile.strftime("%d.%m.%Y")}')
        if date_website > date_infile:
            return ask_user('Run scrapper to update info?')
        return False
    else:
        return True

def scrap_codes_info(soup: BeautifulSoup) -> dict:
    data = {}
    extra_codes = re.findall(r'\d{3}', soup.find('div', class_='d-flex flex-wrap gap-5').find_next_sibling('p').text)
    extra_codes += [
        code.strip()
        for tr in soup.find_all('table', class_='table table-bordered table-width-auto')[1].tbody.find_all('tr')[1:]
        for code in tr.find_all('td')[1].text.split(',')
    ]
    do_add_extra_codes = ask_user(f'Scrap "extra" codes: ({", ".join(extra_codes)})?')

    for code in [a.text for a in soup.find('div', class_='list-mobile-codes mb-3').find_all('a')]:
        if not do_add_extra_codes and code in extra_codes:
            continue

        r = requests.get(f'{DOMAIN}/code/mobile/{code}')
        soup = BeautifulSoup(r.text, 'lxml')

        table = soup.find('table', class_='table table-bordered table-mobile-phones table-width-auto')
        columns = [th.text for th in table.thead.tr.find_all('th')]

        code_data = []
        for tr in table.tbody.find_all('tr'):
            row_data = {}
            tds = tr.find_all('td')
            for i in range(len(columns)):
                if columns[i] == 'Вид номеров':
                    values = tds[i].get_text('\n').split('\n')
                    if len(values) == 1:
                        value = values
                    else:
                        prefix = values[0][:-len(values[1])]
                        value = [values[0]] + [prefix + v for v in values[1:]]
                elif columns[i] == 'Диапазон номеров':
                    values = tds[i].get_text('\n').split('\n')
                    value = [
                        [int(n) for n in v.replace(f'+7 {code}', '').replace(' ', '').split('...')]
                        for v in values
                    ]
                elif columns[i] == 'Кол-во номеров':
                    value = int(tds[i].text.replace(' ', ''))
                else:
                    value = tds[i].text
                row_data[columns[i]] = value
            code_data.append(row_data)
        data[code] = code_data
        print(f'Scrapped data for code: {code}')
    return data


def main() -> dict:
    r = requests.get(DOMAIN + '/code/mobile')
    soup = BeautifulSoup(r.text, 'lxml')

    last_updates_text = soup.find('p', class_='mt-3 mb-1 fst-italic').get_text('\n')
    date_website = datetime.strptime(
        re.search(r'\d{2}\.\d{2}\.\d{4}(?=.)', last_updates_text).group(0), '%d.%m.%Y'
    )

    if is_update_needed(date_website):
        data = scrap_codes_info(soup)
        data['last_update'] = date_website.strftime('%d.%m.%Y')
        with open(FILEPATH_JSON, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
    else:
        if not FILEPATH_JSON.exists():
            print('Для продолжения нужно спарсить данные...')
            exit()
        with open(FILEPATH_JSON, 'r', encoding='utf-8') as f:
            data = json.load(f)
    return data


if __name__ == '__main__':
    main()
