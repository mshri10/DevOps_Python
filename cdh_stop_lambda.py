#!/usr/bin/python

#---------------------------------------------------------------------------------
# Description
# Lambda to stop the QA instance Instances and send an alert to cyb-support channel
#-----------------------------------------------------------------------------------
import boto3
from botocore.exceptions import ClientError
import httplib,json
from datetime import datetime
"""
session = boto3.session.Session(profile_name='QA')
client_ec2 = session.client('ec2',region_name='us-west-2')
resource_ec2 = session.resource('ec2',region_name='us-west-2')
"""
client_ec2 = boto3.client('ec2')
resource_ec2 = boto3.resource('ec2')

instance_ids =[] #list to hold the instance ids
instance_name_string = "instance*"
today = datetime.utcnow().strftime('%Y%m%d')
slack_channel =  '#support'
slack_message = {"Message": ""}

slack_webhook_url = 'https://hooks.slack.com/services/TJp2c1h'
stop_color = '#FF0000'
alert_icon ='https://www.cloudera.com/content/dam/www/Downloads/Product%20Icons/xManager_Icon.png.pagespeed.ic.p93WiflsDG.png'

def slack_alert(webhook,color,ids):
      WEBHOOK_URL = webhook
      headers = {'Content-Type': 'application/json'}
      text= "QA instance Shutdown Lambda ! \n{} ".format(slack_message["Message"])
      message = {
              'username' : 'Daily QA instance Shutdown',
              'channel'  : slack_channel,
              'fallback' : text,
              'pretext'  : text,
              'color'    : stop_color,
              'icon_url' : alert_icon,
              'fields'   : [

                   {
                      'title' : "Intance-Ids:",
                      'value' : ids,
                      'short' : True
                      }
                  ]
              }
      connection = httplib.HTTPSConnection('hooks.slack.com')
      connection.request('POST',WEBHOOK_URL, json.dumps(message), headers)
      print json.dumps(message)
      response = connection.getresponse()
      print response.read().decode()


def clean_up_tags():
  """
  Function to update the tags of the instance Instances
  """
  try:
    client_ec2.create_tags(

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
      slack_message["Message"]=e

def get_instances_tag_value(tag,value):
    try:
        instances = resource_ec2.instances.filter(
                Filters=[{
                    'Name':'tag:'+tag,
                    'Values':[value]
                    }]
                )
        for instance in instances:
            instance_ids.append(instance.id)
        if len(instance_ids) == 0:
            print "running instance stop function"
            instance_instance_stop()
        else:
          slack_message["Message"] = "instance Instances will `not` be stopped today: {}".format(today)
          print "running cleanup tags"
          clean_up_tags()
          #slack_alert(slack_webhook_url,stop_color,','.join(map(str,instance_ids)))
    except Exception as e:
        print e
        slack_message["Message"]=e


def instance_instance_stop():
    try:
        response  = client_ec2.describe_instances(
                    Filters= [{
                                    'Name' :'tag:Name',
                                    'Values':[instance_name_string]
                                },
                                {
                                    'Name':'instance-state-name',
                                    'Values':['running']
                                    }
                                ])

        for reservation in response["Reservations"]:
          for instance in reservation["Instances"]:
            instance_ids.append(instance["InstanceId"])
        print "instances Ids from if instancestop {}".format(instance_ids)
        if len(instance_ids) == 0:
            print "running cleanup inside instance_stop"
            clean_up_tags()
            slack_message["Message"] = "Instances are already in a `stopped` state !"
        else:
            client_ec2.stop_instances(
                        InstanceIds=instance_ids
                        )
            print "Stopping the instances !"
            #using get_waiter() below to verify the instances are in the stopped state
            stoppedWaiter = client_ec2.get_waiter('instance_stopped')
            stoppedWaiter.wait(
                  InstanceIds=instance_ids,
                  WaiterConfig={
                      'Delay': 5,
                      'MaxAttempts': 30
                  }

                  )
            # Sends the slack alert when the instance state is 'stopped'
            slack_message["Message"] = "Instances have been stopped successfully!"
            #slack_alert(slack_webhook_url,stop_color,','.join(map(str,instance_ids)))
    except ClientError as e:
        print e
        slack_message["Message"]=e

def lambda_handler(event,context):
    """
    main function
    """
    get_instances_tag_value('daily_instance_shutdown_lambda',today)
    slack_alert(slack_webhook_url,stop_color,','.join(map(str,set(instance_ids))))



