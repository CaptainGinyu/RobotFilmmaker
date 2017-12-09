# AUTHORS: Philip, Harshil
# DESCRIPTION:
# This is the training module for RobotFilmmaker
# Takes mugshots, uploads them to AWS buckets, and does training to generate an XML in a bucket


###################################################################
# IMPORT
###################################################################
import cv2
import os
import boto3

###################################################################
# PARAMETERS
###################################################################
WEBCAM_PORT = 1                     # Webcam port
N_SAMPLES = 40                      # Number of sample mugshots to take
KEY_BREAK = 27                      # Break key (27 = escape)
UPLOAD_KEVIN = 0                    # Upload the nontarget, Kevin :)
FOLDER_TARGET = '/Faces/Target'     # Folder for storing mugshots (relative to current directory)
FOLDER_KEVIN = '/Faces/Kevin'       # Folder for nontarget, Kevin :)

# AWS parameters
# AWS_CREDS should be a text file with two lines: first line is access key, seconds line is secret key
AWS_CREDS = 'adminuser.txt'
AWS_BUCKET_UPLOAD = 'robotfilmmaker-mugshots'   # Bucket name to upload to
AWS_INSTANCE_ID = 'i-01608966e12056364'         # Instance ID with training script

###################################################################
# LOAD WEBCAM AND SETUP
###################################################################
webcam = cv2.VideoCapture(WEBCAM_PORT)  # Use camera 0
count = []                              # Mugshots count
add = 0

folder = os.getcwd() + FOLDER_TARGET    # Setup folder to save mugshots
print (os.getcwd())

if not os.path.exists(folder):
    os.makedirs(folder)

# We load the xml file
classifier = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
size = 4

###################################################################
# RUN MUGSHOTS UNTIL BREAK
###################################################################
while True:
    (rval, im) = webcam.read()                                                  # Read frame
    im = cv2.flip(im, 1, 0)                                                     # Flip to act as a mirror
    mini = cv2.resize(im, (int(im.shape[1] / size), int(im.shape[0] / size)))   # Resize the image to speed up detection

    # Detect MultiScale / faces
    faces = classifier.detectMultiScale(mini)

    # Draw rectangles around each face
    for f in faces:
        (x, y, w, h) = [v * size for v in f]  # Scale the shapesize backup

        # Save just the rectangle faces in SubRecFaces
        sub_face = im[y:y + h, x:x + w]
        if str(y) not in count:
            count.append(str(y))
            add = add + 1

        print(add)
        FaceFileName = folder +'/Image_' + str(add) + '.jpg'
        cv2.imwrite(FaceFileName, sub_face)

        cv2.rectangle(im, (x, y), (x + w, y + h), (0, 255, 0), thickness=4)

    # Show the image
    cv2.imshow('Training Set Generator', im)

    # Break if key is pressed or samples more than X
    key = cv2.waitKey(10)
    # if Esc key is press then break out of the loop
    if key == KEY_BREAK or len(count) > N_SAMPLES:  # The Esc key or samples more than 20
        break

# Cleanup
cv2.destroyAllWindows()
webcam.release()

###################################################################
# UPLOAD MUGSHOTS
###################################################################
try:
    file_creds = open(AWS_CREDS,'r')
    creds = file_creds.readlines()
    for i in range(0, len(creds)):
        curr = creds[i]
        newline_index = curr.find('\n')
        if newline_index != -1:
            creds[i] = curr[0:newline_index]

    file_creds.close()

except IOError:
    print('Error: Cannot read s3creds.txt')
    quit()

# Open boto resource/bucket
s3 = boto3.resource(
    's3',
    aws_access_key_id = creds[0],
    aws_secret_access_key = creds[1]
)

# Open SSM client for EC2
ssm_client = boto3.client(
    'ssm',
    aws_access_key_id = creds[0],
    aws_secret_access_key = creds[1],
    region_name = 'us-east-1'
)

# Empty bucket
bucket_mugshots = s3.Bucket(AWS_BUCKET_UPLOAD)

for myfile in bucket_mugshots.objects.filter(Prefix='Target/'):
    myfile.delete()

folder_target = os.getcwd() + FOLDER_TARGET

print("Uploading /Faces/Target")
# Upload target folder
for root,dirs,files in os.walk(folder_target):
    for myfile in files:
        s3.meta.client.upload_file(os.path.join(root,myfile),AWS_BUCKET_UPLOAD,os.path.join('Target/',myfile))

folder_target = os.getcwd() + FOLDER_KEVIN
if UPLOAD_KEVIN:
    print("Uploading /Faces/Kevin")
    # Upload target folder
    for root,dirs,files in os.walk(folder_target):
        for myfile in files:
            s3.meta.client.upload_file(os.path.join(root,myfile),AWS_BUCKET_UPLOAD,os.path.join('Kevin/',myfile))

print("Uploading complete!")

####################################################################
# GENERATE XML
####################################################################
commands = ['sh /home/ec2-user/robotfilmmaker/starttraining.sh']
instance_ids = [AWS_INSTANCE_ID]

response = ssm_client.send_command(
    DocumentName="AWS-RunShellScript",
    Parameters={'commands':commands},
    InstanceIds=instance_ids
)

print('Successful xml file creation')