This repository can help you scrap possible phone numbers,
generate password dict based on scrapped phones ranges 
to crack with `hashcat` or similar tool.

### Now supports only `+7` code

#### Preamble
Crack all phone's range using GPU such as `GTX 960 4gb` taking about 
<text style="font-size: 20px">3-4 hours</text>... 
My thoughts to make it faster (ofc if we are lucky):

If you know region OR mobile operator OR code which that phone can use,
you can generate possible phones based on this information.</b>

### Requirements
`python3` (stdlib only).

`requests` is optional — only for the best-effort auto-download in step 1.

### Installation

``` commandline
git clone https://github.com/555Russich/phones_range
cd phones_range
```

### Usage

1. Get phone ranges as `json` from the official numbering registry.

   The old source (codificator.ru) is now behind a captcha, so this uses the
   authoritative **"Выписка из реестра Российской системы и плана нумерации"**
   published by Минцифры России. Download `DEF-9xx.csv` (the 9xx mobile block) from:

   https://opendata.digital.gov.ru/registry/numeric/downloads/

   then convert it:
``` commandline
python3 scrap_phone_codes.py DEF-9xx.csv
```
   Run with no argument to attempt an auto-download (`pip3 install requests` first);
   the portal often blocks it, in which case download the file in a browser as above.

2. Generate password dict based on `json` file. Filters can be passed as arguments

```commandline
python3 gen_dict.py --help
usage: gen_dict.py [-h] [--list-codes] [--list-regions] [--list-operators] [-c CODE] [-r REGION] [-o OPERATOR]

options:
  -h, --help            show this help message and exit
  --list-codes
  --list-regions
  --list-operators
  -c CODE, --code CODE
  -r REGION, --region REGION
  -o OPERATOR, --operator OPERATOR
```

Filter values must match the `--list-*` output exactly — in the official
registry operators are full legal names (e.g. `ПАО "МТС"`, `ООО "Т2 МОБАЙЛ"`)
and regions come from the ГАР territory (e.g. `Краснодарский край`). List them
first, then copy the value you want.

Examples:

Generate all possible phones (huge — hundreds of millions of numbers, filter instead):

`python3 gen_dict.py`

Region filter: 

`python3 gen_dict.py -r "Московская область"`

Operator filter:

`python3 gen_dict.py -o 'ПАО "МТС"'`

All regions to stdout:

`python3 gen_dict.py --list-regions`

All operators to stdout:

`python3 gen_dict.py --list-operators` 

It's possible to combine filters and pass few values for one filter

Generated dict will look like that:

```text
9160000000
9160000001
9160000002
9160000003
9160000004
9160000005
9160000006
9160000007
9160000008
9160000009
...
```

After that you can run `hashcat` and use `phones.rule` file:

```commandline
hashcat <some_more_parameters> -r phones.rule <your_hash_file> phones_filtered.dict
```
