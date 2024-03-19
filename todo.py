from utils import Todo
from pray import current_date_to_json

from starlette.responses import RedirectResponse, JSONResponse, HTMLResponse
from fastapi import Request, APIRouter

router = APIRouter()

DATABASE = Todo("database(sqlite3)/database.db")


@router.get("/todo_today", response_class=JSONResponse)
async def todo():
    try:
        req_to_db = await DATABASE.db_operations(
            f"SELECT id, todo, when_to_do, description FROM todos WHERE when_to_do={current_date_to_json} ORDER BY "
            f"when_to_do"
        )
        all_todos = [
            {"id": x[0], "todo": x[1], "when_to_do": x[2], "description": x[3]}
            for x in req_to_db
        ]
        if len(all_todos) > 0:
            context = {
                "all_todos": all_todos,
                "date": current_date_to_json,
                "empty": "",
            }
            return context
        return None
    except Exception as e:
        return {"error": str(e)}


@router.get("/todos", response_class=JSONResponse)
async def todos():
    req_to_db = await DATABASE.db_operations(
        "SELECT id, todo, when_to_do, description FROM todos ORDER BY when_to_do"
    )
    all_todos = [
        {"id": x[0], "todo": x[1], "when_to_do": x[2], "description": x[3]}
        for x in req_to_db
    ]

    return {"all_todos": all_todos}


@router.post("/todo_create", response_class=JSONResponse)
async def todo_create(request: Request):
    form = await request.form()
    todo = form.get("todo").strip()
    date = form.get("date")
    description = form.get("description").strip()

    if date < current_date_to_json:
        return {
            "error": "Дата не должна быть раньше сегодняшнего дня",
        }

    # Защита от спама (пробелы или пустые строки...)
    if len(todo) <= 0 or len(date) <= 0:
        print(todo, date)
        return {
            "error": "Пожалуйста заполните поля!",
        }
    try:
        await DATABASE.db_operations(
            "INSERT INTO todos(todo, when_to_do, description) VALUES (?, ?, ?)",
            value=(todo, date, description),
        )
        return {
            "success": 201,
        }
    except Exception as e:
        return {
            "error": f"Неправильные данные! {str(e)}",
        }


@router.post("/todos/{pk}", response_class=JSONResponse)
async def delete_todo(pk):
    try:
        await DATABASE.db_operations("DELETE FROM todos WHERE id = ?", pk=(pk,))
        return {
            "success": 200,
        }
    except Exception as e:
        return {
            "error": f"Ошибка при удалении! {str(e)}",
        }
