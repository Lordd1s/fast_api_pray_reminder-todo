# uvicorn main:app --reload --host=0.0.0.0 --port=8000
# http://127.0.0.1:8000/

from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.responses import HTMLResponse

from routers import pray
from routers import todo

app = FastAPI(debug=True)
# app.mount("/frontend/src", StaticFiles(directory="assets"), name="assets") # dist
templates = Jinja2Templates(directory="frontend")

app.include_router(todo.router)
app.include_router(pray.router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get('/', response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse('index.html', {"request": request})
