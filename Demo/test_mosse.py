###################################################################
# IMPORTS
###################################################################

import boto3
import botocore
import cv2, sys, numpy, os
import time
import serial
from cv2 import face
from mosse import MOSSE


#arduinoSerial = serial.Serial('/dev/cu.usbmodem1421', 9600)
#fourcc = cv2.VideoWriter_fourcc(*'MP42')
#out = cv2.VideoWriter('output.mp4', fourcc, 20.0, (1280,960))

###################################################################
# PARAMETERS
###################################################################
arduinoSerial = serial.Serial('COM3', 9600)

XML_FILE = 'trained - Copy.xml'     # XML file name
WEBCAM_PORT = 1                     # Webcam port
KEY_BREAK = 27                      # Key to stop program (27 = escape)

TIMER_FACE = 7.5        # Face detection reset every x seconds
TIMER_SERVO = 3         # Servo movement every x seconds
MOVE_DIFF_X = 35        # Servo moves if x-axis difference between center of face and frame is greater than this
MOVE_DIFF_Y = 30        # Servo moves if y-axis difference between center of face and frame is greater than this

###################################################################
# DETECT INITIAL FACE
###################################################################
# Create model
model = face.FisherFaceRecognizer_create()

names = ['Kevin', 'Target']
fn_dir = os.getcwd() + '/Faces'
(images, labels, names, id) = ([], [], {}, 0)
for (subdirs, dirs, files) in os.walk(fn_dir):
    for subdir in dirs:
        names[id] = subdir
        print (subdir)
        id += 1
model.read(XML_FILE)
face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
(im_width, im_height) = (125, 125)

# Start webcam, record time, start counting frames
webcam = cv2.VideoCapture(WEBCAM_PORT)      # Start webcam
time.sleep(1)                               # Allow warmup
t_start = time.time()
n_frames = 0

# Loop until face detected (target = 1)
target = 0
while target == 0:
    # Read frame and calculate center
    (rval, frame) = webcam.read()
    n_frames = n_frames + 1                                 # Increment frame count for FPS calculations
    height, width = frame.shape[:2]
    frame = cv2.flip(frame, 1, 0)
    desired_center = numpy.array([width / 2, height / 2])   # Calculate center of frame

    label = []
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)

    # Detect faces
    for (x, y, w, h) in faces:
        face = gray[y:y + h, x:x + w]
        face_resize = cv2.resize(face, (im_width, im_height))
        otsu = cv2.adaptiveThreshold(face_resize, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 11, 2)

        # Try to recognize the face
        prediction = model.predict(otsu)
        (dirX, dirY) = ("", "")

        # Write the name of recognized face
        name = names[prediction[0]]
        if prediction[1] < 3000:
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 3)
            cv2.putText(frame, '%s - %.0f' % (name, prediction[1]), (x - 10, y - 10), cv2.FONT_HERSHEY_PLAIN, 1,
                        (0, 255, 0))
            label.append(name)
            target = 1
            print("FOUND!")

        else:
            target = 0

        # Show frame
        cv2.imshow('Test', frame)

# Found a face!
tracker = MOSSE(gray, [x, y, x + w, y + h])     # Create MOSSE tracker
t0 = time.time()                                # Start timer for face detection
servo_t0 = time.time()                          # Start timer for servo movement

# Initial face is found so forever loop
while 1:
    # Keep getting the times and calculate the differences
    t1 = time.time()
    servo_t1 = time.time()
    tdiff = t1 - t0
    servo_tdiff = servo_t1 - servo_t0

    # Read in a frame and increment frames
    (rval, frame) = webcam.read()
    n_frames = n_frames + 1
    frame = cv2.flip(frame, 1, 0)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # 1. If timer is up or face hasn't been detected, do face detection until it has been detected
    #    This also does a continual face detection 'reset' every x seconds
    if tdiff > TIMER_FACE or target == 0:
        print("Detecting face")
        # Reset timer
        t0 = time.time()

        # Do face detection
        faces = face_cascade.detectMultiScale(gray, 1.3, 5)
        for (x, y, w, h) in faces:
            face = gray[y:y + h, x:x + w]
            face_resize = cv2.resize(face, (im_width, im_height))
            otsu = cv2.adaptiveThreshold(face_resize, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 11, 2)

            # Try to recognize the face
            prediction = model.predict(otsu)
            (dirX, dirY) = ("", "")

            # Write the name of recognized face
            name = names[prediction[0]]
            if prediction[1] < 3000:
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 3)
                cv2.putText(frame, '%s - %.0f' % (name, prediction[1]), (x - 10, y - 10), cv2.FONT_HERSHEY_PLAIN, 1,
                            (0, 255, 0))
                label.append(name)

                # Face has been found.  Update MOSSE tracker
                print("Face found! Creating tracker")
                target = 1
                tracker.newface(gray, [x, y, x + w, y + h])

            else:
                target = 0

    # 2. Do MOSSE tracking if face has been detected
    else:
        tracker.update(gray)
        (draw_x, draw_y), (draw_w, draw_h) = tracker.pos, tracker.size
        draw_x1, draw_y1, draw_x2, draw_y2 = int(draw_x - 0.5 * draw_w), int(draw_y - 0.5 * draw_h), int(draw_x + 0.5 * draw_w), int(draw_y + 0.5 * draw_h)

        x = draw_x1
        y = draw_y1
        w = draw_x2 - draw_x1
        h = draw_y2 - draw_y1

        #Original MOSSE rectangle is:
        #cv2.rectangle(frame, (draw_x1, draw_y1), (draw_x2, draw_y2), (0, 0, 255), 3)
        cv2.rectangle(frame, (x, y), (draw_x2, draw_y2), (0, 0, 255), 3)

    # 3. If servo timer is up and face detected, move the servo
    if servo_tdiff > TIMER_SERVO and target == 1:
        print("Moving servo")
        # Reset timer
        servo_t0 = time.time()

        # Calculate center difference
        center = numpy.array([x + (w / 2), y + (h / 2)])
        movement = desired_center - center
        length_face = x + w;
        width_face = y + h;

        # Move servo based if face is off center by some amount
        if numpy.abs(movement[0]) > MOVE_DIFF_X and numpy.abs(movement[1]) > MOVE_DIFF_Y:
            if movement[0] > 0:
                dirX = "East"
                arduinoSerial.write(bytes('r'))
                print ('r')
            else:
                dirX = "West"
                arduinoSerial.write(bytes('l'))
                print ('l')
            if movement[1] > 0:
                dirY = "North"
                arduinoSerial.write(bytes('u'))
                print ('u')
            else:
                dirY = "South"
                arduinoSerial.write(bytes('d'))
                print ('d')
        # if numpy.abs(length_face) < height/3 or numpy.abs(width_face) < width/3:
        #     arduinoSerial.write(bytes('f'))
        #     print ('f')
        #
        # if numpy.abs(length_face) > height/3 or numpy.abs(width_face) > width/3:
        #     arduinoSerial.write(bytes('b'))
        #     print ('b')

    #4. Show frame
    cv2.imshow('Test', frame)

    #5. Break key
    key = cv2.waitKey(10)
    if key == 27:
        #out.release()
        break

# Calculate total time
t_end = time.time()
t_total = t_end - t_start
print ("Time taken : {0} seconds".format(t_total))
print (t_total)

# Calculate frames per second
fps = n_frames / t_total
print ("Estimated frames per second : {0}".format(fps))