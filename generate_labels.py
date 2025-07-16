import os
import json

DATA_DIR = "labeled_data"
OUTPUT_FILE = "image_labels.json"

image_data = []

# Go through each class folder (e.g. pinwheel, non_pinwheel)
for label in os.listdir(DATA_DIR):
    label_dir = os.path.join(DATA_DIR, label)
    if os.path.isdir(label_dir):
        for filename in os.listdir(label_dir):
            if filename.lower().endswith(('.jpg', '.jpeg', '.png')):
                image_data.append({
                    "filename": os.path.join(label, filename),
                    "label": label
                })

# Save to a JSON file
with open(OUTPUT_FILE, "w") as f:
    json.dump(image_data, f, indent=4)

print(f"Saved {len(image_data)} labeled images to {OUTPUT_FILE}")
