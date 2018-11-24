import json
import urllib2
import os


def lambda_handler(event, context):
    webhook =  os.environ['slack_webhok_url']
    channel =  os.environ['slack_channel_name']
    results = []

    aws_account = {
                   'Prod3.0': "682514645333",
                   'devops':"195150329923",
                   "sandbox": "413985601798",
                   "fullfunnel": "410844597293",
                   "Amp2.5": "213868388452"
                  }
    account_name = aws_account.keys()[aws_account.values().index(str(event['account']))]
    region = str(event['region'])
    starttime = str(event['detail']['startTime'])
    typecode = str(event['detail']['eventTypeCode'])
    resources = str(event['resources'])
    service = str(event['detail']['service'])
    descripton = str(event['detail']['eventDescription'][0]['latestDescription'])
    message = {
           'text': '{}\n *Account* {}\n *Region* {}\t\t *Starts* {}\n*Event* {}'.format(descripton,account_name,region,starttime,typecode),
            'username': 'AWS Health Event!',
            'channel': channel ,
            'icon_emoji': ':meeseeks:',
             'mrkdwn': True,
             'color': '#FF6600',
             #'short' : True
             'fields' : [

               {

                'title': '*Resources*\t\t *Service*',
                'value':  "{}\t\t{}".format(resources,service),
                'short': True
               }

              ]
    }
    data = json.dumps(message)

    req = urllib2.Request(webhook, data)
    response = urllib2.urlopen(req)
    results.append(response.read())


    return results
