import boto3
from datetime import datetime
from botocore.exceptions import ClientError
import httplib,json

dont_shut_down_date = datetime.utcnow().strftime('%Y%m%d')

print dont_shut_down_date

ec2_client=boto3.client('ec2')
instance_name_string ="QA*" #Instance name starting with the string instance
instance_ids = []

def get_instances():
    instance_ids=[]
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


    except Exception as e:
        print e

    return instance_ids

def clean_up_tags():
    instance_ids = get_instances()
    try:
      ec2_client.create_tags(
          Resources = instance_ids,
          Tags = [
              {
                  'Key':'daily_instance_shutdown_lambda',
                  'Value': "Yes"
                }
            ]
        )
    except Exception as e:
        print e

def instance_instance_stop():
    try:
        clean_up_tags()
        instance_ids=[]
        response  = ec2_client.describe_instances(
            Filters= [{
                'Name' :'tag:Name',
                'Values':[instance_name_string]
                },
                {'Name': 'instance-state-name', 'Values': ['running']}
            ]
        )
        for reservation in response["Reservations"]:
          for instance in reservation["Instances"]:
            instance_ids.append(instance["InstanceId"])

        print "instances Ids from if instancestop {}".format(instance_ids)

        if len(instance_ids) == 0:
            clean_up_tags()
            print "Instances are already in a `stopped` state !"
            return "Instances are already in a `stopped` state !"
        else:
            ec2_client.stop_instances(
                InstanceIds=instance_ids
            )

#            stoppedWaiter = ec2_client.get_waiter('instance_stopped')
#            stoppedWaiter.wait(
#                InstanceIds=instance_ids,
#                WaiterConfig={
#                    'Delay': 5,
#                    'MaxAttempts': 30
#                }
#            )
            print "Following instances stopped ".format(instance_ids)
            return instance_ids
    except ClientError as e:
        print e


def instance_tagger():
    instance_ids = get_instances()
    try:
        ec2_client.create_tags(
                Resources=  instance_ids,
                Tags=[
                    {
                        'Key':'daily_instance_shutdown_lambda',
                        'Value':dont_shut_down_date
                        }
                    ]
                )
    except Exception as e:
        print e

    return instance_ids

def instance_instance_start():
    instance_ids = get_instances()
    try:
        ec2_client.start_instances(
                        InstanceIds=instance_ids
                        )
        print "Starting the the instances !"
        #using get_waiter() below to verify the instances are in the running state
#        startedWaiter = ec2_client.get_waiter('instance_running')
#        startedWaiter.wait(InstanceIds=instance_ids)

    except ClientError as e:
        print e
    return instance_ids

def lambda_handler(event, context):
   output=""
   whattodo=event['whattodo']

   if whattodo == "donotstop":
       output = instance_tagger()
       return {
           "attachments": [
               {

                   "text": str(output),
                   "title": "QA instances will not be stopped today"
                  }
                ]
        }
   if whattodo == "stop":
       output = instance_instance_stop()
       return {
           "attachments": [
               {
                   "text": str(output),
                   "title": "QA instances stopped",
                   "color": '#FF0000'
                  }
                ]
        }
   if whattodo == "start":
       output = instance_instance_start()
       print "Starting instance"
       return {
           "attachments": [
               {
                   "text": str(output),
                   "title": "QA instances started",
                   "color": '#00FF00'
                  }
                ]
        }


