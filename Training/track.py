import cv2, sys, numpy, os
import time
import _thread
from cv2 import face

labl = []
size = 5
face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
fn_dir = '/Users/harshilprajapati/Desktop/Boston University/Semester 1/Product Design in ECE/RobotFilmMaker/RobotFilmmaker/Training/att_faces'
flag =0

print('Training...')

(images, lables, names, id) = ([], [], {}, 0)
for (subdirs, dirs, files) in os.walk(fn_dir):
    for subdir in dirs:
        names[id] = subdir
        subjectpath = os.path.join(fn_dir, subdir)
        for filename in os.listdir(subjectpath):
            if filename.startswith('I'):
                path = subjectpath + '/' + filename
                #print(filename)
                lable = id
                ximg=cv2.imread(path, 0)
                ximg=cv2.resize(ximg,(125,125))
                otsu = cv2.adaptiveThreshold(ximg,255,cv2.ADAPTIVE_THRESH_MEAN_C,cv2.THRESH_BINARY,11,2)
                images.append(otsu)
                lables.append(int(lable))
        id += 1
(im_width, im_height) = (125, 125)
#print(lables)

(images, lables) = [numpy.array(lis) for lis in [images, lables]]

model = face.FisherFaceRecognizer_create()

model.train(images, lables)
webcam = cv2.VideoCapture(0)
start  = time.time()
while True:
    (rval, frame) = webcam.read()
    frame=cv2.flip(frame,1,0)
    #cv2.imshow(frame)
    if (flag%10==0):
        labl = []
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        #gray = cv2.resize(gray,im_height,im_width)
        mini = cv2.resize(gray, (int(gray.shape[1] / size), int(gray.shape[0] / size)))
        faces = face_cascade.detectMultiScale(gray, 1.3, 5)
        for (x,y,w,h) in faces:
            face = gray[y:y + h, x:x + w]
            face_resize = cv2.resize(face, (im_width, im_height))
            otsu = cv2.adaptiveThreshold(face_resize,255,cv2.ADAPTIVE_THRESH_MEAN_C,cv2.THRESH_BINARY,11,2)

            # Try to recognize the face
            prediction = model.predict(otsu)
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 3)
            print (prediction[1])

        # Write the name of recognized face
            if prediction[1]<3000:
                cv2.putText(frame,'%s - %.0f' % (names[prediction[0]],prediction[1]),(x-10, y-10), cv2.FONT_HERSHEY_PLAIN,1,(0, 255, 0))
                labl.append(names[prediction[0]])
            else:
                cv2.putText(frame,'Unknown',(x-10, y-10), cv2.FONT_HERSHEY_PLAIN,1,(0, 255, 0))
                labl.append(names[prediction[0]])
    else:
        for i in range(len(faces)):
            face_i = faces[i]
            #x,h,y,w = 250,90,400,125  # simply hardcoded the values
            #(x, y, w, h) = [v * size for v in face_i]
            track_window = (x,y,w,h)
    
        # set up the ROI for tracking
            roi = frame[y:y+h, x:x+w]
            hsv_roi =  cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)
            #print (hsv_roi.shape)
            #low= numpy.uint8([[[189,224,255]]])
            #high = numpy.uint8([[[134,192,234]]])
            #lower_skin = cv2.cvtColor(low ,cv2.COLOR_BGR2HSV)
            #upper_skin = cv2.cvtColor(high,cv2.COLOR_BGR2HSV)
            lower_skin = numpy.array((0, 48, 80))
            upper_skin = numpy.array((20, 255, 255))
            #lower_skin = numpy.array([0, 48, 80], dtype = "uint8")#((32,25.9,100)) #, dtype = "uint8"
            #upper_skin = numpy.array([20, 255, 255], dtype = "uint8") #((35,42.7,91.9))
            mask = cv2.inRange(hsv_roi,lower_skin,upper_skin)
            #mask = cv2.inRange(hsv_roi,numpy.array((0., 60.,32.)), numpy.array((180.,255.,255.)))
            #lower = np.array([0, 48, 80], dtype = "uint8")
            #upper = np.array([20, 255, 255], dtype = "uint8")
            #mask = cv2.inRange(hsv_roi,cv2.cvtColor(lower_skin, cv2.COLOR_BGR2HSV),cv2.cvtColor(upper_skin,cv2.COLOR_BGR2HSV))
            roi_hist = cv2.calcHist([hsv_roi],[0],mask,[180],[0,180])
            cv2.normalize(roi_hist,roi_hist,0,255,cv2.NORM_MINMAX)

        # Setup the termination criteria, either 10 iteration or move by atleast 1 pt
            term_crit = ( cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 1 )
            hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
            dst = cv2.calcBackProject([hsv],[0],roi_hist,[0,180],1)
    
        # apply meanshift to get the new location
            ret, track_window = cv2.meanShift(dst, track_window, term_crit)
    
        # Draw it on image
            x,y,w,h = track_window
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 3)
            cv2.putText(frame, labl[i], (x - 10, y - 10), cv2.FONT_HERSHEY_PLAIN,2,(255,255,255))  

    cv2.imshow('Test',   frame)
    flag = flag + 1
    key = cv2.waitKey(10)
    # if Esc key is press then break out of the loop 
    if key == 27: #The Esc key
        break

end = time.time()
seconds = end - start
print ("Time taken : {0} seconds".format(seconds))
print (flag)
 
# Calculate frames per second
fps  = flag / seconds
print ("Estimated frames per second : {0}".format(fps))