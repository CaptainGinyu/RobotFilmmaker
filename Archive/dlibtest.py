# Note: this is just a test to see how this runs on the Raspberry Pi.  This is not necessarily meant to be in the final product

import dlib
import cv2

if __name__ == '__main__':

    test_img = cv2.cvtColor(cv2.imread('Kevin.jpg'), cv2.COLOR_BGR2GRAY)
    test_img_width = test_img.shape[1]
    test_img_height = test_img.shape[0]
    
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print('Cannot open camera')
        quit()

    tracker = dlib.correlation_tracker()
    ret, frame = cap.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    tracker.start_track(gray, dlib.rectangle(0, 0, test_img_height, test_img_width))

    while True:
        ret, frame = cap.read()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        tracker.update(gray)

        tracked_position = tracker.get_position()

        cv2.rectangle(frame, (int(tracked_position.left()), int(tracked_position.top())), (int(tracked_position.right()), int(tracked_position.bottom())), (255, 0, 0))
        cv2.imshow('Robot Filmmaker', frame)

        pressed_key = cv2.waitKey(1)

        if pressed_key == 27:
            break

    cv2.destroyAllWindows()
    cap.release()
