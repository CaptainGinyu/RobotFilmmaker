# EXAMPLE OF BUCKET COMMANDS

import boto3
import botocore
import os.path
import sys

if __name__ == '__main__':
    ##########################################
    #CREDENTIALS AND RESOURCE OPENING
    ##########################################
    #Get credentials
    # adminuser has two lines: first line is access key, seconds line is secret key
    AWS_CREDS = 'adminuser.txt'
    AWS_BUCKET_UPLOAD = 'robotfilmmaker-signals'
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

    ##########################################
    #BULK UPLOAD: Upload images
    ##########################################
    for root,dirs,files in os.walk('./Meeko'):
        for myfile in files:
            s3.meta.client.upload_file(os.path.join(root,myfile),AWS_BUCKET_UPLOAD,os.path.join('Meeko/',myfile))

    raw_input('Finished uploading, press enter to continue')

    ##########################################
    #BULK DOWNLOAD: Download back same images
    ##########################################
    bucket_dl = s3.Bucket(AWS_BUCKET_UPLOAD)

    for myfile in bucket_dl.objects.all():
        bucket_dl.download_file(myfile.key, os.curdir + "/" + myfile.key)

    raw_input('Finished downloading same images, press enter to continue')

    ##########################################
    #SPECIFIC DOWNLOAD: Download single xml file
    ##########################################
    bucket_dl = s3.Bucket(AWS_BUCKET_DOWNLOAD)

    try:
        bucket_dl.download_file(AWS_KEY, os.curdir + "/XML/trained.xml")

    except botocore.exceptions.ClientError as e:
        if e.response['Error']['Code'] == "404":
            print("The object does not exist.")
        else:
            raise

    raw_input('Finished downloading xml, press enter to continue')

    ##########################################
    #EMPTY BUCKET: Empty entire bucket
    ##########################################
    bucket_empty = s3.Bucket(AWS_BUCKET_UPLOAD)

    for myfile in bucket_empty.objects.all():
        myfile.delete()

    raw_input('Finished deleting bucket, press enter to continue')

    ##########################################
    #EMPTY FOLDER: Empty specific folder of bucket
    ##########################################
    bucket_empty = s3.Bucket(AWS_BUCKET_UPLOAD)

    for myfile in bucket_empty.objects.filter(Prefix='Target/'):
        myfile.delete()