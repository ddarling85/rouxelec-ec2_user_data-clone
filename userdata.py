import boto3
import time
import json
import subprocess

ec2 = boto3.resource('ec2', region_name='ca-central-1')
client = boto3.client('ec2', region_name='ca-central-1')
dynamodb = boto3.resource('dynamodb', region_name='ca-central-1')

cidr_range_table = dynamodb.Table('cidr_range_table')
response = cidr_range_table.scan()
ping_test="1 packets transmitted, 1 received, 0% packet loss"
for item in response['Items']:
    print(item)
    ip=item.get('ec2_ip_address')
    vpc_name=item.get('id')
    if not ip is None:
        out = subprocess.Popen(['ping', ip, '-n', '1', '-w', '1'], 
           stdout=subprocess.PIPE, 
           stderr=subprocess.STDOUT)
        stdout,stderr = out.communicate()
        result_ping="PING NOT OK"
        if ping_test in str(stdout):
            result_ping="PING OK"
        response = cidr_range_table.update_item(
            Key={
                'id': vpc_name
            },
            UpdateExpression="SET ping_from_"+str(ip.replace('.',"_"))+" = :r",            
            ExpressionAttributeValues={
                ':r':  result_ping,
            },
            ReturnValues="UPDATED_NEW"
        )
