#!/usr/bin/python
import yaml
import argparse
import sys
import boto3
from prettytable import PrettyTable


def parse_args():
    parser = argparse.ArgumentParser(description="Display Status of various AWS Services")
    parser.add_argument('-env',action='store',required=True,help="Enter the enviroment name from the config.yaml")
    parser.add_argument('-listasg',action='store_true',help="list all asg names")
    parser.add_argument('-asg asg_name',action='store',dest='asg_name',required=False,help="ASG Name to query")
    return parser.parse_args()


args = parse_args()


# Load the config.yaml file
try:
    config = open('config.yaml')
    config = yaml.load(config)
except:
    print "Could not load the config.yaml file"
    sys.exit(2)


# Read the keys for the enviroment as per the -env argument
access_key = config['enviroments'][args.env]['aws_access_key_id']
secret_key = config['enviroments'][args.env]['aws_secret_access_key']


""" Instantiating the boto3 clients """
asg_client = boto3.client('autoscaling',aws_access_key_id=access_key,\
            aws_secret_access_key=secret_key,region_name='us-west-2')
ec2_client = boto3.client('ec2',aws_access_key_id=access_key,\
            aws_secret_access_key=secret_key,region_name='us-west-2')


""" Pretty Table """
x = PrettyTable()

""" function to list all the asg in the enviroment """
def list_asg_names():
    response= asg_client.describe_auto_scaling_groups()

    asg_names = [] # List to hold the asg names
    for i in response['AutoScalingGroups']:
        asg_names.append(i['AutoScalingGroupName'])
    #print the output in the table
    x.add_column("AutoScaling Groups",asg_names)
    print x


""" function to print the asg instances information """
def get_asg_instances_info():
    asg = args.asg_name
    print "\n Fetching data for the ASG Name: {}\n...".format(asg)

    asg_response = asg_client.describe_auto_scaling_groups(AutoScalingGroupNames=[asg])

    instance_ids = [] # List to hold the instance-ids

    for i in asg_response['AutoScalingGroups']:
     for k in i['Instances']:
         instance_ids.append(k['InstanceId'])

    ec2_response = ec2_client.describe_instances(
         InstanceIds = instance_ids
         )

    private_ip = [] # List to hold the Private IP Address

    for instances in ec2_response['Reservations']:
     for ip in instances['Instances']:
         private_ip.append(ip['PrivateIpAddress'])

    #Print the output in the table
    x.add_column("InstanceIds",instance_ids)
    x.add_column("PrivateIPs",private_ip)
    print x




def main():
    if args.env and args.listasg:
        list_asg_names()
    if args.env and args.asg_name:
        get_asg_instances_info()

if __name__ == "__main__":
    main()




