#!/usr/bin/python

#---------------------------------------------------------------------------------
# Description
# Script to stop the Instances and send an alert to Slack Channel
#-----------------------------------------------------------------------------------
import boto3
from botocore.exceptions import ClientError
import httplib,json

session = boto3.session.Session(profile_name='dev')
client_ec2 = session.client('ec2',region_name='us-west-2')
# Put Instance Ids
Instance_Ids = ['i-96a','i-09ce9','i-04e1']

slack_webhook_url = 'https://hooks.slack.com/services/T123422c1h'
stop_color = '#FF0000'
alert_icon ='https://www.cloudera.com/content/dam/www/Downloads/Product%20Icons/xManager_Icon.png.pagespeed.ic.p93WiflsDG.png'

def slack_alert(webhook,color,ids):
      WEBHOOK_URL = webhook
      headers = {'Content-Type': 'application/json'}
      text= "CDH Instances have been Stopped"
      message = {
              'username' : 'DEV server Shutdown',
              'channel'  : '#support',
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

def cdh_instance_stop():
    try:
        client_ec2.stop_instances(
                        InstanceIds=Instance_Ids
                        )
        print "Stopping the instances !"
        #using get_waiter() below to verify the instances are in the stopped state
        stoppedWaiter = client_ec2.get_waiter('instance_stopped')
        stoppedWaiter.wait(InstanceIds=Instance_Ids)
        # Sends the slack alert when the instance state is 'stopped'
        slack_alert(slack_webhook_url,stop_color,','.join(map(str,Instance_Ids)))
    except ClientError as e:
        print e


def main():
    cdh_instance_stop()


if __name__ == "__main__":
    main()
