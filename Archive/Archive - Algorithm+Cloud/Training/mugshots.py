import cv2
import sys
import os, time

#
# if len(sys.argv) != 2:
#     print('Please provide ONE name as an argument')
#     sys.exit()

size = 4
webcam = cv2.VideoCapture(1) #Use camera 0
count = []
add=0
#subject = sys.argv[1]
subject = 'Target'

folder = '../' + subject

if not os.path.exists(folder):
    os.makedirs(folder)

# We load the xml file
classifier = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

while True:
    (rval, im) = webcam.read()
    im=cv2.flip(im,1,0) #Flip to act as a mirror
    # Resize the image to speed up detection
    mini = cv2.resize(im, (int(im.shape[1] / size), int(im.shape[0] / size)))

    # detect MultiScale / faces 
    faces = classifier.detectMultiScale(mini)

    # Draw rectangles around each face
    for f in faces:
        (x, y, w, h) = [v * size for v in f] #Scale the shapesize backup
        
        #Save just the rectangle faces in SubRecFaces
        sub_face = im[y:y+h, x:x+w]
        if str(y) not in count: 
            count.append(str(y))
            add= add+1

        FaceFileName = folder + '/Image_' + str(add)+ '.jpg'
        cv2.imwrite(FaceFileName, sub_face)
        # if str(y) not in count: 
        #     count.append(str(y))

        cv2.rectangle(im, (x, y), (x + w, y + h),(0,255,0),thickness=4)

    # Show the image
    cv2.imshow('Training Set Generator',   im)
    key = cv2.waitKey(10)
    # if Esc key is press then break out of the loop 
    if key == 27 or len(count) > 34: #The Esc key or samples more than 20
        break

cv2.destroyAllWindows()
webcam.release()
