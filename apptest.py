# Requirements:
# pip install ultralytics opencv-python-headless deepface torch torchvision

import cv2
import torch
import numpy as np
from ultralytics import YOLO
from deepface import DeepFace
from collections import deque

# Load models
person_detector = YOLO('yolov8n.pt')  # Lightweight YOLOv8 model
reference_img = cv2.imread("reference.jpg")  # Replace with your target person's image

# Precompute embedding for target person
reference_embedding = DeepFace.represent(img_path="reference.jpg", model_name="Facenet", enforce_detection=False)[0]["embedding"]

# Tracking buffer
recent_target_box = deque(maxlen=1)

# Video capture
cap = cv2.VideoCapture(0)

# Cosine similarity function
def cosine_similarity(a, b):
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Detect persons in the frame
    results = person_detector(frame)
    boxes = results[0].boxes.xyxy.cpu().numpy()
    confidences = results[0].boxes.conf.cpu().numpy()
    classes = results[0].boxes.cls.cpu().numpy()

    best_match = None
    best_sim = -1

    for i, box in enumerate(boxes):
        if int(classes[i]) != 0:  # class 0 is 'person'
            continue

        x1, y1, x2, y2 = map(int, box)
        person_crop = frame[y1:y2, x1:x2]

        try:
            emb = DeepFace.represent(img_path=person_crop, model_name="Facenet", enforce_detection=False)[0]["embedding"]
            sim = cosine_similarity(reference_embedding, emb)
            if sim > best_sim:
                best_sim = sim
                best_match = (x1, y1, x2, y2)
        except:
            continue

    if best_match:
        recent_target_box.append(best_match)

    if recent_target_box:
        x1, y1, x2, y2 = recent_target_box[-1]
        # Draw highlight box around the target person
        cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
        cv2.putText(frame, "Target", (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)

    cv2.imshow("Live Instance-Specific Segmentation (Demo)", frame)
    if cv2.waitKey(1) == 27:
        break

cap.release()
cv2.destroyAllWindows()
