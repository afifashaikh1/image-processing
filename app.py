import streamlit as st
import cv2
import numpy as np
from PIL import Image
from io import BytesIO

# 🌸 Page config
st.set_page_config(page_title="Image Filter App", page_icon="🎀", layout="centered")

# 💅 Custom CSS for soft pink UI
st.markdown("""
    <style>
    body {
        background-color: #fff0f5;
    }
    .stApp {
        background-color: #fff0f5;
    }
    h1, h2, h3, h4 {
        color: #880e4f !important;
        font-weight: bold;
    }
    .element-container:has(.stFileUploader), 
    .element-container:has(.stCameraInput) {
        min-height: 300px;
        display: flex;
        align-items: center;
        justify-content: center;
    }
    label, .stMarkdown, .stRadio > div {
        color: #880e4f !important;
        font-weight: 600;
    }
    </style>
""", unsafe_allow_html=True)

# 🎀 Title
st.markdown("<h1 style='text-align: center;'>💗 Sweet Image Editor</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color:#cc3366;'>Apply pretty filters & effects on your photos!</p><hr>", unsafe_allow_html=True)

# 📤 Upload or capture image
st.markdown("### 📷 Upload or Capture Image")
img = None
upload_col, camera_col = st.columns(2)

with upload_col:
    uploaded_file = st.file_uploader("Upload Image", type=["jpg", "jpeg", "png"])

with camera_col:
    camera_image = st.camera_input("Take a Photo")

if uploaded_file:
    image = Image.open(uploaded_file)
    img = np.array(image)
elif camera_image:
    image = Image.open(camera_image)
    img = np.array(image)

if img is not None:
    st.markdown("### 🖼️ Original Image")
    st.image(img, use_column_width=True)

    st.markdown("### 🎨 Choose a Filter")
    filter_option = st.selectbox("", [
        "Grayscale",
        "Blur",
        "Edge Detection",
        "Cartoon Effect",
        "Negative",
        "Zoom In (1.5x)"
    ])

    processed_img = img.copy()

    # 🧠 Processing
    if filter_option == "Grayscale":
        processed_img = cv2.cvtColor(processed_img, cv2.COLOR_BGR2GRAY)

    elif filter_option == "Blur":
        processed_img = cv2.GaussianBlur(processed_img, (15, 15), 0)

    elif filter_option == "Edge Detection":
        gray = cv2.cvtColor(processed_img, cv2.COLOR_BGR2GRAY)
        processed_img = cv2.Canny(gray, 100, 200)

    elif filter_option == "Cartoon Effect":
        gray = cv2.cvtColor(processed_img, cv2.COLOR_BGR2GRAY)
        gray = cv2.medianBlur(gray, 5)
        edges = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C,
                                      cv2.THRESH_BINARY, 9, 9)
        color = cv2.bilateralFilter(processed_img, 9, 250, 250)
        processed_img = cv2.bitwise_and(color, color, mask=edges)

    elif filter_option == "Negative":
        processed_img = cv2.bitwise_not(processed_img)

    elif filter_option == "Zoom In (1.5x)":
        height, width = processed_img.shape[:2]
        centerX, centerY = int(width / 2), int(height / 2)
        radiusX, radiusY = int(width / 3), int(height / 3)
        minX, maxX = centerX - radiusX, centerX + radiusX
        minY, maxY = centerY - radiusY, centerY + radiusY
        cropped = processed_img[minY:maxY, minX:maxX]
        processed_img = cv2.resize(cropped, (width, height), interpolation=cv2.INTER_LINEAR)

    # 🖼️ Show processed
    st.markdown("### ✅ Processed Image")

    if len(processed_img.shape) == 2:
        st.image(processed_img, use_column_width=True)
    else:
        rgb_img = cv2.cvtColor(processed_img, cv2.COLOR_BGR2RGB)
        st.image(rgb_img, use_column_width=True)

    # 💾 Download section
    st.markdown("### 📥 Download")

    if len(processed_img.shape) == 2:
        result = Image.fromarray(processed_img)
    else:
        rgb_img = cv2.cvtColor(processed_img, cv2.COLOR_BGR2RGB)
        result = Image.fromarray(rgb_img)

    buf = BytesIO()
    result.save(buf, format="PNG")
    byte_im = buf.getvalue()

    st.download_button(
        label="⬇️ Download Image",
        data=byte_im,
        file_name="processed_image.png",
        mime="image/png"
    )
else:
    st.markdown("<h4 style='color:#cc3366;'>⚠️ Please upload or capture an image to continue.</h4>", unsafe_allow_html=True)
