import numpy as np
from PIL import Image
import open_clip
import torch
import cv2
from src.sensory_detector.yolo_server.detectors.detector_interface import ModelTaskType

class CLIPWrapper:
    def __init__(self, model_name: str):
        self._model_name = model_name
        self.model, _, self.preprocess = open_clip.create_model_and_transforms(model_name)
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.model = self.model.to(self.device)
    def model_name(self) -> str:
        return self._model_name
    def task_type(self):
        return ModelTaskType.EMBEDDING
    def process_image(self, frame: np.ndarray) -> np.ndarray:
        pil_img = Image.fromarray(frame[..., ::-1])
        img_t = self.preprocess(pil_img).unsqueeze(0).to(self.device)
        with torch.no_grad():
            emb = self.model.encode_image(img_t)
            return emb.cpu().numpy().flatten()
    def process_bytes(self, image_bytes: bytes) -> np.ndarray:
        arr = np.frombuffer(image_bytes, np.uint8)
        img = cv2.imdecode(arr, cv2.IMREAD_COLOR)
        return self.process_image(img)
    def unload(self): pass