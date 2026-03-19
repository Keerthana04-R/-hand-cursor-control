import cv2
import mediapipe as mp
import pyautogui
import numpy as np
import time
import os

# Setup
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=1, min_detection_confidence=0.7)
mp_draw = mp.solutions.drawing_utils

cap = cv2.VideoCapture(0)
screen_w, screen_h = pyautogui.size()
pyautogui.FAILSAFE = False

# Screenshot save folder
SAVE_FOLDER = r"C:\Users\acer\OneDrive\画像\Screenshots"

# Smooth function
positions = []
def smooth(x, y, n=5):
    positions.append((x, y))
    if len(positions) > n:
        positions.pop(0)
    return int(np.mean([p[0] for p in positions])), int(np.mean([p[1] for p in positions]))

# Detect which fingers are up
def fingers_up(hand_landmarks):
    tips = [8, 12, 16, 20]
    fingers = []
    for tip in tips:
        if hand_landmarks.landmark[tip].y < hand_landmarks.landmark[tip - 2].y:
            fingers.append(1)
        else:
            fingers.append(0)
    return fingers  # [index, middle, ring, pinky]

# Screenshot cooldown
last_screenshot_time = 0
screenshot_cooldown = 2

while True:
    ret, frame = cap.read()
    frame = cv2.flip(frame, 1)
    h, w, _ = frame.shape

    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    result = hands.process(rgb)

    if result.multi_hand_landmarks:
        for hand_landmarks in result.multi_hand_landmarks:
            mp_draw.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

            index_tip  = hand_landmarks.landmark[8]
            thumb_tip  = hand_landmarks.landmark[4]
            middle_tip = hand_landmarks.landmark[12]

            fingers = fingers_up(hand_landmarks)

            x = int(index_tip.x * w)
            y = int(index_tip.y * h)
            screen_x = np.interp(x, [0, w], [0, screen_w])
            screen_y = np.interp(y, [0, h], [0, screen_h])
            screen_x, screen_y = smooth(screen_x, screen_y)

            # GESTURE 1 — Move cursor (only index finger up)
            if fingers == [1, 0, 0, 0]:
                pyautogui.moveTo(screen_x, screen_y, duration=0.05)
                cv2.putText(frame, "MOVE", (10, 50),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 0), 2)

            # GESTURE 2 — Left Click (pinch thumb + index)
            dist_click = abs(index_tip.x - thumb_tip.x) + abs(index_tip.y - thumb_tip.y)
            if dist_click < 0.05:
                pyautogui.click()
                cv2.putText(frame, "LEFT CLICK", (10, 50),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

            # GESTURE 3 — Right Click (pinch thumb + middle)
            dist_right = abs(middle_tip.x - thumb_tip.x) + abs(middle_tip.y - thumb_tip.y)
            if dist_right < 0.05:
                pyautogui.rightClick()
                cv2.putText(frame, "RIGHT CLICK", (10, 50),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

            # GESTURE 4 — Scroll Up (index + middle up)
            if fingers == [1, 1, 0, 0]:
                pyautogui.scroll(3)
                cv2.putText(frame, "SCROLL UP", (10, 50),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)

            # GESTURE 5 — Scroll Down (index + middle + ring up)
            if fingers == [1, 1, 1, 0]:
                pyautogui.scroll(-3)
                cv2.putText(frame, "SCROLL DOWN", (10, 50),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 165, 255), 2)

            # GESTURE 6 — Screenshot (all 4 fingers up)
            if fingers == [1, 1, 1, 1]:
                current_time = time.time()
                if current_time - last_screenshot_time > screenshot_cooldown:
                    cv2.putText(frame, "SCREENSHOT IN 1s...", (10, 50),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 0, 255), 2)
                    cv2.imshow("Hand Cursor", frame)
                    cv2.waitKey(1000)

                    timestamp = time.strftime("%Y%m%d_%H%M%S")
                    filename = os.path.join(SAVE_FOLDER, f"screenshot_{timestamp}.png")
                    screenshot = pyautogui.screenshot()
                    screenshot.save(filename)

                    last_screenshot_time = current_time
                    print(f"Screenshot saved: {filename}")

                    cv2.putText(frame, f"SAVED!", (10, 90),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 255), 2)
                else:
                    remaining = screenshot_cooldown - (current_time - last_screenshot_time)
                    cv2.putText(frame, f"WAIT {remaining:.1f}s", (10, 50),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (150, 0, 150), 2)

    cv2.imshow("Hand Cursor", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()