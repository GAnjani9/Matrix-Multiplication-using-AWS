import boto3
import subprocess
import os
import time
from botocore.exceptions import ClientError
#import resources

ec2_client = boto3.client('ec2')

response = ec2_client.describe_vpcs()
vpc_id = response.get('Vpcs', [{}])[0].get('VpcId', '')
print(vpc_id)

try:
    response = ec2_client.create_security_group(GroupName='test1',
                                         Description='DESCRIPTION',
                                         VpcId=vpc_id)
    print(response['GroupId'])
    security_group_id = response['GroupId']
    print('Security Group Created %s in vpc %s.' % (security_group_id, vpc_id))
    security_group_id=str(security_group_id)

    data = ec2_client.authorize_security_group_ingress(
        GroupId=security_group_id,
        IpPermissions=[
            {'IpProtocol': 'tcp',
             'FromPort': 80,
             'ToPort': 80,
             'IpRanges': [{'CidrIp': '0.0.0.0/0'}]},
            {'IpProtocol': 'tcp',
             'FromPort': 22,
             'ToPort': 22,
             'IpRanges': [{'CidrIp': '0.0.0.0/0'}]}
        ])
    print('Ingress Successfully Set %s' % data)
except ClientError as e:
    print(e)



aws_key='AKIAIFHPZJG6ALBUQR2Q'
aws_secret='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'
ec2 = boto3.resource('ec2', aws_access_key_id=aws_key,
                     aws_secret_access_key=aws_secret,region_name='us-east-2')

# Launching new instances requires an image ID and the number of instances to launch.
# It can also take several optional parameters, such as the instance type and security group:
inst=ec2.create_instances(ImageId='ami-0653e888ec96eab9b', MinCount=1, MaxCount=1, InstanceType='t2.micro',KeyName='Cloud_Computing',
	NetworkInterfaces=[{ 'DeviceIndex': 0, 'AssociatePublicIpAddress': True,'Groups': [security_group_id]}])
insta = inst[0]

# Wait for the instance to enter the running state
insta.wait_until_running()
# Reload the instance attributes
insta.load()

time.sleep(60)
instances = ec2.instances.filter(Filters=[{'Name': 'instance-state-name', 'Values': ['running']}])
pdn=[]
for instance in instances:
	pdn.append(instance.public_dns_name)
print(pdn)
pdn[0]=str("ubuntu@"+pdn[0])



cmd = "ssh -i Cloud_Computing.pem "+pdn[0]

returned_value = os.system(cmd)  # returns the exit code in unix
print('returned value:', returned_value)


ids=[]
instances = ec2.instances.filter(Filters=[{'Name': 'instance-state-name', 'Values': ['running']}])
for instance in instances:
	ids.append(instance.id)
ec2.instances.filter(InstanceIds=ids).stop()
ec2.instances.filter(InstanceIds=ids).terminate()