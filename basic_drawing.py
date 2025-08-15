import cv2
import numpy as np
import mediapipe as mp
import math
import time

# Initialize MediaPipe Hands
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
hands = mp_hands.Hands(max_num_hands=1, min_detection_confidence=0.7, min_tracking_confidence=0.5)

# Canvas and states
prev_x, prev_y = 0, 0
canvas = None

# Start Webcam
cap = cv2.VideoCapture(0)
cap.set(3, 640)
cap.set(4, 480)

# Frame rate control
prev_time = 0

while True:
    success, frame = cap.read()
    if not success:
        break

    frame = cv2.flip(frame, 1)
    h, w, _ = frame.shape

    if canvas is None:
        canvas = np.zeros((h, w, 3), dtype=np.uint8)

    # Limit to ~30 FPS
    current_time = time.time()
    if current_time - prev_time < 1 / 30:
        continue
    prev_time = current_time

    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    result = hands.process(rgb)

    if result.multi_hand_landmarks:
        for hand_landmarks in result.multi_hand_landmarks:
            mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

            lm = hand_landmarks.landmark
            index_tip = (int(lm[8].x * w), int(lm[8].y * h))
            thumb_tip = (int(lm[4].x * w), int(lm[4].y * h))

            # Distance between index and thumb
            distance = math.hypot(index_tip[0] - thumb_tip[0], index_tip[1] - thumb_tip[1])

            if distance < 40:
                if prev_x == 0 and prev_y == 0:
                    prev_x, prev_y = index_tip
                cv2.line(canvas, (prev_x, prev_y), index_tip, (255, 255, 255), 5)  # Solid red line
                prev_x, prev_y = index_tip
            else:
                prev_x, prev_y = 0, 0

    # Combine canvas and frame without transparency
    mask = cv2.cvtColor(canvas, cv2.COLOR_BGR2GRAY)
    _, mask = cv2.threshold(mask, 10, 255, cv2.THRESH_BINARY)
    mask_inv = cv2.bitwise_not(mask)
    frame_bg = cv2.bitwise_and(frame, frame, mask=mask_inv)
    canvas_fg = cv2.bitwise_and(canvas, canvas, mask=mask)
    output = cv2.add(frame_bg, canvas_fg)

    # Instruction text
    cv2.putText(output, "✍️ Pinch to Draw | Press 'c' to Clear | Press 'Esc' to Exit", (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 255), 2)

    cv2.imshow("Gesture Drawing ✍️", output)

    key = cv2.waitKey(1) & 0xFF
    if key == ord('c'):
        canvas = np.zeros((h, w, 3), dtype=np.uint8)
    elif key == 27:  # ESC key
        break

cap.release()
cv2.destroyAllWindows()
