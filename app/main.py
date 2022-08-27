from fastapi import FastAPI, Request, Depends, File, UploadFile,HTTPException
from fastapi.templating import Jinja2Templates
import io
import pathlib
import uuid
from functools import lru_cache
from pydantic import BaseSettings
from fastapi.responses import FileResponse

class Settings(BaseSettings):
    debug: bool = False
    echo_active: bool = False

    class Config:
        env_file = ".env"

@lru_cache
def get_settings():
    return Settings()

settings = get_settings()
DEBUG=settings.debug

BASE_DIR = pathlib.Path(__file__).parent
UPLOAD_DIR = BASE_DIR / "uploads"
UPLOAD_DIR.mkdir(exist_ok=True)


app = FastAPI()
templates = Jinja2Templates(directory=str(BASE_DIR / "./templates"))

@app.get("/")
async def home_view(request: Request,settings: Settings() =Depends(get_settings)):
    return templates.TemplateResponse("home.html", {"request": request})

@app.post("/")
async def home_detail_view():
    return {"message": "Hello World"}

@app.post("/img-echo/", response_class=FileResponse)
async def img_echo_view(file: UploadFile = File(...),settings: Settings() =Depends(get_settings)):
    if not settings.echo_active:
        raise HTTPException(status_code=400, detail="Not Found")
    bytes_str = io.BytesIO(await file.read())
    fname = pathlib.Path(file.filename).name
    fext = fname.suffix
    destination = UPLOAD_DIR / f'{uuid.uuid1()}-{fext}'
    with open(str(destination), 'wb') as out:
        out.write(bytes_str.read())
    return destination