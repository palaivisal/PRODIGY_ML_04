import cv2 as cv
import mediapipe as mp
import pyautogui


mp_hands = mp.solutions.hands
capture_hands = mp_hands.Hands()
drawing_options = mp.solutions.drawing_utils
camera = cv.VideoCapture(0)
scr_width, scr_height = pyautogui.size()
x1 = x2 = y1 = y2 = 0


while True:
    ret, image = camera.read()
    if not ret:
        print("Failed to grab frame")
        break
    image_height, image_width, _ = image.shape
    image = cv.flip(image, 1)
    rgb = cv.cvtColor(image, cv.COLOR_BGR2RGB)
    op_hands = capture_hands.process(rgb)
    all_hands = op_hands.multi_hand_landmarks
    if all_hands:
        for hand in all_hands:
            drawing_options.draw_landmarks(image, hand, mp_hands.HAND_CONNECTIONS)
            one_hand_landmarks = hand.landmark
            for id, lm in enumerate(one_hand_landmarks):
                x = int(lm.x * image_width)
                y = int(lm.y * image_height)
                if id == 8:
                    y1 = y
                    x1 = x
                    mouse_x = int(scr_width / image_width * x)
                    mouse_y = int(scr_height / image_height * y)
                    pyautogui.moveTo(mouse_x, mouse_y)
                    cv.circle(image, (x, y), 10, (0, 255, 255), -1)
                if id == 4:
                    x2 = x
                    y2 = y
                    cv.circle(image, (x, y), 10, (0, 255, 255), -1)
        dist = abs(y2 - y1)
        print(dist)
        if dist < 60:
            pyautogui.click()
    cv.imshow("Hand movement", image)
    if cv.waitKey(1) & 0xFF == ord('q'):
        break
camera.release()
cv.destroyAllWindows()
