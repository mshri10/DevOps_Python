#!/usr/bin/python

#---------------------------------------------------------------------------------
# Description
# Script to start the Instances and send an alert to cyb-support channel
#-----------------------------------------------------------------------------------
import boto3
from botocore.exceptions import ClientError
import httplib,json

session = boto3.session.Session(profile_name='user')
client_ec2 = session.client('ec2',region_name='us-west-2')
# Put Instance Ids
Instance_Ids = ['i-6a','i-ce9','i-034e1']

# Add slack webhook
slack_webhook_url = 'https://hooks.slack.com/services/T123131h'
start_color = '#00FF00'
alert_icon ='https://www.cloudera.com/content/dam/www/Downloads/Product%20Icons/xManager_Icon.png.pagespeed.ic.p93WiflsDG.png'

def slack_alert(webhook,color,ids):
      WEBHOOK_URL = webhook
      headers = {'Content-Type': 'application/json'}
      text= "CDH Instances have been Started"
      message = {
              'username' : 'Dev Server Started',
              'channel'  : '#support',
              'fallback' : text,
              'pretext'  : text,
              'color'    : start_color,
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

def cdh_instance_start():
    try:
        client_ec2.start_instances(
                        InstanceIds=Instance_Ids
                        )
        print "Starting the the instances !"
        #using get_waiter() below to verify the instances are in the running state
        startedWaiter = client_ec2.get_waiter('instance_running')
        startedWaiter.wait(InstanceIds=Instance_Ids)
        # Sends the slack alert when the instance state is 'running'
        slack_alert(slack_webhook_url,start_color,','.join(map(str,Instance_Ids)))
    except ClientError as e:
        print e


def main():
    cdh_instance_start()


if __name__ == "__main__":
    main()
