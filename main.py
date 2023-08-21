import requests, time

from fastapi import FastAPI, Request, Form
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
api_key = "RGAPI-90120bf3-1f8f-4bef-8639-6db419e8d5c9"
templates = Jinja2Templates(directory="templates")

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36",
    "Accept-Language": "ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7,ru;q=0.6",
    "Accept-Charset": "application/x-www-form-urlencoded; charset=UTF-8",
    "Origin": "https://developer.riotgames.com",
    "X-Riot-Token": api_key
}
@app.get("/", response_class=HTMLResponse)      # main page with nickname search
async def search_nickname(request: Request):
    return templates.TemplateResponse("main.html", {"request" : request})

@app.post("/accounts/{account_name}", response_class=HTMLResponse)        # get account info using nickname
async def get_acc_info(request: Request, account_name: str):
    url = 'https://kr.api.riotgames.com/tft/summoner/v1/summoners/by-name/' + account_name
    get_info = requests.get(url, headers=headers)
    puuid = get_info.json()['puuid']
    profile_icon = get_info.json()['profileIconId']
    name_list = []

    match_list = get_match_ids(puuid)
    latest_match = match_list[0]
    for i in range(len(match_list)):
        name_list.append(get_match_participants(match_list[i]))

    leagueid = get_info.json()['id']
    tier_rank = get_summoner_tier(leagueid)
    tier = tier_rank.split()[0]
    rank = tier_rank.split()[1]

    result = {
        "request" : request,
        "nickname" : account_name,
        "tier" : tier,
        "rank" : rank,
        "profile_icon" : profile_icon,
        "name_list" : name_list
    }

    return templates.TemplateResponse("info.html", result)

@app.get("/server")     # check current server status
def server_status():
    url = f'https://kr.api.riotgames.com/tft/status/v1/platform-data?api_key={api_key}'     # header에 x-riot-token 키 값을 넣어줬기 때문에 사실상 불필요
    get_info = requests.get(url, headers=headers)

    return get_info.json()

@app.get("/matches/by-puuid/{puuid}")      # get match ids using puuid
def get_match_ids(puuid: str):
    url = f'https://asia.api.riotgames.com/tft/match/v1/matches/by-puuid/{puuid}/ids?start=0&count=5'
    get_info = requests.get(url, headers=headers)

    return get_info.json()

@app.get("/matches/{matchid}")      # get participants of the match using match id
def get_match_participants(matchid: str):

    start = time.time()

    url = f'https://asia.api.riotgames.com/tft/match/v1/matches/{matchid}'
    get_info = requests.get(url, headers=headers)
    info = get_info.json()
    participants = info['info']['participants']
    name_list = []

    for i in range(len(participants)):
        name_list.append(get_summoner_name(participants[i]['puuid']))

    end = time.time()

    print(end - start)

    return name_list

@app.get("/summoners/name/{puuid}")      # get summoner's name using puuid
def get_summoner_name(puuid: str):
    url = f'https://kr.api.riotgames.com/tft/summoner/v1/summoners/by-puuid/{puuid}'
    get_info = requests.get(url, headers=headers)
    name = get_info.json()['name']

    return name

################################ APIs


# get summoner's tier and rank
def get_summoner_tier(leagueid: str):
    url = f'https://kr.api.riotgames.com/tft/league/v1/entries/by-summoner/{leagueid}'
    get_info = requests.get(url, headers=headers)
    tier = get_info.json()[0]['tier']
    rank = get_info.json()[0]['rank']

    return tier + " " + rank