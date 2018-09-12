import boto3
from datetime import datetime

#aws cli profile name for sandbox
profile_name = 'sandbox'
session = boto3.session.Session(profile_name=profile_name,region_name='us-west-2')
ec2_client = session.client('ec2')
dont_shut_down_date = datetime.utcnow().strftime('%Y%m%d')

print dont_shut_down_date #current UTC date when u dont want to shutdown Ec2

instance_name_string ="tag_name*" #Instance name starting with the string tag_name
instance_ids = []

def get_instances():
    try:
        response = ec2_client.describe_instances(
                Filters=[
                    {
                    'Name':'tag:Name',
                    'Values':[instance_name_string]
                    }
                ]
                )
        for reservation in response["Reservations"]:
            for instance in reservation["Instances"]:
                instance_ids.append(instance["InstanceId"])

        print "Following instances will not be stoppped today\n{}".format(instance_ids)
    except Exception as e:
        print e

def instance_tagger():
    try:
        ec2_client.create_tags(
                Resources=  instance_ids,
                Tags=[
                    {
                        'Key':'daily_cdh_shutdown_lambda',
                        'Value':dont_shut_down_date
                        }
                    ]
                )
    except Exception as e:
        print e


def main():
    get_instances()
    instance_tagger()



if __name__ == "__main__":
    main()



