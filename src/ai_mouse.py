import cv2
import mediapipe
import pyautogui

capture_hands = mediapipe.solutions.hands.Hands() # to capture hands
drawing_option = mediapipe.solutions.drawing_utils # importing drawing utilities
screen_width, screen_height = pyautogui.size()
camera = cv2.VideoCapture(0) # camera access
x1 = y1 = x2 = y2 = 0
while True:
    _, image = camera.read() # captureing the image from webcam
    image_height, image_width, _ = image.shape
    image = cv2.flip(image, 1) # fliping the camera view
    rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB) # converting bgr to rgb
    output_hand = capture_hands.process(rgb_image) # processing rgb image
    all_hands = output_hand.multi_hand_landmarks # captureing multi hand and drawing landmarks
    if all_hands:
        for hand in all_hands:
            drawing_option.draw_landmarks(image, hand) # all hand landmarks
            one_hand_landmark = hand.landmark # capturing one hand
            for id, lm in enumerate(one_hand_landmark):
                # print(lm.x, lm.y) # gives float value position of fingers landmark
                x = int(lm.x * image_width)
                y = int(lm.y * image_height)
                if id == 8:
                    mouse_x = int(screen_width / image_width * x)
                    mouse_y = int(screen_height / image_height * y)
                    pyautogui.moveTo(mouse_x, mouse_y)
                    cv2.circle(image, (x, y), 10, (0,255, 255))
                    x1 = x
                    y1 = y
                if id == 4:
                    x2 = x 
                    y2 = y 
                    cv2.circle(image, (x, y), 10, (0, 255, 255))
        dist = y2 - y1
        print(dist)
        if dist < 20:
            pyautogui.click()

    cv2.imshow("Hand movement video", image)
    key = cv2.waitKey(100)
    if key == 27:
        break

camera.release()
cv2.destroyAllWindows()