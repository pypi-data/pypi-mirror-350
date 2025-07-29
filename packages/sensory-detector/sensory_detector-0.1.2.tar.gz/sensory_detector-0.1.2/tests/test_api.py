import os
import pytest
import httpx
from pathlib import Path

API_URL = "http://localhost:8000"
IMG_PATH = "tests/data/test.jpg"  # PNG или JPG (можно сгенерировать)
VIDEO_PATH = r"X:\CODER\Yolo\tests\data\screen.avi"  # Абсолютный путь (должен быть доступен сервису)
DEFAULT_MODEL = os.environ.get("DEFAULT_MODEL_NAME", "yolov8s")

@pytest.fixture(scope="session")
def client():
    with httpx.Client(base_url=API_URL, timeout=30.0) as c:
        yield c

def test_healthz(client):
    r = client.get("/healthz")
    assert r.status_code == 200
    assert "status" in r.json()

def test_available_models(client):
    r = client.get("/api/available_models")
    assert r.status_code == 200
    data = r.json()
    assert "available_models" in data
    assert "default_model" in data

def test_loaded_models(client):
    r = client.get("/api/loaded_models")
    assert r.status_code == 200
    assert isinstance(r.json(), list)

def test_analyze_image_upload(client):
    # Сгенерируем картинку если нет
    if not Path(IMG_PATH).exists():
        import cv2
        import numpy as np
        img = np.zeros((128, 128, 3), np.uint8)
        cv2.putText(img, "test", (10, 64), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,255,255), 2)
        cv2.imwrite(IMG_PATH, img)

    files = {"file": ("data/test.png", open(IMG_PATH, "rb"), "image/jpeg")}
    data = {"model_name": DEFAULT_MODEL}
    r = client.post("/api/analyze/auto", files=files, data=data)
    assert r.status_code == 200
    body = r.json()
    assert "detections" in body

def test_analyze_image_by_path(client):
    # Путь должен быть внутри FILES_PATH!
    # Для теста скопируйте test.png в FILES_PATH или используйте уже имеющийся файл
    test_path = os.environ.get("TEST_IMAGE_IN_FILES_PATH", "data/test.png")
    data = {"path": test_path, "model_name": DEFAULT_MODEL}
    r = client.post("/api/analyze/auto", data=data)
    assert r.status_code == 200
    body = r.json()
    assert "detections" in body

@pytest.mark.skipif(not Path(VIDEO_PATH).exists(), reason="Video file not found")
def test_analyze_video_by_path(client):
    # Аналогично, путь должен быть внутри FILES_PATH
    data = {"path": VIDEO_PATH, "model_name": DEFAULT_MODEL}
    r = client.post("/api/analyze/auto", data=data)
    assert r.status_code == 200
    body = r.json()
    assert "detections" in body
    # Проверим что детекций несколько (для видео)
    assert isinstance(body["detections"], list)
    assert len(body["detections"]) > 0

def test_unload_model(client):
    # Проверим выгрузку модели (после любого анализа она должна быть загружена)
    r = client.delete(f"/api/unload_model/{DEFAULT_MODEL}")
    assert r.status_code == 200
    data = r.json()
    assert "detail" in data