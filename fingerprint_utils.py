import os
import cv2
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

FINGERPRINTS_DIR = "fingerprints"
os.makedirs(FINGERPRINTS_DIR, exist_ok=True)

def extract_fingerprint(video_path):
    cap = cv2.VideoCapture(video_path)
    fingerprints = []

    while True:
        ret, frame = cap.read()
        if not ret:
            break
        resized = cv2.resize(frame, (32, 32))
        mean_color = resized.mean(axis=(0, 1))  # RGB متوسط
        fingerprints.append(mean_color)

    cap.release()
    return np.array(fingerprints)

def save_fingerprint(video_id, fingerprint):
    path = os.path.join(FINGERPRINTS_DIR, f"{video_id}.npy")
    np.save(path, fingerprint)

def is_duplicate(new_fingerprint, threshold=0.1):
    for filename in os.listdir(FINGERPRINTS_DIR):
        old_fp = np.load(os.path.join(FINGERPRINTS_DIR, filename))
        min_len = min(len(new_fingerprint), len(old_fp))
        sim = cosine_similarity(
            new_fingerprint[:min_len].reshape(1, -1),
            old_fp[:min_len].reshape(1, -1)
        )[0][0]
        if sim > (1 - threshold):
            return True
    return False
