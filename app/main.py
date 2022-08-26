from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
import pathlib

BASE_DIR = pathlib.Path(__file__).parent
app = FastAPI()
templates = Jinja2Templates(directory=str(BASE_DIR / "./templates"))

@app.get("/")
async def root(request: Request):
    return templates.TemplateResponse("home.html", {"request": request})



@app.post("/")
async def root_post():
    return {"message": "Hello World"}