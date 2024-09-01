from database.db import Parse

import asyncio
import json

from datetime import datetime
from pathlib import Path

from starlette.responses import RedirectResponse, JSONResponse, HTMLResponse
from fastapi import Request, APIRouter

router = APIRouter()

date_today: str = datetime.today().strftime("%d.%m.%Y")
current_date_to_json: str = datetime.today().strftime("%Y-%m-%d")

YEAR: str = datetime.today().strftime("%Y")


# Parse.dump_api(response_obj='https://namaz.muftyat.kz/kk/api/times/2023/51.133333/71.433333',
# file_name_path="city_api/astana_time.json")  # example


@router.get("/pray_times", response_class=JSONResponse)
async def pray_times(request: Request):
    try:
        data = await Parse.load_api(file_path_name="city_api/Астана.json")
        cities = await Parse.load_api(file_path_name="city_api/cities.json")
        values = data["result"]
        async for item in values:
            if item["Date"] == current_date_to_json:
                context = {
                    "request": request,
                    "times": item,
                    "date": date_today,
                    "city": data["city"],
                    "cities": cities["results"],
                    "time_to_js": current_date_to_json,
                }
                return context
    except FileNotFoundError as e:
        return {'error': 'File not found! Please try download it manually!'}


@router.post("/city", response_class=JSONResponse)
async def get_city_time(request: Request):
    form = await request.form()
    search = form.get("search")
    path = "city_api/cities.json"
    data = await Parse.load_api(file_path_name=path)

    if not search:
        return "404 Error Not Found!!!"

    api_path = f"city_api/{search}.json"

    # Проверка на наличие файлов с данными API
    if not Path(api_path).exists():
        # Если файл не существует, загружаем данные API для указанного города
        for city in data["results"]:
            if search == city["title"]:
                await Parse.dump_api(
                    response_obj=f'https://api.muftyat.kz/prayer-times/{YEAR}/{city["lat"]}/{city["lng"]}',
                    file_name_path=api_path,
                )

    # Загрузка данных API для указанного города
    current_city_api = await Parse.load_api(file_path_name=api_path)

    # Поиск данных о времени для текущей даты
    for item in current_city_api["result"]:
        if item["Date"] == current_date_to_json:

            context = {
                "request": request,
                "times": item,
                "date": date_today,
                "city": search,
                "time_to_js": current_date_to_json,
            }

            return context