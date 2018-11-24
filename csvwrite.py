#!/usr/bin/python
import boto3
import csv

client_ec2 = boto3.client('ec2',region_name='us-west-2')

response = client_ec2.describe_snapshots(
            OwnerIds=['213868388452']
            )

with open('snapshot_list.csv', 'w') as csvfile:
    writer = csv.writer(csvfile,delimiter=',')
    writer.writerow( ['SnapshotId',
                        'StartTime',
                        'VolumeId',
                        'VolumeSize'])
    print ("Writing to CSV")
    for i in response["Snapshots"]:
        SnapshotId = i["SnapshotId"]
        StartTime = i["StartTime"]
        VolumeId = i["VolumeId"]
        VolumeSize = i["VolumeSize"]
        writer.writerow([SnapshotId,
                         StartTime,
                         VolumeId,
                         VolumeSize,])
