import cv2, sys, numpy, os
import time
from cv2 import face

size = 5
face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

fn_dir = os.getcwd() + '\Faces'
flag = 0

print('Training...')

(images, labels, names, id) = ([], [], {}, 0)
for (subdirs, dirs, files) in os.walk(fn_dir):
    for subdir in dirs:
        names[id] = subdir
        subjectpath = os.path.join(fn_dir, subdir)
        for filename in os.listdir(subjectpath):
            if filename.startswith('I'):
                path = subjectpath + '/' + filename
                lable = id
                ximg=cv2.imread(path, 0)
                ximg=cv2.resize(ximg,(125,125))
                otsu = cv2.adaptiveThreshold(ximg,255,cv2.ADAPTIVE_THRESH_MEAN_C,cv2.THRESH_BINARY,11,2)
                images.append(otsu)
                labels.append(int(lable))
        id += 1
(im_width, im_height) = (125, 125)
#print(labels)

(images, labels) = [numpy.array(lis) for lis in [images, labels]]

model = cv2.face.FisherFaceRecognizer_create()
model.train(images, labels)
model.save('trained.xml')

print('XML generated')
