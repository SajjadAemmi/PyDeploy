import streamlit as st
import cv2
from PIL import Image
import numpy as np


st.title("Image Blur App")

uploaded_file = st.file_uploader("Choose an image...", type=['jpg', 'jpeg', 'png'])
if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption='Uploaded Image', use_column_width=True)
    st.write("")
    st.write("Processed Image")

    # Convert the image to array and then to OpenCV format
    img_array = np.array(image)
    img = cv2.cvtColor(img_array, cv2.COLOR_RGB2BGR)

    # Slider for setting the blur level
    blur_amount = st.slider("Select the amount of blur", min_value=1, max_value=99, value=5, step=2)

    # Apply a Gaussian blur filter
    kernel_size = (blur_amount, blur_amount)
    blur_img = cv2.blur(img, kernel_size)
    
    # Convert the BGR image to RGB
    blur_img_rgb = cv2.cvtColor(blur_img, cv2.COLOR_BGR2RGB)

    # Convert the OpenCV image to PIL format
    blur_img_pil = Image.fromarray(blur_img_rgb)
    
    # Display the blurred image
    st.image(blur_img_pil, caption='Blurred Image', use_column_width=True)
