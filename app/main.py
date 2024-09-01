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

app.include_router(todo.router)
app.include_router(pray.router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # change this to environment variable
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
