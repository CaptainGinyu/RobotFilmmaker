import cv2, sys, numpy, os
import time
#import _thread
from cv2 import face
# import pickle

labl = []
size = 5
face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
fn_dir = os.getcwd() + '/Faces'
# fn_dir = '/Users/harshilprajapati/Desktop/Boston University/Semester 1/Product Design in ECE/RobotFilmMaker/RobotFilmmaker/Cloud+RPi/faces'
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
model.write('localtrained.xml')