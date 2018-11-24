#AWS Health Events Notifier Lambda  CrossAccount/Region Setup.

This lambda functions sends out alerts to the slack #channel_name channel for ![AWS Health Events](https://docs.aws.amazon.com/health/latest/ug/cloudwatch-events-health.html) . The fucntion is Invoked by the Cloudwatch Health Event Rules targeted to a SNS topic in 
the aws account.s