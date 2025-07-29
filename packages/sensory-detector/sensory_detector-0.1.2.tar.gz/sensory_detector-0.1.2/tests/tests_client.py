import asyncio
from src.sensory_detector.yolo_client.client import YOLOAPIClient

async def main():
    client = YOLOAPIClient("http://localhost:8000")

    # Список моделей
    models = await client.get_available_models()
    print("Доступные модели:", models.available_models)

    # Анализ изображения (upload)
    result = await client.analyze_image("data/test.jpg", model_name=models.default_model)
    print(result.model_dump())

    # Анализ видео (upload)
    video_result = await client.analyze_video_upload("data/screen.avi", model_name=models.default_model)
    print(video_result.model_dump())

    # Анализ по серверному пути
    path_result = await client.analyze_by_path("data/screen.avi", model_name=models.default_model)
    print(path_result.model_dump())

if __name__ == "__main__":
    asyncio.run(main())