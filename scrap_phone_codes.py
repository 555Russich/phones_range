"""Build phone_codes.json from the official DEF-9xx numbering-plan CSV.

Source: "Выписка из реестра Российской системы и плана нумерации" published by
Минцифры России (opendata.digital.gov.ru) — the authoritative list of 9xx
mobile ranges allocated to operators. Public allocation data, no personal info.

codificator.ru (the old source) is now behind a captcha, so this reads the
official CSV instead. The portal gates automated downloads and serves TLS via
the Russian national CA, so the reliable path is: download DEF-9xx.csv in a
browser, then pass it here. A best-effort auto-download is attempted first.

    python scrap_phone_codes.py [path/to/DEF-9xx.csv]   # default: ./DEF-9xx.csv
"""
import csv
import json
import sys
from datetime import date
from pathlib import Path

FILEPATH_JSON = Path('phone_codes.json')
DEFAULT_CSV = Path('DEF-9xx.csv')
SOURCE_URL = 'https://opendata.digital.gov.ru/downloads/DEF-9xx.csv'
SOURCE_PAGE = 'https://opendata.digital.gov.ru/registry/numeric/downloads/'


def ask_user(question: str) -> bool:
    answer = input(f'{question} [y/n]: ').strip().lower()
    while answer not in ('y', 'n'):
        answer = input('Enter y(es) or n(o): ').strip().lower()
    return answer == 'y'


def _rows_from_csv(path: Path):
    # Official file: Windows-1251, ';'-separated, one header row.
    # Parsed by column position (code;from;to;capacity;operator;region;...)
    # so it survives header-text changes.
    with open(path, encoding='cp1251', newline='') as f:
        next(f, None)  # header
        for row in csv.reader(f, delimiter=';'):
            if len(row) < 6:
                continue
            code, frm, to, cap, operator, region = (c.strip() for c in row[:6])
            if not (code.isdigit() and frm.isdigit() and to.isdigit()):
                continue
            yield code, int(frm), int(to), int(cap) if cap.isdigit() else int(to) - int(frm) + 1, operator, region


def csv_to_data(path: Path) -> dict:
    data = {}
    for code, frm, to, cap, operator, region in _rows_from_csv(path):
        data.setdefault(code, []).append({
            'Регион РФ': region,
            'Оператор': operator,
            'Диапазон номеров': [[frm, to]],
            'Кол-во номеров': cap,
        })
    if not data:
        sys.exit(f'No valid rows parsed from {path}. Is it the DEF-9xx CSV?')
    data['last_update'] = date.today().strftime('%d.%m.%Y')
    return data


def try_download(path: Path) -> bool:
    import requests  # only needed for the optional auto-download
    try:
        r = requests.get(SOURCE_URL, timeout=60, headers={'User-Agent': 'Mozilla/5.0'})
        r.raise_for_status()
        if b';' not in r.content[:2000]:  # got an HTML/captcha page, not the CSV
            return False
        path.write_bytes(r.content)
        return True
    except Exception as e:
        print(f'Auto-download failed: {e}')
        return False


def main() -> dict:
    csv_path = Path(sys.argv[1]) if len(sys.argv) > 1 else DEFAULT_CSV
    if not csv_path.exists():
        print(f'CSV not found: {csv_path}')
        if not (ask_user(f'Try downloading from {SOURCE_URL}?') and try_download(csv_path)):
            sys.exit(
                f'\nDownload DEF-9xx.csv manually from:\n  {SOURCE_PAGE}\n'
                f'then run:  python scrap_phone_codes.py <path-to-DEF-9xx.csv>'
            )
        print(f'Downloaded -> {csv_path}')

    data = csv_to_data(csv_path)
    with open(FILEPATH_JSON, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)
    print(f'Wrote {FILEPATH_JSON} ({len(data) - 1} codes)')
    return data


if __name__ == '__main__':
    main()
