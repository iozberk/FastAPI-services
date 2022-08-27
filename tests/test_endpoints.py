import shutil
import time
from fastapi.testclient import TestClient
from app.main import app, BASE_DIR, UPLOAD_DIR

client = TestClient(app)



def test_echo_upload():
    img_saved_path = BASE_DIR / "images"
    for path in img_saved_path.glob("*"):
        response = client.post("/img-echo/", files={"file": open(path, 'rb')})
        assert response.status_code == 200
        fext = path.suffix.replace('.', '')
        assert fext in response.headers['content-type']
    # time.sleep(2)
    shutil.rmtree(UPLOAD_DIR)