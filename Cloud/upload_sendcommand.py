# Sends command to instance to start a python script

import boto3

if __name__ == '__main__':
    ##########################################
    #CREDENTIALS AND RESOURCE OPENING
    ##########################################
    #Get credentials:
    #adminuser.txt has two lines: first line is access key, seconds line is secret key
    try:
        file = open('adminuser.txt','r')
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


    ssm_client = boto3.client(
        'ssm',
        aws_access_key_id = creds[0],
        aws_secret_access_key = creds[1]
    )

    ##########################################
    #START SCRIPT
    ##########################################
    commands = ['sh /home/ec2-user/robotfilmmaker/starttraining.sh']
    instance_ids = ['i-09cdfca3b64d75b0e']

    response = ssm_client.send_command(
        DocumentName="AWS-RunShellScript",
        Parameters={'commands':commands},
        InstanceIds=instance_ids
    )

    print(response)