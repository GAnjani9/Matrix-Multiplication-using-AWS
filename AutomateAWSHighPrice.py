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

# try:
#     response = ec2_client.create_security_group(GroupName='HPSG',
#                                                 Description='DESCRIPTION',
#                                                 VpcId=vpc_id)
#     print(response['GroupId'])
#     security_group_id = response['GroupId']
#     print('Security Group Created %s in vpc %s.' % (security_group_id, vpc_id))
#     security_group_id=str(security_group_id)

#     data = ec2_client.authorize_security_group_ingress(GroupId=security_group_id,
#                                                         IpPermissions=[
#                                                             {'IpProtocol': 'tcp',
#                                                              'FromPort': 80,
#                                                              'ToPort': 80,
#                                                              'IpRanges': [{'CidrIp': '0.0.0.0/0'}]},
#                                                             {'IpProtocol': 'tcp',
#                                                              'FromPort': 22,
#                                                              'ToPort': 22,
#                                                              'IpRanges': [{'CidrIp': '0.0.0.0/0'}]}
#                                                         ])
#     print('Ingress Successfully Set %s' % data)
# except ClientError as e:
#     print(e)



aws_key = 'XXXXXXXXXXXXX'
aws_secret = 'XXXXXXXXXXXXX'

ec2 = boto3.resource('ec2', aws_access_key_id=aws_key,
                     aws_secret_access_key=aws_secret,region_name='ap-south-1')

# Launching new instances requires an image ID and the number of instances to launch.
# It can also take several optional parameters, such as the instance type and security group:
# inst = ec2.create_instances(ImageId='ami-0c1a7f89451184c8b', MinCount=1, MaxCount=1, InstanceType='c4.4xlarge',KeyName='CloudComputingProject',
# 	NetworkInterfaces=[{ 'DeviceIndex': 0, 'AssociatePublicIpAddress': True,'Groups': [security_group_id]}])
# insta = inst[0]

# # # Wait for the instance to enter the running state
# insta.wait_until_running()
# # # Reload the instance attributes
# insta.load()

# time.sleep(60)
instances = ec2.instances.filter(Filters=[{'Name': 'instance-state-name', 'Values': ['running']}])
# pdn=[]
# for instance in instances:
# 	pdn.append(instance.public_dns_name)
# print(pdn)
# pdn[0]=str("ubuntu@"+pdn[0])


# for instance in instances:
#     cmd1 = "ssh -i CloudComputingProject.pem " + "ubuntu@" + str(instance.public_dns_name)
#     cmdList = [cmd1 + " mkdir AnjaniCloud",
#                cmd1 + " sudo apt-get update",
#                cmd1 + " sudo apt-get install g++",
#                " scp -i CloudComputingProject.pem MatrixMutliplication.cpp " + "ubuntu@" + str(instance.public_dns_name) + ":~/AnjaniCloud/",
#                cmd1 + " g++ AnjaniCloud/MatrixMutliplication.cpp",
#                cmd1 + " ./a.out"]
#     for cmd in cmdList:
#         returned_value = os.system(cmd)  # returns the exit code in unix
#         print('returned value:', returned_value)
# call = subprocess.check_output(["ssh", "-i", "CloudComputingProject.pem", pdn[0]], stderr=subprocess.PIPE)
# for line in call:
#     print(call.stdout)

# returned_value1 = os.system(cmd1)  # returns the exit code in unix
# print('returned value:', returned_value1)

# call = subprocess.check_output(["exit"], stderr=subprocess.PIPE)
# time.sleep(10)




ids=[]
instances = ec2.instances.filter(Filters=[{'Name': 'instance-state-name', 'Values': ['running']}])
for instance in instances:
	ids.append(instance.id)
ec2.instances.filter(InstanceIds=ids).stop()
ec2.instances.filter(InstanceIds=ids).terminate()
