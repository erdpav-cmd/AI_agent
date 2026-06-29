import os
from dotenv import load_dotenv
from langchain.agents import create_agent
from langchain_openai import ChatOpenAI
from .tools import (
    web_search, get_weather, get_crypto_price, 
    file_read, file_write, get_fiat_currency_rate, generate_qr_code
)

load_dotenv()

SYSTEM_PROMPT = """Ты — умный и полезный AI-агент.
Ты умеешь искать информацию в интернете, узнавать погоду, курсы криптовалют и фиатных валют,
работать с файлами и генерировать QR-коды.
Всегда используй инструменты для получения точных данных. Отвечай на русском языке."""

def get_agent():
    api_key = os.getenv("PROXYAPI_KEY")
    base_url = os.getenv("PROXYAPI_BASE_URL")
    
    llm = ChatOpenAI(
        model="gpt-4o-mini",
        api_key=api_key,
        base_url=base_url,
        temperature=0
    )
    
    tools = [
        web_search, get_weather, get_crypto_price, 
        file_read, file_write, get_fiat_currency_rate, generate_qr_code
    ]
    
    return create_agent(
        llm,
        tools,
        system_prompt=SYSTEM_PROMPT,
    )