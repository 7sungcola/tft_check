from typing import Optional
from fastapi import FastAPI
from urllib import parse
import requests

app = FastAPI()
api_key = "RGAPI-e0f83465-354c-4a91-9014-32861ee64c2e"
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36",
    "Accept-Language": "ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7,ru;q=0.6",
    "Accept-Charset": "application/x-www-form-urlencoded; charset=UTF-8",
    "Origin": "https://developer.riotgames.com",
    "X-Riot-Token": api_key
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

    return get_info.json()

@app.get("/server")
def server_status():
    url = f'https://kr.api.riotgames.com/tft/status/v1/platform-data?api_key={api_key}'     # header에 x-riot-token 키 값을 넣어줬기 때문에 사실상 불필요
    print(url)
    get_info = requests.get(url, headers=headers)

    return get_info.json()

@app.get("/matches/{puuid}")      # get match ids using puuid
def get_puuid(puuid: str):
    url = f'https://asia.api.riotgames.com/tft/match/v1/matches/by-puuid/{puuid}/ids?start=0&count=10'
    get_info = requests.get(url, headers=headers)
    print(url)

    return get_info.json()