# uvicorn main:app --reload --host=0.0.0.0 --port=8000
# http://127.0.0.1:8000/
import asyncio
from datetime import datetime, timedelta
import json
from pathlib import Path
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.responses import RedirectResponse
import requests

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

class Parse:
    @staticmethod
    def load_api(file_path_name: str):
        """
        params: file_path_name take only ".json" files to read!
        """
        with open(file_path_name, mode="r", encoding='utf-8') as file:
            return json.load(file)

    @staticmethod
    def dump_api(response_obj: str, file_name_path: str):
        """
        This method works only with module "requests"!
        params: file_name_path take only '.json' files!
                      response_obj accepts an object(website) to be parsed!
        """
        head = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36"
        try:
            response = requests.get(url=response_obj, headers={'User-Agent': head}).json()
            with open(file_name_path, mode="w", encoding='utf-8') as file:
                return json.dump(response, file, indent=4, ensure_ascii=False)
        except requests.exceptions.RequestException as e:
            print(f"An error occurred: {e}")
            return False


# Parse.dump_api(response_obj='https://namaz.muftyat.kz/kk/api/times/2023/51.133333/71.433333', file_name_path="city_api/astana_time.json")
date_today: str = datetime.today().strftime("%d-%m-%Y")
current_date_to_json: str = datetime.today().strftime("%Y-%m-%d")


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    data = Parse.load_api(file_path_name="city_api/Астана.json")
    values = data["result"]
    for item in values:
        if item["Date"] == current_date_to_json:
            context = {"request": request, "times": item, "date": date_today, "city": data['city']}
            return templates.TemplateResponse("home.html", context=context)


@app.post("/", response_class=HTMLResponse)
async def get_city_time(request: Request):
    form = await request.form()
    search = form.get('search').capitalize()
    path = Path("city_api/cities.json")
    data = Parse.load_api(file_path_name=path)

    if not Path(f"city_api/{search}.json").exists():
        for city in data["results"]:
            if search == city["title"]:
                Parse.dump_api(response_obj=f'https://api.muftyat.kz/prayer-times/2023/{city["lat"]}/{city["lng"]}', file_name_path=f"city_api/{search}.json")
                current_city_api = Parse.load_api(file_path_name=f"city_api/{search}.json")
                for item in current_city_api["result"]:
                    if item["Date"] == current_date_to_json:
                        context = {"request": request, "times": item, "date": date_today, "city": search}
                        return templates.TemplateResponse("home.html", context=context)

    current_city_api = Parse.load_api(file_path_name=f"city_api/{search}.json")
    for item in current_city_api["result"]:
        print(item["Date"])
        if item["Date"] == current_date_to_json:
            context = {"request": request, "times": item, "date": date_today, "city": search}
            return templates.TemplateResponse("home.html", context=context)






if __name__ == "__main__":
    pass
