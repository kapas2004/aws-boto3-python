import json
from botocore.vendored import requests
import boto3
import time

# e.g. eu-west-1
tagKey='tag:MonthlyPatch'
tagValue='True'
region = 'ap-southeast-2'
ec2 = boto3.client('ec2', region_name=region)

custom_filter = [{
    'Name': tagKey, 
    'Values': [tagValue]}]



def lambda_handler(event, context):
    reboot_instance()
    return {
        'statusCode': 200,
        'body': json.dumps('Restarted instances')
    }

def reboot_instance():  
    instances = ec2.describe_instances(Filters=custom_filter)["Reservations"]
    count = 0
    for instanceId in instances:
        InstanceID=instanceId['Instances'][0]['InstanceId']
        ec2.reboot_instances(InstanceIds=[InstanceID])
        instance_name = get_tag_name(instanceId['Instances'][0])
        print("Rebooting started for Server " + instance_name + ", InstanceID " + InstanceID)
        count += 1
    print("Total Servers rebooted " + str(count))

def get_tag_name(instanceId):
    instanceName = ''
    for tags in instanceId['Tags']:
        if tags["Key"] == 'Name':
                instanceName = tags["Value"]
                return instanceName
    return 'null'