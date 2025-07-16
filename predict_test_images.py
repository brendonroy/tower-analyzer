import os
import numpy as np
from PIL import Image
from tensorflow.keras.models import load_model
import shutil

# --- Settings ---
IMAGE_SIZE = (64, 64)  # Match model input size
TEST_DIR = "test_data"
MODEL_PATH = "trained_model.keras"
OUTPUT_DIR = "predicted"

# --- Load model ---
model = load_model(MODEL_PATH)

# --- Make sure output folders exist ---
os.makedirs(os.path.join(OUTPUT_DIR, "pinwheel"), exist_ok=True)
os.makedirs(os.path.join(OUTPUT_DIR, "non-pinwheel"), exist_ok=True)

# --- Loop through test images ---
for filename in os.listdir(TEST_DIR):
    if not filename.lower().endswith((".png", ".jpg", ".jpeg")):
        continue

    filepath = os.path.join(TEST_DIR, filename)

    try:
        # Load and preprocess image
        image = Image.open(filepath).convert("RGB")  # Ensure 3 channels
        image = image.resize(IMAGE_SIZE)
        img_array = np.array(image) / 255.0
        img_array = np.expand_dims(img_array, axis=0)  # Shape: (1, 64, 64, 3)

        # Predict
        prediction = model.predict(img_array)[0][0]
        predicted_label = "pinwheel" if prediction >= 0.5 else "non-pinwheel"

        # Print result
        print(f"{filename} → {predicted_label} ({prediction:.2f})")

        # Move to appropriate folder
        dest_path = os.path.join(OUTPUT_DIR, predicted_label, filename)
        shutil.copy(filepath, dest_path)

    except Exception as e:
        print(f"Error processing {filename}: {e}")
