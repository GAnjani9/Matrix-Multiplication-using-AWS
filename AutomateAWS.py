import boto3
import subprocess
import os
import time
from botocore.exceptions import ClientError
#import resources

aws_key = 'XXXXXXXXXXXXX'
aws_secret = 'XXXXXXXXXXXXX'

def getEC2Client():
    print("Getting EC2 Client")
    ec2_client = boto3.client('ec2',
                              'ap-south-1',
                              aws_access_key_id=aws_key,
                              aws_secret_access_key=aws_secret,
                              use_ssl=False)
    return ec2_client

def getVPCId(ec2_client):
    print("Getting VPC ID")
    response = ec2_client.describe_vpcs()
    vpc_id = response.get('Vpcs', [{}])[0].get('VpcId', '')
    print("VPC being used:", vpc_id)
    return vpc_id

def createAndAuthorizeSecurityGroup(ec2_client, vpc_id, groupName):
    print("Creating and Loading security group")
    try:
        response = ec2_client.create_security_group(GroupName=groupName,
                                                    Description='DESCRIPTION',
                                                    VpcId=vpc_id)
        # print(response['GroupId'])
        security_group_id = response['GroupId']
        print('Security Group Created %s in VPC: %s.' % (security_group_id, vpc_id))
        security_group_id = str(security_group_id)

        data = ec2_client.authorize_security_group_ingress(GroupId=security_group_id,
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
        security_group_id = None
        print(e)

    return security_group_id

def checkAndWaitEC2InstanceReady(ec2Instances):
    instance_status_ok=False
    sysytem_status_ok=False

    while((instance_status_ok == False) or (sysytem_status_ok == False)):
        ec2Instance_Ids = []
        for ec2Instance in ec2Instances:
            ec2Instance_Ids.append(ec2Instance.id)
            print("Checking Instance status: " + str(ec2Instance.id))
        response2 = ec2Client.describe_instance_status(InstanceIds=ec2Instance_Ids)

        instance_status = response2['InstanceStatuses'][0]['InstanceStatus']['Status']
        system_status = response2['InstanceStatuses'][0]['SystemStatus']['Status']

        print("Instance Status:", response2['InstanceStatuses'][0]['InstanceStatus']['Status'])
        print("System Status:", response2['InstanceStatuses'][0]['SystemStatus']['Status'])
        if (instance_status == "ok"):
            instance_status_ok = True

        if (system_status == "ok"):
            sysytem_status_ok = True

        time.sleep(5)

def createAndLoadInstance(ec2Resource, ec2Client, security_group_id, ec2InstanceType):
    print("Creating and Loading Instance")
    # Launching new instances requires an image ID and the number of instances to launch.
    # It can also take several optional parameters, such as the instance type and security group:
    ec2Instances = ec2Resource.create_instances(ImageId = 'ami-0f5ee92e2d63afc18',
                                MinCount = 1,
                                MaxCount = 1,
                                InstanceType = ec2InstanceType,
                                KeyName = 'AshuCloudComputing',
                                NetworkInterfaces = [{ 'DeviceIndex': 0,
                                                     'AssociatePublicIpAddress': True,
                                                     'Groups': [security_group_id]}])
    ec2instance = ec2Instances[0]

    # Wait for the instance to enter the running state
    ec2instance.wait_until_running()
    # Reload the instance attributes
    ec2instance.load()

    checkAndWaitEC2InstanceReady(ec2Instances)

    return ec2instance

def getEC2Resource():
    print("Retrieving EC2 Resource object")
    ec2 = boto3.resource('ec2',
                         aws_access_key_id=aws_key,
                         aws_secret_access_key=aws_secret,
                         region_name='ap-south-1',
                         use_ssl=False)

    return ec2

def getPublicDNS(ec2Resource, instanceCreated):
    instances = ec2Resource.instances.filter(Filters=[{'Name': 'instance-state-name', 'Values': ['running']}])
    pdns = []
    runningInstanceCount = 0

    for instance in instances:
        runningInstanceCount = runningInstanceCount + 1

    if runningInstanceCount == 0:
        print("No Running Instance Found")
    else:
        print(str(runningInstanceCount) + " instances running")

        for instance in instances:
            if (instanceCreated == None):
                print("Running commands in already existing instance")
                pdns.append(instance.public_dns_name)
                print(pdns)
                break
            elif (instance == instanceCreated):
                print("Running commands in newly created instance")
                pdns.append(instance.public_dns_name)
                print(pdns)
                break


        if (len(pdns) == 0):
            print("Instances present but not in running state!")
            usrAtHost = None
        else:
            usrAtHost = str("ubuntu@" + pdns[0])
            print(usrAtHost)

    return usrAtHost

def runCommandInServer(ec2Resource, usrAtHost, terminateAfterExecute):
    print("Running Commands in server")

    cmd1 = 'ssh -i AshuCloudComputing.pem -o "StrictHostKeyChecking no" ' + usrAtHost
    # cmd1 = 'ssh -i AshuCloudComputing.pem ' + usrAtHost
    cmdList = [cmd1 + " mkdir AnjaniCloud",
               cmd1 + " sudo apt-get update --assume-yes",
               cmd1 + " sudo apt-get --assume-yes install g++",
               "scp -i AshuCloudComputing.pem MatrixMutliplication.cpp " + usrAtHost + ":~/AnjaniCloud/",
               cmd1 + " g++ AnjaniCloud/MatrixMutliplication.cpp",
               cmd1 + " ./a.out"]

    for cmd in cmdList:
        print("Running CMD " + cmd)
        returned_value = os.system(cmd)  # returns the exit code in unix
        if returned_value == 0:
            print("CMD ran successfully: " + cmd + "\n")
        else:
            print("CMD failed: ", cmd)

    # Stop and Terminate all Running instances
    if (terminateAfterExecute == True):
        stopAndTerminateInstances(ec2Resource)

def stopAndTerminateInstances(ec2Resource):
    ids = []
    instances = ec2Resource.instances.filter(Filters=[{'Name': 'instance-state-name', 'Values': ['running']}])
    for instance in instances:
        ids.append(instance.id)
        print("Terminating instance: " + str(instance.id))
    ec2Resource.instances.filter(InstanceIds=ids).stop()
    ec2Resource.instances.filter(InstanceIds=ids).terminate()


if __name__ == "__main__":

    # Define EC2 instance type
    ec2InstanceType = "t2.micro"

    # Define Group Name
    groupName = "test3"

    # Get EC2 Resource Object
    ec2Resource = getEC2Resource()

    # Get EC2 Client
    ec2Client = getEC2Client()

    # Get VPC ID
    vpcID = getVPCId(ec2Client)

    # Create And Authorize Security Group
    securityGroupId = createAndAuthorizeSecurityGroup(ec2Client, vpcID, groupName)

    ec2_instance = createAndLoadInstance(ec2Resource, ec2Client, securityGroupId, ec2InstanceType)

    # username@host string of running instances to connect to EC2 server using ssh
    usrAtHost   = getPublicDNS(ec2Resource, instanceCreated=ec2_instance)

    # Run Commands in EC2 Server
    if (usrAtHost != None):
        runCommandInServer(ec2Resource, usrAtHost, terminateAfterExecute=True)
