import cv2, sys, numpy, os
import time
import boto3, botocore
from cv2 import face

fn_dir = "/home/ec2-user/robotfilmmaker/Faces"
xml_dir = "/home/ec2-user/robotfilmmaker"
AWS_BUCKET_DOWNLOAD = "robotfilmmaker-mugshots"
AWS_BUCKET_UPLOAD = "robotfilmmaker-models"

#########################################################################
# GET MUGSHOTS FROM S3 BUCKET PHOTOS
#########################################################################
print('Downloading mugshots...')
s3_dl = boto3.resource('s3')

bucket_dl = s3_dl.Bucket(AWS_BUCKET_DOWNLOAD)

for myfile in bucket_dl.objects.all():
    if not myfile.key.endswith('/'):
        message = bucket_dl.download_file(myfile.key, fn_dir + '/' + myfile.key)

#########################################################################
# DO TRAINING
#########################################################################
print('Training...')
(images, labels, names, id) = ([], [], {}, 0)
for (subdirs, dirs, files) in os.walk(fn_dir):
    for subdir in dirs:
        names[id] = subdir

        subjectpath = os.path.join(fn_dir, subdir)
        for filename in sorted(os.listdir(subjectpath)):
            if filename.startswith('I'):
                path = subjectpath + '/' + filename
                # print(path)
                label = id
                ximg = cv2.imread(path, 0)
                ximg = cv2.resize(ximg, (125, 125))
                otsu = cv2.adaptiveThreshold(ximg, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 11, 2)
                images.append(otsu)
                labels.append(int(label))
        id += 1
(im_width, im_height) = (125, 125)
# print(labels)

(images, labels) = [numpy.array(lis) for lis in [images, labels]]

# Train and save
model = face.FisherFaceRecognizer_create()
model.train(images, labels)
model.write('trained.xml')

#########################################################################
# PUT IN S3 MODEL BUCKET
#########################################################################
print('Uploading XML...')
s3_ul = boto3.resource('s3')

s3_ul.meta.client.upload_file(xml_dir + '/trained.xml', AWS_BUCKET_UPLOAD, 'trained.xml')