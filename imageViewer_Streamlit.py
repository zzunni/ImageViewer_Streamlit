import streamlit as st
import cv2
import numpy as np
from PIL import Image

# 이미지 업로드
uploaded_file = st.file_uploader("Upload an image", type=["jpg", "png"])

# 작업 선택 메뉴
st.sidebar.write("작업을 선택하세요")
convert_to_gray = st.sidebar.button("Convert to Gray")
crop_image = st.sidebar.button("Image Cut")
rotate_image = st.sidebar.button("Image Rotation")
restore_image = st.sidebar.button("Restore")

if uploaded_file:
    # 업로드한 이미지를 읽고 표시
    image = Image.open(uploaded_file)
    img_array = np.array(image)
    original_img = img_array.copy()  # 원본 이미지 저장
    st.image(img_array, caption="Uploaded Image", use_column_width=True)

    # 흑백 이미지 변환
    if convert_to_gray:
        gray = cv2.cvtColor(img_array, cv2.COLOR_RGB2GRAY)
        st.image(gray, caption="Grayscale Image", use_column_width=True)

    # 이미지 자르기
    if crop_image:
        # 사용자로부터 자를 범위를 입력받음 (기본값을 제공함)
        x = st.number_input("Enter start X coordinate:", min_value=0, value=0)
        y = st.number_input("Enter start Y coordinate:", min_value=0, value=0)
        w = st.number_input("Enter width of the crop:", min_value=1, value=100)
        h = st.number_input("Enter height of the crop:", min_value=1, value=100)

        # 이미지 크롭
        if x + w <= img_array.shape[1] and y + h <= img_array.shape[0]:
            cropped = img_array[y:y+h, x:x+w]
            st.image(cropped, caption="Cropped Image", use_column_width=True)
        else:
            st.error("Invalid cropping coordinates.")

    # 이미지 회전
    if rotate_image:
        angle = st.number_input("Enter angle to rotate (degrees):", min_value=-360, max_value=360, value=0)
        (height, width) = img_array.shape[:2]
        center = (width // 2, height // 2)
        matrix = cv2.getRotationMatrix2D(center, angle, 1.0)
        rotated = cv2.warpAffine(img_array, matrix, (width, height))
        st.image(rotated, caption=f"Rotated Image ({angle} degrees)", use_column_width=True)

    # 이미지 복원
    if restore_image:
        st.image(original_img, caption="Restored Original Image", use_column_width=True)

