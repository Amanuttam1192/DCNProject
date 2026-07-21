import torch
import cv2
from config import CONFIDENCE_THRESHOLD

def load_model():
    """Load YOLOv5s model from torch.hub."""
    print("Loading YOLOv5s model (this may take a few seconds)...")
    model = torch.hub.load('ultralytics/yolov5', 'yolov5s', pretrained=True)
    model.eval()
    return model

def get_elephant_class_id(model):
    """Find class ID for 'elephant'."""
    names = model.names
    for cid, name in names.items():
        if name.lower() == 'elephant':
            return cid
    raise ValueError("Model does not contain 'elephant' class.")

def detect_elephant(frame, model, elephant_id):
    """Detect elephants in the frame. Returns True if detected and draws bounding boxes."""
    results = model(frame)
    detections = results.xyxy[0]
    detected_elephant = False

    for *box, conf, cls in detections.tolist():
        if int(cls) == elephant_id and conf >= CONFIDENCE_THRESHOLD:
            x1, y1, x2, y2 = map(int, box)
            label = f"elephant {conf:.2f}"
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv2.putText(frame, label, (x1, y1 - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)
            detected_elephant = True

    return detected_elephant, frame
