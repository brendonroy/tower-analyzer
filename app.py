import streamlit as st
import tensorflow as tf
import numpy as np
import os
import shutil
from PIL import Image
from tensorflow.keras.preprocessing.image import img_to_array

# Load model and set class names
model = tf.keras.models.load_model("trained_model.keras")
class_names = ["pinwheel", "non_pinwheel"]
confidence_threshold = 0.6

# Streamlit UI
st.title("Pinwheel Image Classifier")
st.write("Upload one or more images to classify them as pinwheel or non-pinwheel.")

uploaded_files = st.file_uploader("Upload Images", type=["jpg", "jpeg", "png"], accept_multiple_files=True)

if uploaded_files:
    for uploaded_file in uploaded_files:
        # Read and preprocess image
        image = Image.open(uploaded_file).convert("RGB")
        image_resized = image.resize((64, 64))
        img_array = img_to_array(image_resized) / 255.0
        img_array = np.expand_dims(img_array, axis=0)

        # Predict
        prediction = model.predict(img_array)
        confidence = float(np.max(prediction))
        predicted_label = class_names[np.argmax(prediction)]

        # Display
        st.image(image, caption=f"{uploaded_file.name}", width=200)
        st.write(f"**Prediction:** {predicted_label}")
        st.write(f"**Confidence:** {confidence:.2f}")

        # Save to folders if you want
        if confidence >= confidence_threshold:
            folder = predicted_label
        elif confidence <= 1 - confidence_threshold:
            folder = class_names[1 - np.argmax(prediction)]
        else:
            folder = "unsure"

        # Save image
        os.makedirs(folder, exist_ok=True)
        image.save(os.path.join(folder, uploaded_file.name))
        st.write(f"Image saved to **{folder}/** folder.")
