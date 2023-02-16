import argparse
import json
from pathlib import Path

from scrap_phone_codes import FILEPATH_JSON, ask_user


def get_list_of_key(data: dict, key: str) -> list[str]:
    uniq = set()
    for code, lst in data.items():
        for d in lst:
            for k, v in d.items():
                if k == key:
                    uniq.add(v)
    return sorted(uniq)


def check_filter_values(values: list, available_values: list):
    for reg in values:
        if reg not in available_values:
            print(f'Value: {reg} not available. See available filter list with "--list-<filter>"')
            exit()


def create_filtered_dict(data: dict, args) -> list:
    code_ranges = []
    for code, lst, in data.items():
        for d in lst:
            region = d['Регион РФ']
            operator_ = d.get('Оператор')

            if code in args.code:
                if not args.region and not args.operator or \
                        region in args.region and not args.operator or \
                        not args.region and operator_ in args.operator or \
                        region in args.region and operator_ in args.operator:
                    code_ranges.append((code, d['Диапазон номеров'], d['Кол-во номеров']))
            elif region in args.region:
                if not args.code and not args.operator or \
                        code in args.code and not args.operator or \
                        not args.code and operator_ in args.operator or \
                        code in args.code and operator_ in args.operator:
                    code_ranges.append((code, d['Диапазон номеров'], d['Кол-во номеров']))
            elif operator_ in args.operator:
                if not args.code and not args.region or \
                        code in args.code and not args.region or \
                        not args.code and region in args.region or \
                        code in args.code and region in args.region:
                    code_ranges.append((code, d['Диапазон номеров'], d['Кол-во номеров']))

    return sorted(code_ranges, key=lambda x: x[2], reverse=True)


def create_dict(codes_data: list, filepath: Path):
    with open(filepath, 'a', encoding='utf-8') as f:
        for t in codes_data:
            for code_range in t[1]:
                for n in range(code_range[0], code_range[1]+1):
                    f.write(f'{t[0]}{n}\n')


def main():
    with open(FILEPATH_JSON, 'r', encoding='utf-8') as f:
        data = json.load(f)
    del data['last_update']

    parser = argparse.ArgumentParser()
    parser.add_argument('--list-codes', action='store_true')
    parser.add_argument('--list-regions', action='store_true')
    parser.add_argument('--list-operators', action='store_true')
    parser.add_argument('-c', '--code', action='append', default=[])
    parser.add_argument('-r', '--region', action='append', default=[])
    parser.add_argument('-o', '--operator', action='append', default=[])
    args = parser.parse_args()

    if args.list_codes:
        for v in data.keys():
            print(v)
    if args.list_regions:
        for v in get_list_of_key(data, 'Регион РФ'):
            print(v)
    if args.list_operators:
        for v in get_list_of_key(data, 'Оператор'):
            print(v)

    if args.code:
        check_filter_values(args.codes, data.keys())
    if args.region:
        check_filter_values(args.region, get_list_of_key(data, 'Регион РФ'))
    if args.operator:
        check_filter_values(args.operator, get_list_of_key(data, 'Оператор'))

    if not args.code and not args.region and not args.operator:
        print('No one filter was selected, exiting...')
        exit()

    filepath_dict = Path('phones_filtered.dict')
    if filepath_dict.exists():
        if ask_user(f'File {filepath_dict.absolute()} already exists. Rewrite?'):
            filepath_dict.unlink()
        else:
            exit()

    codes_data = create_filtered_dict(data, args)
    create_dict(codes_data, filepath_dict)


if __name__ == '__main__':
    main()