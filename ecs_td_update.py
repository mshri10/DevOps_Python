import boto3
import sys


#         Usage
# run python update_ecs.py td_name cluster_name int
# Example : python update_ecs.py rhino cluster_name desired_count


# profile name for sandbox from ~/.aws/config
try:
    session = boto3.session.Session(profile_name='ecs_prod',region_name='us-west-2')
    ecs_client = session.client('ecs')
except Exception as e:
    print e

def get_latest_td():
    '''
    Finds the latest TD ARN
    '''
    try:
        latest_td = sys.argv[1]
        desc_td =  ecs_client.list_task_definitions(
                    familyPrefix = latest_td,
                    status = 'ACTIVE',
                    maxResults= 100
                    )['taskDefinitionArns']
        td_index = len(desc_td) -1
        print "New TD ARN is {}".format(desc_td[td_index])
        new_td_arn = desc_td[td_index]
        return new_td_arn
    except Exception as e:
        print e



def update_service(td_arn):
    '''
    Updates the service with the latest ARN and waits for the service to become stable
    '''
    try:
        service = "ecs_service_"+sys.argv[1]
        print service
        ecs_client.update_service(
                cluster = sys.argv[2],
                service = service,
                taskDefinition = td_arn,
                desiredCount = int(sys.argv[3])
                )
        ecs_client.get_waiter('services_stable').wait(
                cluster = sys.argv[2],
                services=[service],
                WaiterConfig={'Delay':15,'MaxAttempts':10}
                )
        print "{} Updated Sueccfully with TD {}".format(service,td_arn)

        with open('updated_services.txt','a') as f:
            f.write("\n"+service + " " + td_arn)

        print "\n Service update is complete "
    except Exception as e:
        print e


def main():
    new_td_arn = get_latest_td()
    update_service(new_td_arn)


if __name__ == "__main__":
    main()
