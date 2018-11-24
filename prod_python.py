import boto3

def get_hosts_from_asg():
    keys = {'access_key':'xxxxxxxxxxxx','secret_key':'xxxxxxxxxxxx'}
    acc_key = keys['access_key']
    sec_key = keys['secret_key']

    """ Instantiating Boto3 Clients """
    ec2_client = boto3.client('ec2',aws_access_key_id=acc_key,aws_secret_access_key=sec_key,region_name='us-west-2')
    asg_client = boto3.client('autoscaling',aws_access_key_id=acc_key,aws_secret_access_key=sec_key,region_name='us-west-2')

    asg =   "asg_name"
    #print asg
    asg_response = asg_client.describe_auto_scaling_groups(AutoScalingGroupNames=[asg])

    instance_ids = [] # List to hold the instance-ids

    for i in asg_response['AutoScalingGroups']:
        for k in i['Instances']:
            instance_ids.append(k['InstanceId'])

    ec2_response = ec2_client.describe_instances(
            InstanceIds = instance_ids
            )
#    print instance_ids #This line will print the instance_ids

    private_ip = [] # List to hold the Private IP Address

    for instances in ec2_response['Reservations']:
        for ip in instances['Instances']:
            private_ip.append(ip['PrivateIpAddress'])


    print '\n'.join(private_ip)




get_hosts_from_asg()
