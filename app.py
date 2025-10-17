import streamlit as st
import cv2
import numpy as np
from PIL import Image

st.title("🖼️ Image Processing Web App")

uploaded_file = st.file_uploader("Upload an Image", type=["jpg", "png", "jpeg"])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    img_array = np.array(image)
    
    st.image(image, caption='Original Image', use_container_width=True)
    
    option = st.selectbox(
        "Choose Processing Technique",
        ("Grayscale", "Blur", "Edge Detection", "Sharpen")
    )
    
    if option == "Grayscale":
        processed = cv2.cvtColor(img_array, cv2.COLOR_BGR2GRAY)
        st.image(processed, caption="Grayscale Image", use_container_width=True)
        
    elif option == "Blur":
        processed = cv2.GaussianBlur(img_array, (15,15), 0)
        st.image(processed, caption="Blurred Image", use_container_width=True)
        
    elif option == "Edge Detection":
        gray = cv2.cvtColor(img_array, cv2.COLOR_BGR2GRAY)
        processed = cv2.Canny(gray, 100, 200)
        st.image(processed, caption="Edges Detected", use_container_width=True)
        
    elif option == "Sharpen":
        kernel = np.array([[0,-1,0], [-1,5,-1], [0,-1,0]])
        processed = cv2.filter2D(img_array, -1, kernel)
        st.image(processed, caption="Sharpened Image", use_container_width=True)
    
    st.download_button(
        label="Download Processed Image",
        data=cv2.imencode('.png', processed)[1].tobytes(),
        file_name="processed_image.png",
        mime="image/png"
    )
