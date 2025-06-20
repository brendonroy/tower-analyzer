import streamlit as st
from PIL import Image
from PIL.ExifTags import TAGS, GPSTAGS
import math
import io

def get_exif_data(image):
    exif_data = {}
    info = image._getexif()
    if info:
        for tag, value in info.items():
            decoded = TAGS.get(tag, tag)
            if decoded == "GPSInfo":
                gps_data = {}
                for t in value:
                    sub_decoded = GPSTAGS.get(t, t)
                    gps_data[sub_decoded] = value[t]
                exif_data["GPSInfo"] = gps_data
            else:
                exif_data[decoded] = value
    return exif_data

def convert_to_degrees(value):
    d, m, s = value
    return d + (m / 60.0) + (s / 3600.0)

def extract_gps_info(gps_info):
    lat = lon = alt = None
    if "GPSLatitude" in gps_info and "GPSLatitudeRef" in gps_info:
        lat = convert_to_degrees([float(x) for x in gps_info["GPSLatitude"]])
        if gps_info["GPSLatitudeRef"] != "N":
            lat = -lat
    if "GPSLongitude" in gps_info and "GPSLongitudeRef" in gps_info:
        lon = convert_to_degrees([float(x) for x in gps_info["GPSLongitude"]])
        if gps_info["GPSLongitudeRef"] != "E":
            lon = -lon
    if "GPSAltitude" in gps_info:
        alt = float(gps_info["GPSAltitude"])
    return lat, lon, alt

def get_direction(gps_info):
    if "GPSImgDirection" in gps_info:
        try:
            direction = float(gps_info["GPSImgDirection"])
            return direction
        except:
            pass
    return None

def get_pitch(exif_data):
    # Placeholder — EXIF pitch not commonly stored
    return None

# -- Streamlit app --
def main():
    st.title("📷 Tower Image Analyzer")

    uploaded_images = st.file_uploader("Upload image(s)", type=["jpg", "jpeg", "png"], accept_multiple_files=True)

    if uploaded_images:
        for img in uploaded_images:
            image = Image.open(img)
            st.image(image, caption=f"📸 {img.name}", use_column_width=True)

            exif_data = get_exif_data(image)
            gps_info = exif_data.get("GPSInfo", {})

            lat, lon, alt = extract_gps_info(gps_info)
            direction = get_direction(gps_info)
            pitch = get_pitch(exif_data)

            st.markdown("### 📍 Metadata Info")
            st.write("**GPS Coordinates:**")
            st.write(f"Latitude: {lat if lat else 'Not available'}")
            st.write(f"Longitude: {lon if lon else 'Not available'}")
            st.write(f"Altitude: {alt if alt else 'Not available'} m")

            st.write("**Azimuth (compass direction camera is facing):**")
            st.write(f"{direction if direction else 'Not available'}°")

            st.write("**Pitch (vertical tilt up/down):**")
            if pitch is not None:
                st.write(f"{pitch:.2f}°")
            else:
                st.write("Not available in EXIF.")

            # --- Manual pitch input ---
            st.markdown("#### 📐 Enter Pitch (if not in EXIF):")
            pitch_input = st.number_input(f"Pitch angle (degrees) for {img.name}", min_value=0.0, max_value=90.0, step=0.1)

            # --- Manual distance input ---
            st.markdown("#### 📏 Enter Distance to Tower:")
            distance = st.number_input(f"Distance from camera to tower (in meters) for {img.name}", min_value=0.0, step=0.1)

            # --- Height calculation ---
            if pitch_input > 0 and distance > 0:
                pitch_radians = math.radians(pitch_input)
                height = distance * math.tan(pitch_radians)
                st.markdown("#### 📊 Calculated Height on Tower:")
                st.success(f"Estimated height = **{height:.2f} m** above base of tower.")
            else:
                st.info("Enter both pitch and distance to calculate tower height.")

if __name__ == "__main__":
    main()
