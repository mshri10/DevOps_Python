import boto3

"""Print the list of ASG with Environment tag and value sandbox"""
asg_client = boto3.client('autoscaling','us-west-2')
ec2_client = boto3.client('ec2','us-west-2')
asg_name_dict = {}

def get_list_asg():
    asg_name = []
    paginator = asg_client.get_paginator('describe_auto_scaling_groups')
    page_iterator = paginator.paginate(PaginationConfig={'PageSize': 100})
    print page_iterator


    filtered_asgs = page_iterator.search(
            'AutoScalingGroups[] | [?contains(Tags[?Key==`{}`].Value, `{}`)]'.format('Environment', 'sandbox')
            )

    for asg in filtered_asgs:
     asg_name_dict[asg['AutoScalingGroupName']] = asg_name


#-----------------------------------------

def get_instance_list():
    instanceids=[]
    for asg_name in asg_name_dict.items():
#        for i in asg_name['AutoScalingGroups']:
#            for k in i['Instances']:
#                instanceids.append(k['InstanceId'])
        print asg_name
#    print instance_ids

def main():
    get_list_asg()
    get_instance_list()

if __name__ == "__main__":
    main()
