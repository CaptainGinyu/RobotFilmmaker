# AUTHORS: Philip, Harshil
# DESCRIPTION:
# This is the tracking module for RobotFilmmaker
# Downloads XML from AWS bucket to read into model, then tracks target using MOSSE and moves servos
# Breaking this program depends on either reading the right firebase tag or pressing the KEY_BREAK on keyboard
# Saves video as VIDEO_FILE as .avi

def tracking():
    ###################################################################
    # IMPORTS
    ###################################################################
    import boto3
    import botocore
    import cv2, sys, numpy, os
    import time
    import serial
    import pyrebase
    from cv2 import face
    from mosse import MOSSE

    # arduinoSerial = serial.Serial('/dev/cu.usbmodem1421', 9600)
    # fourcc = cv2.VideoWriter_fourcc(*'MP42')
    # out = cv2.VideoWriter('output.mp4', fourcc, 20.0, (1280,960))
    ###################################################################
    # PARAMETERS
    ###################################################################
    # Arduino connection
    ARDUINO_PORT = 'COM3'
    arduinoSerial = serial.Serial(ARDUINO_PORT, 9600)

    # General parameters
    VIDEO_FILE = 'output.avi'  # Video output file name
    WEBCAM_PORT = 1  # Webcam port
    XML_FILE = 'trained.xml'  # XML file name
    KEY_BREAK = 27  # Key to stop program (27 = escape)

    # Tracking parameters
    TIMER_FACE = 5.0  # Face detection reset every x seconds
    TIMER_SERVO = 1.0  # Servo movement every x seconds
    TIMER_FORWARD = 5.0  # Robot movement forward and backwards every x seconds
    TIMER_FIREBASE = 2  # Firebase messaging every x seconds
    MOVE_DIFF_X = 45  # Servo moves if x-axis difference between center of face and frame is greater than this (35 default)
    MOVE_DIFF_Y = 40  # Servo moves if y-axis difference between center of face and frame is greater than this (30 default)

    # AWS parameters
    # AWS_CREDS should be a text file with two lines: first line is access key, seconds line is secret key
    AWS_CREDS = 'adminuser.txt'
    AWS_BUCKET_DOWNLOAD = 'robotfilmmaker-models'  # Bucket name to download from
    AWS_KEY = 'trained.xml'  # File to download

    # Firebase parameters
    config = {
        "apiKey": "AIzaSyBpFiIIpHEkuj7PgiQad8EcggMIqcGohWI",
        "authDomain": "https://fir-auth-6d6d8.firebaseapp.com",
        "databaseURL": "https://fir-auth-6d6d8.firebaseio.com",
        "storageBucket": "https://fir-auth-6d6d8.appspot.com"
    }

    ####################################################################
    # GET XML FILE FROM CLOUD
    ####################################################################
    try:
        file = open(AWS_CREDS, 'r')
        creds = file.readlines()
        for i in range(0, len(creds)):
            curr = creds[i]
            newline_index = curr.find('\n')
            if newline_index != -1:
                creds[i] = curr[0:newline_index]

        file.close()

    except IOError:
        print('Error: Cannot read s3creds.txt')
        quit()

    # Open boto resource/bucket
    s3 = boto3.resource(
        's3',
        aws_access_key_id=creds[0],
        aws_secret_access_key=creds[1]
    )

    bucket_dl = s3.Bucket(AWS_BUCKET_DOWNLOAD)

    try:
        path = os.curdir
        if not os.path.exists(path):
            os.makedirs(path)
        bucket_dl.download_file(AWS_KEY, path + "/trained.xml")

    except botocore.exceptions.ClientError as e:
        if e.response['Error']['Code'] == "404":
            print("The object does not exist.")
        else:
            raise

    print('XML file retrieved')

    ####################################################################
    # FIREBASE SETUP
    ####################################################################
    firebase = pyrebase.initialize_app(config)
    db = firebase.database()

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

    # Start webcam and video writer.  Allow warmup
    webcam = cv2.VideoCapture(WEBCAM_PORT)
    out = cv2.VideoWriter(VIDEO_FILE, cv2.VideoWriter_fourcc('M', 'J', 'P', 'G'), 20,
                          (int(webcam.get(3)), int(webcam.get(4))))
    time.sleep(1)

    # Keep reading until webcam gets something
    (rval, frame) = webcam.read()
    while frame is None:
        webcam.release()
        webcam = cv2.VideoCapture(WEBCAM_PORT)
        (rval, frame) = webcam.read()

    # Start counting time and frames
    t_start = time.time()
    n_frames = 0

    # Loop until face detected (target = 1)
    target = 0
    while target == 0:
        # Read frame, flip and output to video
        (rval, frame) = webcam.read()
        frame = cv2.flip(frame, 1, 0)
        out.write(frame)

        # Calculations
        n_frames = n_frames + 1  # Increment frame count for FPS calculations
        height, width = frame.shape[:2]
        desired_center = numpy.array([width / 2, height / 2])  # Calculate center of frame

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

                # Save the box as face detection specific
                w_detect = w
                h_detect = h
                w_mosse = w_detect
                h_mosse = h_detect
                length_face = w_detect
                width_face = h_detect

            else:
                target = 0

        # Show frame
        cv2.imshow('Test', frame)
        cv2.waitKey(10)

    ###################################################################
    # FACE FOUND.  GO TO MAIN LOOP
    ###################################################################
    # Found a face! Set up timers and tracker and variables
    tracker = MOSSE(gray, [x, y, x + w, y + h])  # Create MOSSE tracker
    tag_status = "Tracking Started"  # Firebase status is set to Started1
    db.child("Status").set("Tracking Started")
    t0 = time.time()  # Start timer for face detection
    servo_t0 = t0  # Start timer for servo movement
    firebase_t0 = t0  # Start timer for firebase
    forward_t0 = t0     # Start timer for forward/backward

    # Initial face is found so forever loop
    while 1:
        # Keep getting the times and calculate the differences
        t1 = time.time()
        servo_t1 = t1
        firebase_t1 = t1
        forward_t1 = t1

        tdiff = t1 - t0
        servo_tdiff = servo_t1 - servo_t0
        firebase_tdiff = firebase_t1 - firebase_t0
        forward_tdiff = forward_t1 - forward_t0

        # Read frame, flip, and output to video
        (rval, frame) = webcam.read()
        frame = cv2.flip(frame, 1, 0)
        out.write(frame)

        # Frame manipulations
        n_frames = n_frames + 1
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # 1. Do face detection if:
        #       - Timer is up or
        #       - Face hasn't been detected, either by algorithm or by a manual Firebase 'reset' (target == 0)
        #    This also does a continual face detection 'reset' every x seconds
        if tdiff > TIMER_FACE or target == 0:
            print("Detecting face")
            t0 = time.time()  # Reset timer

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

                    # Save the box as face specific and update MOSSE
                    w_detect = w
                    h_detect = h
                    w_mosse = w_detect
                    h_mosse = h_detect
                    length_face = w_detect
                    width_face = h_detect

                else:
                    target = 0

        # 2. Do MOSSE tracking if face has been detected
        else:
            tracker.update(gray)
            (draw_x, draw_y), (draw_w, draw_h) = tracker.pos, tracker.size
            draw_x1, draw_y1, draw_x2, draw_y2 = int(draw_x - 0.5 * draw_w), int(draw_y - 0.5 * draw_h), int(
                draw_x + 0.5 * draw_w), int(draw_y + 0.5 * draw_h)

            # Save coordinates
            x = draw_x1
            y = draw_y1
            w = draw_x2 - draw_x1
            h = draw_y2 - draw_y1

            # Save coordinates for tracking
            w_mosse = w
            h_mosse = h

            # Original MOSSE rectangle is:
            # cv2.rectangle(frame, (draw_x1, draw_y1), (draw_x2, draw_y2), (0, 0, 255), 3)
            cv2.rectangle(frame, (x, y), (draw_x2, draw_y2), (0, 0, 255), 3)

        # 4. If forward timer is up and face detected, move the car forward/backward
        if forward_tdiff > TIMER_FORWARD and target == 1:
            print("Moving cart")
            forward_t0 = time.time()    # Reset timer

            # The closer you are, the bigger the box is
            print(length_face)
            print(height/3)
            print(width_face)
            print(width/3)
            #print("length: " + length_face + "vs. height/3: " + height/3)
            #print("width: " + width_face + "width/3: "+ width/ 3)
            if numpy.abs(length_face) < height/6 or numpy.abs(width_face) < width/6:
                arduinoSerial.write(bytes('f'))
                print ('f')
            if numpy.abs(length_face) > height/3 or numpy.abs(width_face) > width/3:
                arduinoSerial.write(bytes('b'))
                print ('b')

        # 3. If servo timer is up and face detected, move the servo
        elif servo_tdiff > TIMER_SERVO and target == 1:
            print("Moving servo")
            servo_t0 = time.time()  # Reset timer

            # Calculate center difference
            center = numpy.array([x + (w / 2), y + (h / 2)])
            movement = desired_center - center
            #length_face = w_mosse
            #width_face = h_mosse

            # Move servo based if face is off center by some amount
            if numpy.abs(movement[0]) > MOVE_DIFF_X or numpy.abs(movement[1]) > MOVE_DIFF_Y:
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
            '''
            # If the face takes up less than 33% of the frame, move forward
            if numpy.abs(length_face) < height/3 or numpy.abs(width_face) < width/3:
                arduinoSerial.write(bytes('f'))
                print ('f')

            # If the face takes up greater than 66% of the frame, move backward
            if numpy.abs(length_face) > 2*height/3 or numpy.abs(width_face) > 2*width/3:
                arduinoSerial.write(bytes('b'))
                print ('b')
            '''


        # 5. Check firebase for status
        if firebase_tdiff > TIMER_FIREBASE:
            print("Retrieving Firebase")
            firebase_t0 = time.time()  # Reset timer
            tag_status = db.child("Status").get()  # Check firebase

            # If status = Stopped1, break
            if tag_status.val() == "Tracking Completed":
                break

            # If status = Reset, do manual face detection (target = 0) and reset tag to Started
            if tag_status.val() == 'Tracking Reset':
                print("Reset face detection")
                target = 0
                db.child("Status").set("Tracking Started")

                # Reset port
                #arduinoSerial.close()
                #arduinoSerial = serial.Serial(ARDUINO_PORT, 9600)

        # 5. Show frame
        cv2.imshow('Test', frame)

        # 6. Check user keyboard
        key = cv2.waitKey(10)
        if key == 27:
            out.release()  # Save video
            break

    # Save video and cleanup
    arduinoSerial.close()
    out.release()
    cv2.destroyAllWindows()
    webcam.release()

    # Calculate total time
    t_end = time.time()
    t_total = t_end - t_start
    print ("Time taken : {0} seconds".format(t_total))
    print (t_total)

    # Calculate frames per second
    fps = n_frames / t_total
    print ("Estimated frames per second : {0}".format(fps))