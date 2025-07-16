import os
import shutil
import numpy as np
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
from PIL import Image

# Load the trained model
model = load_model('trained_model.keras')

# Define class names in the same order used during training
class_names = ['non_pinwheel', 'pinwheel']

# Set the confidence threshold for "unsure" classification
confidence_threshold = 0.7

# Folder with new images to classify
input_folder = 'new_images'

# Output folder where images will be organized
output_folder = 'organized_images'
os.makedirs(output_folder, exist_ok=True)

# Preprocessing settings
img_size = (64, 64)  # Update if your model was trained with different size

# Go through each image in the input folder
for img_name in os.listdir(input_folder):
    img_path = os.path.join(input_folder, img_name)

    try:
        # Load and preprocess image
        img = Image.open(img_path).convert("RGB")
        img = img.resize(img_size)
        img_array = image.img_to_array(img)
        img_array = np.expand_dims(img_array, axis=0) / 255.0

        # Predict
        prediction = model.predict(img_array)
        confidence = np.max(prediction)
        predicted_label = class_names[np.argmax(prediction)]

        # Decide folder based on confidence
        if confidence >= confidence_threshold:
            destination_folder = os.path.join(output_folder, predicted_label)
        else:
            destination_folder = os.path.join(output_folder, "unsure")

        os.makedirs(destination_folder, exist_ok=True)
        shutil.move(img_path, os.path.join(destination_folder, img_name))
        print(f"{img_name} → {predicted_label} (confidence: {confidence:.2f})")

    except Exception as e:
        print(f"Failed to process {img_name}: {e}")
