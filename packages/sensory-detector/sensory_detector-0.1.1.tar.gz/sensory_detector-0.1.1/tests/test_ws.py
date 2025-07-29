import pytest
import cv2
import numpy as np
import asyncio
import websockets
import json

WS_URL = "ws://localhost:8000/ws/analyze?model_name=yolov8s"

@pytest.mark.asyncio
async def test_ws_analyze_image():
    # Сгенерируем тестовый кадр в памяти
    img = np.zeros((128, 128, 3), np.uint8)
    cv2.putText(img, "ws", (10, 64), cv2.FONT_HERSHEY_SIMPLEX, 2, (255,255,255), 3)
    _, jpg = cv2.imencode(".jpg", img)
    jpg_bytes = jpg.tobytes()

    async with websockets.connect(WS_URL, max_size=4_000_000) as ws:
        await ws.send(jpg_bytes)
        resp = await ws.recv()
        data = json.loads(resp)
        assert "detections" in data
        assert "index" in data
        assert data["index"] == 0

        # Отправим еще один кадр
        await ws.send(jpg_bytes)
        resp2 = await ws.recv()
        data2 = json.loads(resp2)
        assert data2["index"] == 1

        # Закроем соединение
        await ws.close()

@pytest.mark.asyncio
async def test_ws_analyze_video():
    # Можно отправлять кадры из видео
    video_path = r"X:\CODER\Yolo\tests\data\screen.avi"
    cap = cv2.VideoCapture(video_path)
    async with websockets.connect(WS_URL, max_size=8_000_000) as ws:
        idx = 0
        while idx < 3:
            ret, frame = cap.read()
            if not ret:
                break
            _, jpg = cv2.imencode(".jpg", frame)
            await ws.send(jpg.tobytes())
            resp = await ws.recv()
            data = json.loads(resp)
            assert data["index"] == idx
            assert "detections" in data
            idx += 1
        await ws.close()
    cap.release()