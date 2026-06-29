# AI Agent — Telegram-бот с инструментами

Telegram-бот на базе LangChain и GPT-4o-mini. Агент сам выбирает нужные инструменты: ищет в интернете, проверяет погоду и курсы валют, работает с файлами и генерирует QR-коды.

## Возможности

| Инструмент | Описание |
|---|---|
| `web_search` | Поиск информации в интернете (DuckDuckGo) |
| `get_weather` | Текущая погода в любом городе |
| `get_crypto_price` | Курс криптовалют (CoinGecko) |
| `get_fiat_currency_rate` | Курс фиатных валют |
| `file_read` / `file_write` | Чтение и запись файлов |
| `generate_qr_code` | Генерация QR-кодов |

## Стек

- **Python 3.11+**
- **LangChain 1.x** — агент с вызовом инструментов (`create_agent`)
- **OpenAI API** через [ProxyAPI](https://proxyapi.ru/)
- **pyTelegramBotAPI** (`telebot`) — Telegram-интерфейс

## Структура проекта

```
AI_agent/
├── agent/
│   ├── agent.py      # Сборка агента и системный промпт
│   └── tools.py      # Инструменты агента
├── memory/           # История диалогов (по chat_id)
├── bot.py            # Логика Telegram-бота
├── run.py            # Точка входа
├── requirements.txt
├── .env.example
└── README.md
```

## Установка

1. Клонируйте репозиторий и перейдите в папку проекта.

2. Создайте виртуальное окружение:

```bash
python -m venv .venv
```

3. Активируйте окружение:

```bash
# Windows (PowerShell)
.venv\Scripts\Activate.ps1

# Linux / macOS
source .venv/bin/activate
```

4. Установите зависимости:

```bash
pip install -r requirements.txt
```

## Настройка

Скопируйте `.env.example` в `.env` и заполните переменные:

```env
# Токен от @BotFather в Telegram
BOT_TOKEN=your_telegram_bot_token

# Ключ и URL ProxyAPI (OpenAI-совместимый API)
PROXYAPI_KEY=your_proxyapi_key
PROXYAPI_BASE_URL=https://api.proxyapi.ru/openai/v1
```

### Как получить токен бота

1. Откройте [@BotFather](https://t.me/BotFather) в Telegram.
2. Отправьте `/newbot` и следуйте инструкциям.
3. Скопируйте выданный токен в `BOT_TOKEN`.

## Запуск

```bash
python run.py
```

После запуска напишите боту в Telegram. Остановка — `Ctrl+C` в терминале.

## Команды бота

| Команда | Описание |
|---|---|
| `/start` | Приветствие и краткая справка |
| `/clear` | Очистить историю текущего диалога |

Любое текстовое сообщение обрабатывается агентом. Ответы приходят на русском языке.

## Примеры запросов

- «Какая погода в Москве?»
- «Курс биткоина в долларах»
- «Сколько стоит 1 USD в рублях?»
- «Найди последние новости про Python»
- «Сгенерируй QR-код для https://example.com»
- «Запиши в файл notes.txt: купить молоко»

## Память

История каждого чата сохраняется в `memory/{chat_id}.json`. При перезапуске бота контекст в рамках сессии сбрасывается, но архив сообщений остаётся в файлах.

## Лицензия

Учебный проект. Используйте на своё усмотрение.
