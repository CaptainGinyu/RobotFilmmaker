import cv2, sys, numpy, os
import time
import boto3, botocore
from cv2 import face

fn_dir = '/home/ec2-user/robotfilmmaker/temp-mugshots'
AWS_BUCKET_DOWNLOAD = 'robotfilmmaker-mugshots'

print('Downloading from S3...')
s3 = boto3.resource('s3')
bucket_dl = s3.Bucket(AWS_BUCKET_DOWNLOAD)

for myfile in bucket_dl.objects.all():
    bucket_dl.download_file(myfile.key, fn_dir + "/" + myfile.key)


print('Training...')

(images, labels, names, id) = ([], [], {}, 0)
for (subdirs, dirs, files) in os.walk(fn_dir):
    for subdir in dirs:
        names[id] = subdir
        subjectpath = os.path.join(fn_dir, subdir)
        for filename in os.listdir(subjectpath):
            if filename.startswith('I'):
                path = subjectpath + '/' + filename
                label = id
                ximg=cv2.imread(path, 0)
                ximg=cv2.resize(ximg,(125,125))
                otsu = cv2.adaptiveThreshold(ximg,255,cv2.ADAPTIVE_THRESH_MEAN_C,cv2.THRESH_BINARY,11,2)
                images.append(otsu)
                labels.append(int(label))
        id += 1
(im_width, im_height) = (125, 125)
#print(labels)

(images, labels) = [numpy.array(lis) for lis in [images, labels]]

model = cv2.face.createFisherFaceRecognizer()
model.train(images, labels)
model.save('/home/ec2-user/robotfilmmaker/robotfilmmaker-models/trained.xml')

print('XML created')
