# Note: this is just a test to see how this runs on the Raspberry Pi.  This is not necessarily meant to be in the final product

import cv2
import numpy as np

if __name__ == '__main__':

    test_img = cv2.cvtColor(cv2.imread('Kevin.jpg'), cv2.COLOR_BGR2GRAY)
    test_img_width, test_img_height = test_img.shape[::-1]
    
    cap = cv2.VideoCapture(0)

    while True:
        frame = cap.read()[1]
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        res = cv2.matchTemplate(gray, test_img, cv2.TM_CCOEFF_NORMED)
        top_left = cv2.minMaxLoc(res)[3]
        bottom_right = (top_left[0] + test_img_width, top_left[1] + test_img_height)

        cv2.rectangle(frame, top_left, bottom_right, (255, 0, 0), 2)
        
        cv2.imshow('Robot Filmmaker', frame)

        pressed_key = cv2.waitKey(1)

        if pressed_key == 27:
            break

    cv2.destroyAllWindows()
    cap.release()
