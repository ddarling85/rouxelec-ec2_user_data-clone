import boto3
import time
import json
import subprocess

ec2 = boto3.resource('ec2', region_name='ca-central-1')
client = boto3.client('ec2', region_name='ca-central-1')
dynamodb = boto3.resource('dynamodb', region_name='ca-central-1')

cidr_range_table = dynamodb.Table('cidr_range_table')
response = cidr_range_table.scan()
for item in response['Items']:
    print(item)
    ip=item.get('ec2_ip_address')
    vpc_name=item.get('id')
    if not ip is None:
        out = subprocess.Popen(['ping', ip, '-n', '1', '-w', '1'], 
           stdout=subprocess.PIPE, 
           stderr=subprocess.STDOUT)
        stdout,stderr = out.communicate()
        response = cidr_range_table.update_item(
            Key={
                'id': "the_defaut"
            },
            UpdateExpression="SET ping_from_"+str(ip.replace('.',"_"))+" = :r",
            ExpressionAttributeValues={
                ':r':  str(stdout),
            },
            ReturnValues="UPDATED_NEW"
        )
