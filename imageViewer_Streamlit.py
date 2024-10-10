import streamlit as st
import numpy as np
import cv2
from PIL import Image

# 이미지 업로드
uploaded_file = st.file_uploader("Upload an image", type=["jpg", "png"])

# 작업 선택 메뉴
st.sidebar.write("작업을 선택하세요")
convert_to_gray = st.sidebar.button("Convert to Gray")
crop_image = st.sidebar.button("Image Cut")
rotate_image = st.sidebar.button("Image Rotation")
restore_image = st.sidebar.button("Restore")

# 이미지 변환 함수들
def convert_to_gray(image_array):
    gray = cv2.cvtColor(image_array, cv2.COLOR_RGB2GRAY)
    return gray

def crop_image_func(image_array, x, y, w, h):
    return image_array[y:y+h, x:x+w]

def rotate_image_func(image_array, angle):
    (h, w) = image_array.shape[:2]
    center = (w // 2, h // 2)
    matrix = cv2.getRotationMatrix2D(center, angle, 1.0)
    return cv2.warpAffine(image_array, matrix, (w, h))

# 이미지 복원
if uploaded_file:
    image = Image.open(uploaded_file)
    img_array = np.array(image)
    original_img = img_array.copy()  # 원본 이미지 저장
    st.image(img_array, caption="Uploaded Image", use_column_width=True)

    if convert_to_gray:
        gray_img = convert_to_gray(img_array)
        st.image(gray_img, caption="Grayscale Image", use_column_width=True)

    if crop_image:
        x = st.sidebar.number_input("X", min_value=0, max_value=img_array.shape[1], value=0)
        y = st.sidebar.number_input("Y", min_value=0, max_value=img_array.shape[0], value=0)
        w = st.sidebar.number_input("Width", min_value=0, max_value=img_array.shape[1] - x, value=100)
        h = st.sidebar.number_input("Height", min_value=0, max_value=img_array.shape[0] - y, value=100)
        cropped_img = crop_image_func(img_array, x, y, w, h)
        st.image(cropped_img, caption="Cropped Image", use_column_width=True)

    if rotate_image:
        angle = st.sidebar.number_input("Angle", min_value=-360, max_value=360, value=0)
        rotated_img = rotate_image_func(img_array, angle)
        st.image(rotated_img, caption=f"Rotated Image ({angle} degrees)", use_column_width=True)

    if restore_image:
        st.image(original_img, caption="Restored Original Image", use_column_width=True)
