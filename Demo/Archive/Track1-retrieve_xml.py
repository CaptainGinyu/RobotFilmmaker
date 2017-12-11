import boto3
import botocore
import os
import sys

if __name__ == '__main__':
    ##########################################
    #CREDENTIALS AND RESOURCE OPENING
    ##########################################
    #Get credentials
    # adminuser has two lines: first line is access key, seconds line is secret key
    AWS_CREDS = 'adminuser.txt'
    AWS_BUCKET_DOWNLOAD = 'robotfilmmaker-models'
    AWS_KEY = 'trained.xml'

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
