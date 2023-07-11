from typing import Optional
from fastapi import FastAPI
from urllib import parse
import requests

app = FastAPI()
api_key = "RGAPI-f0bf5a5f-6c26-4dd2-a2bd-80f7cf3b047b"
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36",
    "Accept-Language": "ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7,ru;q=0.6",
    "Accept-Charset": "application/x-www-form-urlencoded; charset=UTF-8",
    "Origin": "https://developer.riotgames.com"
}

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/items/{item_id}")
def read_item(item_id: int, q: Optional[str] = None):
    return {"item_id": item_id, "q": q}

@app.get("/accounts/{account_name}")
def get_acc_info(account_name: str):
    url = 'https://kr.api.riotgames.com/tft/summoner/v1/summoners/by-name/' + account_name
    get_info = requests.get(url, headers=headers)

    print(get_info.status_code)
    print(get_info.text)
    print(get_info.json())

@app.get("/server")
def server_status():
    url = f'https://kr.api.riotgames.com/tft/status/v1/platform-data?api_key={api_key}'
    print(url)
    get_info = requests.get(url, headers=headers)

    return get_info.json()