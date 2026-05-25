# Выжимка чата: 20-й пакет санкций ЕС, крипто-провайдеры РФ/РБ, риски Cifra Markets

## 1. Контекст: 20-й пакет санкций ЕС (23 апреля 2026)

- **Не точечный список**, а **сплошной запрет** для лиц ЕС на любые транзакции со всеми CASP, зарегистрированными в РФ и РБ.
- Поименно в Annex: цифровой рубль, RUBx, A7A5, кыргызская TengriCoin, ряд банков.
- AML-вендоры (Chainalysis, TRM, Elliptic) **сами** «красят» кластеры адресов, относя их к подсанкционным CASP — отсюда расхождения между вендорами.

## 2. Cifra Markets / Tradersnet в публичных источниках

- Ни Cifra Markets, ни Tradersnet **не фигурируют** именованно в Tether blacklist и в EU designations.
- Cifra — лицензированный белорусский брокер (ПВТ), формально под общий запрет 20-го пакета подпадает как белорусский CASP.
- Tradersnet — в публичном поле по санкционке не находится.
- On-chain проверку в этой сессии сделать не удалось: Arkham, Tronscan, AMLBot, Etherscan logs API — все вернули 403 (анти-бот). Без конкретных адресов `isBlackListed` не дёргается.

## 3. USDC vs USDT для Cifra

Переход на USDC снимает **только один риск** (заморозка Tether) и слегка **повышает другой** (Circle проактивнее по US-комплайнсу).

| Риск | Меняет переход USDT→USDC? |
|---|---|
| Заморозка от Tether | **Да** (снимает) |
| Заморозка от Circle | **Нет**, обычно жёстче |
| Попадание под EU 20-й пакет | **Нет** (вид актива не важен) |
| AML-маркировка адресов | **Нет** |
| Риск контрагента (Cifra не отдаст рубли) | **Нет** |
| Блокировка карты по 115-ФЗ на выводе | **Нет** |

## 4. Circle vs Tether по России

- **Исторически** Circle строже и быстрее по OFAC (Tornado Cash — заморозил в день designations; Tether отказался).
- **По России в 2025–2026** Tether догнал и местами обогнал: март 2025 — заморозил 2.5 млрд руб. на Garantex (89 адресов, $22.8M) после EU 16th.
- USDC в РФ-обороте почти нет → Circle «нечего замораживать», а не «не хочет».
- При designations конкретно на Cifra — оба заморозят с разницей в часы.

## 5. Односторонняя схема «CEX → Cifra → рубли»

Прямой риск ниже (нет входящей грязи), но не нулевой. Три вектора:

1. **Исходящая биржа видит destination**. Major CEX (Binance/Bybit/OKX) знают, что вы вывели на адрес, помеченный их KYT как российский CASP. Систематически → SOF-запрос, ограничение вывода, заморозка по ToS.
2. **TRM/Elliptic считают outgoing exposure** для sanctions/terror финансирования. Биржи на TRM (Coinbase, Kraken, EU-биржи) флагнут на основании только исходящих.
3. **Кросс-биржевая видимость через KYT**: если исходный кошелёк потом используется на других биржах — новые KYC-проверки увидят историю.

**Юридический слой**: для лиц ЕС использование Cifra после 20-го пакета — нарушение санкций ЕС, отдельно от on-chain. Для резидентов РФ/РБ — нет, но если есть счета в EU-биржах/банках, риск переезжает туда.

## 6. AML-сервисы — что использовать (для retail)

| Сервис | Зачем | Цена |
|---|---|---|
| **AMLBot** (`@AMLbot_bot`) | Основной. Агрегирует Chainalysis/Crystal/ScoreChain, даёт разбивку по вендорам — видно, кто как красит | ~$1–2 за проверку, первая бесплатно |
| **Misttrack** (SlowMist) | Бесплатное «второе мнение», сильнее по hack/scam | Бесплатно с лимитом |
| **Bitrace / GetBlock AML** | Если USDT-TRC20 — Bitrace видит то, что западные пропускают | Платно, есть пробные |

**Чего избегать**: Chainalysis Reactor/TRM/Elliptic (enterprise, retail не пустят); подозрительно дешёвые TG-боты (часто скам/фейк-отчёты).

### Как читать результат

| Что видно | Что делать |
|---|---|
| Sanctions exposure: **direct** | Не депозить, потеряете средства |
| Sanctions exposure: **1 hop, >10%** | Высокий риск флага у приёмной биржи |
| High-risk **>30%** (без sanctions) | Серая зона, повлияет на отправку с CEX |
| Risk **<10%, clean** | Безопасно сейчас, перепроверять через время |

## 7. Практические выводы для пользователя

1. **Чекать в две стороны**: и адрес Cifra (для понимания, как увидит исходящая биржа), и свой кошелёк (растёт скор за счёт исходящей экспозиции).
2. **Промежуточный кошелёк** между основной CEX и Cifra — обязателен. Используется **только** под эту схему, обратно на CEX депозиты не идут.
3. **Сегментация и ротация**: периодически (раз в месяц) чекать промежуточный кошелёк в 2–3 сервисах, при росте скора — бросать и заводить новый.
4. **Не систематически с одной биржи**: у major CEX есть pattern-детектор по повторяющимся выводам на high-risk destination.
5. **План Б**: диверсификация по обменникам, на случай если Cifra сама заблокирует вывод.

## Ключевые источники

- [EU 20th Sanctions Package — TRM Labs](https://www.trmlabs.com/resources/blog/eu-adopts-20th-sanctions-package-on-russia----including-a-sweeping-ban-on-all-crypto-asset-transactions-with-russian-and-belarusian-providers)
- [Chainalysis: EU's 20th Russia Sanctions Package](https://www.chainalysis.com/blog/eu-russia-sactions-package-april-2026/)
- [Elliptic: 20th package targets crypto evasion architecture](https://www.elliptic.co/blog/eu-20th-sanctions-package-targets-the-architecture-of-crypto-sanctions-evasion)
- [Council of the EU — пресс-релиз 20-го пакета](https://www.consilium.europa.eu/en/press/press-releases/2026/04/23/russia-s-war-of-aggression-against-ukraine-20th-round-of-stern-eu-sanctions-hits-energy-military-industrial-complex-trade-and-financial-services-including-crypto/)
- [Cifra Markets review (crypto.news)](https://crypto.news/cifra-markets-review-a-regulated-gateway-to-crypto-trading/)
- [Tether заморозил USDT на Garantex (1tab.co)](https://1tab.co/ru/blog/tether-blocked-usdt-2025/)
- Исходный пост Першикова: https://t.me/viktor_pershikov/10268
