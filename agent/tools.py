import os
import json
import requests
import qrcode
from datetime import datetime
from ddgs import DDGS
from geopy.geocoders import Nominatim
from langchain.tools import tool

# --- БАЗОВЫЕ ИНСТРУМЕНТЫ ---

@tool
def web_search(query: str) -> str:
    """Поиск актуальной информации в интернете через DuckDuckGo."""
    try:
        with DDGS() as ddgs:
            results = [r for r in ddgs.text(query, max_results=5)]
            return "\n".join([f"{r['title']}: {r['body']}" for r in results])
    except Exception as e:
        return f"Ошибка поиска: {e}"

@tool
def get_weather(city: str) -> str:
    """Получить текущую погоду в указанном городе."""
    try:
        geolocator = Nominatim(user_agent="my_agent")
        location = geolocator.geocode(city)
        if not location:
            return "Город не найден."
        
        lat, lon = location.latitude, location.longitude
        url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current_weather=true"
        response = requests.get(url).json()
        weather = response.get("current_weather", {})
        return f"Погода в {city}: Температура {weather.get('temperature')}°C, Скорость ветра {weather.get('windspeed')} км/ч."
    except Exception as e:
        return f"Ошибка получения погоды: {e}"

@tool
def get_crypto_price(coin: str, currency: str = "usd") -> str:
    """Узнать курс криптовалюты (например, bitcoin, ethereum) в выбранной валюте."""
    try:
        url = f"https://api.coingecko.com/api/v3/simple/price?ids={coin}&vs_currencies={currency}"
        response = requests.get(url).json()
        if coin in response:
            price = response[coin].get(currency, "N/A")
            return f"Курс {coin}: {price} {currency.upper()}."
        return "Криптовалюта не найдена."
    except Exception as e:
        return f"Ошибка получения курса крипты: {e}"

@tool
def file_read(file_path: str) -> str:
    """Прочитать текст из файла по указанному пути."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()
    except Exception as e:
        return f"Ошибка чтения файла: {e}"

@tool
def file_write(file_path: str, content: str) -> str:
    """Записать текст в файл по указанному пути."""
    try:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        return f"Файл {file_path} успешно сохранен."
    except Exception as e:
        return f"Ошибка записи файла: {e}"

# --- ДОПОЛНИТЕЛЬНЫЕ ИНСТРУМЕНТЫ (ДЗ) ---

@tool
def get_fiat_currency_rate(base_currency: str, target_currency: str) -> str:
    """Узнать курс фиатной валюты (например, USD к RUB или EUR к USD)."""
    try:
        url = f"https://api.exchangerate-api.com/v4/latest/{base_currency.upper()}"
        response = requests.get(url).json()
        rate = response.get("rates", {}).get(target_currency.upper())
        if rate:
            return f"1 {base_currency.upper()} равен {rate} {target_currency.upper()}."
        return "Валюта не найдена или неверный код."
    except Exception as e:
        return f"Ошибка получения курса валюты: {e}"

@tool
def generate_qr_code(data: str, filename: str = "qrcode.png") -> str:
    """Сгенерировать QR-код для текста или ссылки и сохранить его в файл."""
    try:
        img = qrcode.make(data)
        img.save(filename)
        return f"QR-код успешно создан и сохранен как {filename}."
    except Exception as e:
        return f"Ошибка генерации QR-кода: {e}"