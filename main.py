# uvicorn main:app --reload --host=0.0.0.0 --port=8000
# http://127.0.0.1:8000/
import asyncio
from datetime import datetime, timedelta
import json
from pathlib import Path

import jinja2
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.responses import RedirectResponse

from utils import Parse, Todo

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

origins = [
    "http://localhost",
    "http://localhost:8080/",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

DATABASE = Todo("database(sqlite3)/database.db")

# Parse.dump_api(response_obj='https://namaz.muftyat.kz/kk/api/times/2023/51.133333/71.433333',
# file_name_path="city_api/astana_time.json")

date_today: str = datetime.today().strftime("%d.%m.%Y")
current_date_to_json: str = datetime.today().strftime("%Y-%m-%d")


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    data = await Parse.load_api(file_path_name="city_api/Астана.json")
    cities = await Parse.load_api(file_path_name="city_api/cities.json")
    values = data["result"]
    for item in values:
        if item["Date"] == current_date_to_json:
            context = {
                "request": request,
                "times": item,
                "date": date_today,
                "city": data["city"],
                "cities": cities["results"],
                "time_to_js": current_date_to_json,
            }
            return templates.TemplateResponse("home.html", context=context)


@app.post("/city", response_class=HTMLResponse)
async def get_city_time(request: Request):
    form = await request.form()
    search = form.get("search")
    path = Path("city_api/cities.json")
    data = await Parse.load_api(file_path_name=path)

    # Проверка на пустой поисковый запрос
    if not search:
        return "404 Error Not Found!!!"

    api_path = f"city_api/{search}.json"

    # Проверка на наличие файлов с данными API
    if not Path(api_path).exists():
        # Если файл не существует, загружаем данные API для указанного города
        for city in data["results"]:
            if search == city["title"]:
                await Parse.dump_api(
                    response_obj=f'https://api.muftyat.kz/prayer-times/2023/{city["lat"]}/{city["lng"]}',
                    file_name_path=api_path,
                )

    # Загрузка данных API для указанного города
    current_city_api = await Parse.load_api(file_path_name=api_path)

    # Поиск данных о времени для текущей даты
    for item in current_city_api["result"]:
        if item["Date"] == current_date_to_json:
            # Формирование контекста для передачи в шаблон
            context = {
                "request": request,
                "times": item,
                "date": date_today,
                "city": search,
                "time_to_js": current_date_to_json,
            }
            # Определение имени шаблона в зависимости от имени файла API
            template_name = (
                "city.html" if api_path.endswith(search + ".json") else "home.html"
            )
            return templates.TemplateResponse(template_name, context=context)


@app.get("/todos", response_class=HTMLResponse)
async def todos(request: Request):
    req_to_db = DATABASE.db_operations(
        "SELECT id, todo, when_to_do, description FROM todos ORDER BY when_to_do"
    )
    all_todos = [
        {"id": x[0], "todo": x[1], "when_to_do": x[2], "description": x[3]}
        for x in req_to_db
    ]
    return templates.TemplateResponse(
        name="todo.html",
        context={
            "request": request,
            "all_todos": all_todos,
            "date": current_date_to_json,
            "empty": "",
        },
    )


@app.post("/todos", response_class=RedirectResponse)
async def todo_create(request: Request):
    form = await request.form()
    todo = form.get("todo").strip()
    date = form.get("date")
    description = form.get("description").strip()

    if date < current_date_to_json:
        return templates.TemplateResponse(
            name="todo.html",
            context={
                "request": request,
                "error": "Дата не должна быть раньше сегодняшнего дня",
            },
        )

    # Защита от спама (пробелы или пустые строки...)
    if len(todo) <= 0 or len(date) <= 0:
        print(todo, date)
        return templates.TemplateResponse(
            name="todo.html",
            context={
                "request": request,
                "error": "Пожалуйста заполните нужные поля!",
            },
        )

    DATABASE.db_operations(
        "INSERT INTO todos(todo, when_to_do, description) VALUES (?, ?, ?)",
        value=(todo, date, description),
    )
    return RedirectResponse("/todos", status_code=303)


@app.post("/todos/{pk}", response_class=RedirectResponse)
async def delete_todo(request: Request, pk):
    DATABASE.db_operations("DELETE FROM todos WHERE id = ?", pk=(pk,))
    return RedirectResponse("/todos", status_code=303)


if __name__ == "__main__":
    print(current_date_to_json)
