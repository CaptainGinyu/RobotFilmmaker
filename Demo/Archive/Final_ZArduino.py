import boto3
import botocore
import cv2, sys, numpy, os
import time
from cv2 import face
import serial

def Download_Track():
    #serial import
    arduinoSerial = serial.Serial('/dev/cu.usbmodem1421', 9600)
    # fourcc = cv2.VideoWriter_fourcc(*'MP42')
    # out = cv2.VideoWriter('output.mp4', fourcc, 20.0, (960,1280))
        ####################################################################
        # GET XML FILE FROM CLOUD
        ####################################################################
        # Get credentials
        # adminuser has two lines: first line is access key, seconds line is secret key
    # AWS_CREDS = 'adminuser.txt'
    # AWS_BUCKET_DOWNLOAD = 'robotfilmmaker-models'
    # AWS_KEY = 'trained.xml'

    # try:
    #     file = open(AWS_CREDS,'r')
    #     creds = file.readlines()
    #     for i in range(0, len(creds)):
    #         curr = creds[i]
    #         newline_index = curr.find('\n')
    #         if newline_index != -1:
    #             creds[i] = curr[0:newline_index]

    #     file.close()

    # except IOError:
    #     print('Error: Cannot read s3creds.txt')
    #     quit()

    # # Open boto resource/bucket
    # s3 = boto3.resource(
    #     's3',
    #     aws_access_key_id = creds[0],
    #     aws_secret_access_key = creds[1]
    # )

    # bucket_dl = s3.Bucket(AWS_BUCKET_DOWNLOAD)

    # try:
    #     path = os.curdir
    #     if not os.path.exists(path):
    #         os.makedirs(path)
    #     bucket_dl.download_file(AWS_KEY, path + "/trained.xml")

    # except botocore.exceptions.ClientError as e:
    #     if e.response['Error']['Code'] == "404":
    #         print("The object does not exist.")
    #     else:
    #         raise

    # print('XML file retrieved')

    ###################################################################
    #TRACK
    ###################################################################
    from cv2 import face
    model = face.FisherFaceRecognizer_create()

    names = ['Kevin', 'Target']
    fn_dir = os.getcwd() + '/Faces'
    (images, lables, names, id) = ([], [], {}, 0)
    for (subdirs, dirs, files) in os.walk(fn_dir):
        for subdir in dirs:
            names[id] = subdir
            print (subdir)
            id += 1
    model.read('trained.xml')
    face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
    flag = 0
    size = 5
    (im_width, im_height) = (125, 125)
    webcam = cv2.VideoCapture(1)
    start = time.time()
    target = 0
    while True:
        (rval, frame) = webcam.read()
        height, width = frame.shape[:2]
        # print(height)
        # print(width)
        desired_center = numpy.array([width / 2, height / 2])
        frame = cv2.flip(frame, 1, 0)
        # out.write(frame)
        # cv2.imshow(frame)
        if (flag % 10 == 0):
            labl = []
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            mini = cv2.resize(gray, (int(gray.shape[1] / size), int(gray.shape[0] / size)))
            faces = face_cascade.detectMultiScale(gray, 1.3, 5)
            for (x, y, w, h) in faces:
                face = gray[y:y + h, x:x + w]
                face_resize = cv2.resize(face, (im_width, im_height))
                otsu = cv2.adaptiveThreshold(face_resize, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 11, 2)

                # Try to recognize the face
                prediction = model.predict(otsu)
                # cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 3)
                # print (prediction[1])
                (dirX, dirY) = ("", "")
                if (flag % 11 == 0):
                    center = numpy.array([x + (w / 2), y + (h / 2)])
                    movement = desired_center - center
                    # length_face = x + w;
                    # width_face = y +h;
                    # ensure there is significant movement in the
                    if numpy.abs(movement[0]) > 50:
                        if movement[0] > 0:
                            dirX = "East"
                            arduinoSerial.write(bytes('r', 'UTF-8'))
                            # time.sleep(2)
                            print ('r')
                        else:
                            dirX = "West"
                            arduinoSerial.write(bytes('l', 'UTF-8'))
                            # time.sleep(2)
                            print ('l')
                    if numpy.abs(movement[1]) > 50:
                        if movement[1] > 0:
                            dirY = "North"
                            arduinoSerial.write(bytes('u', 'UTF-8'))
                            # time.sleep(2)
                            print ('u')
                        else:
                            dirY = "South"
                            arduinoSerial.write(bytes('d', 'UTF-8'))
                            # time.sleep(2)
                            print ('d')
                    # if numpy.abs(length_face) < height/3 or numpy.abs(width_face) < width/3:
                    #     arduinoSerial.write(bytes('f', 'UTF-8'))
                    #     print ('f')

                    # if numpy.abs(length_face) > height/3 or numpy.abs(width_face) > width/3:
                    #     arduinoSerial.write(bytes('b', 'UTF-8'))
                    #     print ('b')

                # Write the name of recognized face
                name = names[prediction[0]]
                if prediction[1] < 3000:
                    cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 3)
                    cv2.putText(frame, '%s - %.0f' % (name, prediction[1]), (x - 10, y - 10), cv2.FONT_HERSHEY_PLAIN, 1,
                                (0, 255, 0))
                    labl.append(name)
                    target = 1
                else:
                    # cv2.putText(frame, name,(x-10, y-10), cv2.FONT_HERSHEY_PLAIN,1,(0, 255, 0))
                    # labl.append(name)
                    target = 0
        else:
            #print (target)
            if target == 1:
                for i in range(len(faces)):
                    face_i = faces[i]
                    track_window = (x, y, w, h)

                    # set up the ROI for tracking
                    roi = frame[y:y + h, x:x + w]
                    hsv_roi = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)
                    lower_skin = numpy.array((0, 48, 80))
                    upper_skin = numpy.array((20, 255, 255))
                    mask = cv2.inRange(hsv_roi, lower_skin, upper_skin)
                    roi_hist = cv2.calcHist([hsv_roi], [0], mask, [180], [0, 180])
                    cv2.normalize(roi_hist, roi_hist, 0, 255, cv2.NORM_MINMAX)

                    # Setup the termination criteria, either 10 iteration or move by atleast 1 pt
                    term_crit = (cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 1)
                    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
                    dst = cv2.calcBackProject([hsv], [0], roi_hist, [0, 180], 1)

                    # apply meanshift to get the new location
                    ret, track_window = cv2.meanShift(dst, track_window, term_crit)

                    # Draw it on image
                    x, y, w, h = track_window

                    cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 3)
                    # cv2.putText(frame, "{},{}".format(dirX, dirY), (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.65, (0, 0, 255), 3)
                    # cv2.putText(frame, "dx: {}, dy: {}".format(movement[0], movement[1]), (10, frame.shape[0] - 10),
                    #             cv2.FONT_HERSHEY_SIMPLEX, 0.35, (0, 0, 255), 1)
                    # # cv2.putText(frame, labl[i], (x - 10, y - 10), cv2.FONT_HERSHEY_PLAIN,2,(255,255,255))
                    cv2.putText(frame, 'Target', (x - 10, y - 10), cv2.FONT_HERSHEY_PLAIN, 2, (255, 255, 255))

        cv2.imshow('Test', frame)
        # out.write(frame)
        flag = flag + 1
        key = cv2.waitKey(10)
        # if Esc key is press then break out of the loop
        if key == 27:
            webcam.release()
            # out.release()
            break

    end = time.time()
    seconds = end - start
    print ("Time taken : {0} seconds".format(seconds))
    print (flag)

    # Calculate frames per second
    fps = flag / seconds
    print ("Estimated frames per second : {0}".format(fps))
