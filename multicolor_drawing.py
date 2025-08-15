import cv2
import numpy as np
import mediapipe as mp
import math

# Mediapipe setup
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=1, min_detection_confidence=0.7)
mp_draw = mp.solutions.drawing_utils

# Colors (BGR)
colors = [(0,0,255), (0,255,0), (255,0,0), (0,255,255)]  # Red, Green, Blue, Yellow
color_index = 0

# Canvas
canvas = None

# Video capture
cap = cv2.VideoCapture(0)

# Previous point (for smooth drawing)
prev_x, prev_y = 0, 0

def fingers_up(hand_landmarks):
    """Return list [thumb, index, middle, ring, pinky] (1=up,0=down)."""
    tips = [4, 8, 12, 16, 20]
    fingers = []

    # Thumb
    if hand_landmarks.landmark[tips[0]].x < hand_landmarks.landmark[tips[0]-1].x:
        fingers.append(1)
    else:
        fingers.append(0)

    # Other fingers
    for id in range(1,5):
        if hand_landmarks.landmark[tips[id]].y < hand_landmarks.landmark[tips[id]-2].y:
            fingers.append(1)
        else:
            fingers.append(0)
    return fingers

while True:
    ret, frame = cap.read()
    if not ret:
        break
    
    frame = cv2.flip(frame, 1)
    if canvas is None:
        canvas = np.zeros_like(frame)

    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    result = hands.process(rgb)

    if result.multi_hand_landmarks:
        for hand_landmarks in result.multi_hand_landmarks:
            lm = hand_landmarks.landmark
            h, w, _ = frame.shape

            # Index and Thumb tip coordinates
            ix, iy = int(lm[8].x * w), int(lm[8].y * h)
            tx, ty = int(lm[4].x * w), int(lm[4].y * h)

            fingers = fingers_up(hand_landmarks)

            # Color selection with ONLY index finger up
            if fingers[1] == 1 and sum(fingers) == 1:
                for i, col in enumerate(colors):
                    if 10+i*60 < ix < 60+i*60 and 10 < iy < 60:
                        color_index = i

            # Draw when thumb + index finger pinch
            dist = math.hypot(ix - tx, iy - ty)
            if dist < 40:  # pinch detected
                if prev_x == 0 and prev_y == 0:
                    prev_x, prev_y = ix, iy
                cv2.line(canvas, (prev_x, prev_y), (ix, iy), colors[color_index], 3)  # smooth thin line
                prev_x, prev_y = ix, iy
            else:
                prev_x, prev_y = 0, 0  # reset when not pinching

            mp_draw.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

    # Merge drawing
    gray = cv2.cvtColor(canvas, cv2.COLOR_BGR2GRAY)
    _, inv = cv2.threshold(gray, 20, 255, cv2.THRESH_BINARY_INV)
    inv = cv2.cvtColor(inv, cv2.COLOR_GRAY2BGR)
    frame = cv2.bitwise_and(frame, inv)
    frame = cv2.bitwise_or(frame, canvas)

    # Draw color palette
    for i, col in enumerate(colors):
        cv2.rectangle(frame, (10+i*60, 10), (60+i*60, 60), col, -1)
        if i == color_index:
            cv2.rectangle(frame, (10+i*60, 10), (60+i*60, 60), (255,255,255), 2)

    cv2.putText(frame, "C: Clear | ESC: Exit", (10, 470),
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255,255,255), 2)

    cv2.imshow("Air Drawing", frame)

    key = cv2.waitKey(1) & 0xFF
    if key == 27:  # ESC
        break
    elif key == ord('c'):  # clear
        canvas = np.zeros_like(frame)

cap.release()
cv2.destroyAllWindows()
