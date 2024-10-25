import streamlit as st
import pandas as pd

def calculate_bmi(weight, height):
    return weight / ((height / 100) ** 2)

def get_bmi_category(bmi):
    if bmi < 18.5:
        return "Underweight", "images/underweight.png"
    elif 18.5 <= bmi < 25:
        return "Normal weight", "images/normal.png"
    elif 25 <= bmi < 30:
        return "Overweight", "images/overweight.png"
    else:
        return "Obesity", "images/obesity.png"


with st.sidebar:
    st.write("This is sidebar")

# Set up the title of the app
st.title('BMI Calculator')

# Inputs
weight = st.number_input("Enter your weight (kg):", min_value=1.0, format="%.2f")
height = st.number_input("Enter your height (cm):", min_value=1.0, format="%.2f")

if st.button("Calculate BMI"):
    if height > 0 and weight > 0:
        bmi = calculate_bmi(weight, height)
        category, image_path = get_bmi_category(bmi)

        # Display results
        st.write(f"Your BMI is: {bmi:.2f}")
        st.write(f"Category: {category}")
        st.image(image_path, caption=category)
    else:
        st.error("Please enter valid values for height and weight.")


col1, col2 = st.columns(2)
with col1:
    st.session_state.uploaded_file = st.file_uploader(
        "Image", type=["jpg", "jpeg", "png"])
    btn_upload_image = st.button("Upload image", type='primary')

with col2:
    if st.session_state.uploaded_file is not None:
        st.image(st.session_state.uploaded_file, caption='Uploaded Image')

if btn_upload_image:
    bytes_data = st.session_state.uploaded_file.read()
    with open("image.jpg", 'wb') as f:
        f.write(bytes_data)
