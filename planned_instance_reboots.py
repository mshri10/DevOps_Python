import boto3
import csv

client_ec2 = boto3.client('ec2',region_name='us-west-2')

instance_ids = [
    "i-c04b1dsf",
    "i-bac2124c",
    "i-a56ec66g",
    "i-99b9d4f8",
    "i-763c379f",
    "i-6cac163d",
    "i-5b86ff9d",
    "i-3sa9f9e6",
    "i-2d3c329h",
    "i-2ddeefe4",
    "i-3fgg2ae2"
    ]


response = client_ec2.describe_instances(
            InstanceIds=instance_ids
            )
#print response

def planned_instances():
    with open('planned_instances.csv','wb') as csvfile:
        writer = csv.writer(csvfile,delimiter=',')
        writer.writerow( ['InstanceId',
                                'Monitoring ',
                                'PublicDnsName ',
                                'PublicIpAddress ',
                                'PrivateIpAddress',
                                'ImageId ',
                                'KeyName ',
                                'InstanceType ',
                                'SecurityGroup',
                                'vols'])
        print "writing data to csv file"
        for reservation in response["Reservations"]:
            for instances in reservation["Instances"]:
               InstanceId =     instances["InstanceId"]
               Monitoring =     instances["Monitoring"]
               PublicDnsName = instances["PublicDnsName"]
               PublicIpAddress = instances["PublicIpAddress"]
               PrivateIpAddress = instances["PrivateIpAddress"]
               ImageId =         instances["ImageId"]
               KeyName =        instances["KeyName"]
               InstanceType =   instances["InstanceType"]
               SecurityGroup = instances["SecurityGroups"]#["GroupId"]
               print "hello"
               for devices in instances["BlockDeviceMappings"]:
                   vols = devices['Ebs']['VolumeId']
                   
               writer.writerow([InstanceId,
                                Monitoring ,
                                PublicDnsName ,
                                PublicIpAddress ,
                                PrivateIpAddress,
                                ImageId ,
                                KeyName ,
                                InstanceType ,
                                SecurityGroup,
                                vols

                                ])

                  # print InstanceId
                  # print Monitoring
                  # print PublicDnsName
                  # print PublicIpAddress
                  # print PrivateIpAddress
                  # print ImageId
                  # print KeyName
                  # print InstanceType
                  # print SecurityGroup
                  # print vols



def main():
    print "hello"
    planned_instances()



if __name__ == "__main__":
    main()
