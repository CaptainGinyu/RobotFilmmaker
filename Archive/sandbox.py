import cv2
import numpy as np

face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
enable_face_detect = False

curr_face_detect_coord = ()
prev_face_detect_coord = ()

def onmouse(event, x, y, flags, param):
    #print(str(x) + ', ' + str(y))
    pass

def detect_faces(frame):

    global curr_face_detect_coord, prev_face_detect_coord
    
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)

    for (x, y, w, h) in faces:
        frame = cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0))
        prev_face_detect_coord = curr_face_detect_coord
        curr_face_detect_coord = (x, y)

        if prev_face_detect_coord != ():
            x0 = curr_face_detect_coord[0]
            x1 = prev_face_detect_coord[0]
            y0 = curr_face_detect_coord[1]
            y1 = prev_face_detect_coord[1]
            to_print = ''
            if x0 > x1:
                to_print += 'right '
            elif x0 < x1:
                to_print += 'left '
            if y0 > y1:
                to_print += 'down'
            elif y0 < y1:
                to_print += 'up'
            print(to_print)

if __name__ == '__main__':
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print('Cannot open camera')
        quit()

    cv2.namedWindow('Robot Filmmaker')
    cv2.setMouseCallback('Robot Filmmaker', onmouse)

    while True:
        ret, frame = cap.read()        

        if enable_face_detect:
            detect_faces(frame)

        cv2.imshow('Robot Filmmaker', frame)
        
        pressed_key = cv2.waitKey(100)

        # When e key is pressed
        if pressed_key == 101:
            enable_face_detect = not enable_face_detect

        # exit when escape key is pressed
        if pressed_key == 27:        
            break

    cv2.destroyAllWindows()
    cap.release()


