# EXAMPLE OF SEND_COMMAND

import boto3
import pprint

if __name__ == '__main__':
    #adminuser has two lines: first line is access key, seconds line is secret key
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

    #commands = ['cd /home/ec2-user','sh start.sh']
    commands = ['sh /home/ec2-user/start.sh']
    instance_ids = ['i-0e2b18570ed94a64e']

    response = ssm_client.send_command(
        DocumentName="AWS-RunShellScript",
        Parameters={'commands':commands},
        InstanceIds=instance_ids
    )
