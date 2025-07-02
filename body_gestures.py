import cv2
import mediapipe as mp
import time
import pyautogui

cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Error: Could not open video source.")
    exit()

mpHands = mp.solutions.hands
hands = mpHands.Hands()
mpdraw = mp.solutions.drawing_utils
last_action_time = 0
action_delay = 1  
def count_fingers(hand_landmarks):
    tip_ids = [4, 8, 12, 16, 20]
    fingers = []
    if hand_landmarks.landmark[tip_ids[0]].x < hand_landmarks.landmark[tip_ids[0]-1].x:
        fingers.append(1)
    else:
        fingers.append(0)
    for i in range(1,5):
        if hand_landmarks.landmark[tip_ids[i]].y < hand_landmarks.landmark[tip_ids[i]-2].y:
            fingers.append(1)
        else:
            fingers.append(0)
    return fingers
while True:
    success, img = cap.read()
    if not success:
        print("Failed to grab frame.")
        break
    imrgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = hands.process(imrgb)
    
    if results.multi_hand_landmarks:
        for handles in results.multi_hand_landmarks:
            finger_count = count_fingers(handles)
            mpdraw.draw_landmarks(img, handles,mpHands.HAND_CONNECTIONS)
            print(finger_count)
            current_time = time.time()

            if current_time - last_action_time > action_delay:
                if finger_count == [1,1,0,0,0] or finger_count == [0,1,0,0,0]:
                    pyautogui.press('up')
                    cv2.putText(img, "UP", (10, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                    last_action_time = current_time
                elif finger_count == [1,1,1,0,0] or finger_count == [0,1,1,0,0]:
                    pyautogui.press('left')
                    cv2.putText(img, "left", (10, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                    last_action_time = current_time
                elif finger_count == [1,1,1,1,0] or finger_count == [0,1,1,1,0]:
                    pyautogui.press('right')
                    cv2.putText(img, "right", (10, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                    last_action_time = current_time
                elif finger_count == [1,1,1,1,1] or finger_count == [0,1,1,1,1]:
                    pyautogui.press('down')
                    cv2.putText(img, "down", (10, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                    last_action_time = current_time
    cv2.imshow("Webcam", img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break


cap.release()              
cv2.destroyAllWindows()      



