import cv2
import boto3
from botocore.client import Config
import datetime

# Note: You need to put a txt file named s3creds.txt in the same directory as this file
# s3creds.txt should contain 3 lines:
# First line is your AWS access key ID
# Second line is your secret access key
# Third line is the name of the bucket

if __name__ == '__main__':

    try:
        file = open('s3creds.txt', 'r')
        creds = file.readlines()
        for i in range(0, len(creds)):
            curr = creds[i]
            newline_index = curr.find('\n')
            if newline_index != -1:
                creds[i] = curr[0:newline_index]

        file.close()
                
    except FileNotFoundError:
        print('s3creds.txt file not found')
        quit()

    curr_date = datetime.datetime.now().strftime('%m-%d-%Y')
    vid_name = 'movie-' + curr_date + '.avi'
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print('Cannot open camera')
        quit()

    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    vid_file = cv2.VideoWriter(vid_name, fourcc, 8.0, (640, 480))

    while True:
        ret, frame = cap.read()

        cv2.imshow('Robot Filmmaker', frame)
        vid_file.write(frame)

        pressed_key = cv2.waitKey(100)

        if pressed_key == 27:
            break

    cv2.destroyAllWindows()
    cap.release()
    vid_file.release()

    print('About to upload to S3...')
    data = open(vid_name, 'rb')
    s3 = boto3.resource('s3', aws_access_key_id = creds[0], aws_secret_access_key = creds[1], config = Config(signature_version = 's3v4'))
    s3.Bucket(creds[2]).put_object(Key = vid_name, Body = data)
    print('Uploaded!')
    
