import cv2
import mediapipe as mp
import numpy as np
import streamlit as st
import os

# Streamlit UI
st.set_page_config(page_title="Air Drawing App", layout="wide")
st.title("✋ Virtual Air Drawing using OpenCV + Mediapipe + Streamlit")

run = st.checkbox("Run Webcam")
clear_btn = st.button("🧹 Clear Drawing")
save_btn = st.button("🖼 Save Drawing")

FRAME_WINDOW = st.image([])

# Mediapipe setup
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=1, min_detection_confidence=0.7, min_tracking_confidence=0.7)

# Drawing setup
canvas = np.zeros((480, 640, 3), dtype=np.uint8)
colors = [(0, 0, 255), (0, 255, 0), (255, 0, 0), (0, 255, 255)]
color_index = 0
draw_color = colors[color_index]

prev_x, prev_y = 0, 0

cap = cv2.VideoCapture(0)

while run:
    ret, frame = cap.read()
    if not ret:
        st.write("⚠️ No webcam detected!")
        break

    frame = cv2.flip(frame, 1)
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    result = hands.process(rgb)

    # Draw color palette
    for i, color in enumerate(colors):
        cv2.rectangle(frame, (i * 60, 0), ((i + 1) * 60, 60), color, -1)

    if result.multi_hand_landmarks:
        for hand_landmarks in result.multi_hand_landmarks:
            h, w, _ = frame.shape
            lm_list = []
            for lm in hand_landmarks.landmark:
                cx, cy = int(lm.x * w), int(lm.y * h)
                lm_list.append((cx, cy))

            if lm_list:
                index_x, index_y = lm_list[8]
                thumb_x, thumb_y = lm_list[4]

                # Color selection (index finger in palette)
                if index_y < 60:
                    color_index = index_x // 60
                    if color_index < len(colors):
                        draw_color = colors[color_index]

                # Drawing when index + thumb close
                dist = np.hypot(index_x - thumb_x, index_y - thumb_y)
                if dist < 40:
                    if prev_x == 0 and prev_y == 0:
                        prev_x, prev_y = index_x, index_y
                    cv2.line(canvas, (prev_x, prev_y), (index_x, index_y), draw_color, 5)
                    prev_x, prev_y = index_x, index_y
                else:
                    prev_x, prev_y = 0, 0

    # 🧹 Clear with Streamlit button
    if clear_btn:
        canvas = np.zeros((480, 640, 3), dtype=np.uint8)

    # 🖼 Save with Streamlit button
    if save_btn:
        cv2.imwrite("drawing.png", canvas)
        st.success("✅ Drawing saved as drawing.png")

    # Merge frame + drawing
    gray = cv2.cvtColor(canvas, cv2.COLOR_BGR2GRAY)
    _, inv = cv2.threshold(gray, 20, 255, cv2.THRESH_BINARY)
    inv = cv2.cvtColor(inv, cv2.COLOR_GRAY2BGR)
    frame = cv2.bitwise_and(frame, cv2.bitwise_not(inv))
    frame = cv2.bitwise_or(frame, canvas)

    FRAME_WINDOW.image(frame, channels="BGR")

cap.release()
