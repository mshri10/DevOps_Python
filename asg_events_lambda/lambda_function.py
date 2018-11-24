import json
import urllib2

#                                Description
#--------------------------------------------------------------------------------------------------
# This lambda function will pusblish the cloudwatch Rule: CloudwatchASGEvents subscribed to the
# SNS topic named :Cloudwatch_ASG_Events to slack channel #prod_alerts .
# This will help us be notified of any instance terminations/status failed events  in ASGs.
#------------------------------------------------------------------------------------------------------

def lambda_handler(event, context):

    # Usage: Replace SLACK_KEY_HERE with a valid slack api key (webhook)
    status_alerts_channel =  'https://hooks.slack.com/services/SLACK_KEY_HERE'
    results = []

    full_message = event['Records'][0]['Sns']['Message']
    data = json.loads(full_message)
    asg = data['detail']['AutoScalingGroupName']
    desc = data['detail']['Description']
    cause = data['detail']['Cause']

    message = {
            'text': '<!channel> \n *AutoScalingGroupName*: `{}`\
                    \n *Description*: `{}`\n *Cause*: `{}`'.format(asg,desc,cause),
            'username': 'ASG CloudWatch Events !',
            'channel': '#SLACK_CHANNEL_NAME',
            'icon_emoji': ':warning:',
             'mrkdwn': True,
             'short' : True
    }
    data = json.dumps(message)

    req = urllib2.Request(status_alerts_channel, data)
    response = urllib2.urlopen(req)
    results.append(response.read())


    return results






