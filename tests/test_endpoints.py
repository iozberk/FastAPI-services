
from http import client
from fastapi.testclient import TestClient
from app.main import app, BASE_DIR
import shutil, time

client = TestClient(app)


from importlib.metadata import files


def test_echo_upload():
    img_saved_path = BASE_DIR / "images"
    for path in img_saved_path.glob('*'):
        # path = list(BASE_DIR / 'images').glob('*')[0]
        res = client.post("/img-echo/",files={"file": open(path, 'rb')})
        assert res.status_code == 200
    