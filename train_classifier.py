import os
from PIL import Image
import numpy as np
import tensorflow as tf
from tensorflow.keras import layers, models

# Configuration
IMAGE_SIZE = (64, 64)  # adjust as needed
BATCH_SIZE = 32
EPOCHS = 5
DATA_DIR = 'labeled_data'

# Data containers
X = []
y = []

# Labels must be consistent and numeric
label_map = {'pinwheel': 1, 'non-pinwheel': 0}

# Walk through each label directory
for label_name in os.listdir(DATA_DIR):
    label_dir = os.path.join(DATA_DIR, label_name)
    
    # Skip anything that isn't a directory
    if not os.path.isdir(label_dir):
        continue

    # Loop through each file in the label directory
    for filename in os.listdir(label_dir):
        file_path = os.path.join(label_dir, filename)
        try:
            # Open and preprocess image
            img = Image.open(file_path).convert('RGB')
            img = img.resize(IMAGE_SIZE)
            img_array = np.array(img) / 255.0  # Normalize

            # Store image and corresponding label
            X.append(img_array)
            y.append(label_map[label_name])

        except Exception as e:
            print(f"Skipping {file_path}: {e}")

# Convert to NumPy arrays
X = np.array(X)
y = np.array(y)

# Ensure there's data before training
if len(X) == 0:
    raise ValueError("No images were loaded. Please check your directory paths and contents.")

# Define a basic CNN model
model = models.Sequential([
    layers.Input(shape=(*IMAGE_SIZE, 3)),
    layers.Conv2D(32, (3, 3), activation='relu'),
    layers.MaxPooling2D((2, 2)),
    layers.Conv2D(64, (3, 3), activation='relu'),
    layers.MaxPooling2D((2, 2)),
    layers.Flatten(),
    layers.Dense(64, activation='relu'),
    layers.Dense(1, activation='sigmoid')
])

model.compile(optimizer='adam',
              loss='binary_crossentropy',
              metrics=['accuracy'])

# Train the model
model.fit(X, y, epochs=EPOCHS, batch_size=BATCH_SIZE, validation_split=0.2)

model.save("trained_model.keras")
