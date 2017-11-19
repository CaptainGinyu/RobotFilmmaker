# Uploads mugshots to bucket

import boto3
import botocore
import os.path

if __name__ == '__main__':
    ##########################################
    #CREDENTIALS AND RESOURCE OPENING
    ##########################################
    #Get credentials:
    #adminuser.txt has two lines: first line is access key, seconds line is secret key
    AWS_CREDS = 'adminuser.txt'
    AWS_BUCKET_UPLOAD = 'robotfilmmaker-mugshots'

    try:
        file = open(AWS_CREDS,'r')
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

    #Open boto resource/bucket
    s3 = boto3.resource(
        's3',
        aws_access_key_id = creds[0],
        aws_secret_access_key = creds[1]
    )

    ##########################################
    #EMPTY TARGET FOLDER: Empty target folder
    ##########################################
    bucket_mugshots = s3.Bucket(AWS_BUCKET_UPLOAD)

    for myfile in bucket_mugshots.objects.filter(Prefix='Target/'):
        myfile.delete()

    ##########################################
    #BULK UPLOAD: Upload images
    ##########################################
    for root,dirs,files in os.walk('/Users/harshilprajapati/Desktop/Boston University/Semester 1/Product Design in ECE/RobotFilmMaker/RobotFilmmaker/Cloud+RPi/faces/Target'):
        for myfile in files:
            s3.meta.client.upload_file(os.path.join(root,myfile),AWS_BUCKET_UPLOAD,os.path.join('Target/',myfile))
    for root,dirs,files in os.walk('/Users/harshilprajapati/Desktop/Boston University/Semester 1/Product Design in ECE/RobotFilmMaker/RobotFilmmaker/Cloud+RPi/faces/Unknown'):
        for myfile in files:
            s3.meta.client.upload_file(os.path.join(root,myfile),AWS_BUCKET_UPLOAD,os.path.join('Unknown/',myfile))