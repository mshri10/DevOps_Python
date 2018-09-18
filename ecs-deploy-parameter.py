#!/usr/bin/python3
import boto3
import sys

#-----------------------------------------------------------------------
# Description: Script to release latest Kraken service tag to ECS
#
# Usage: python3 ship_kraken.py kraken_image_tag
# Example: python3 ship_kraken.py v1.7.0
#
#-----------------------------------------------------------------------

#session = boto3.session.Session(profile_name='ecs_sbx',region_name='us-west-2')
ecs = boto3.client('ecs',region_name='us-west-2')

#ecs = session.client('ecs')
td_name = 'kraken'
cluster='datapipeline_PROD'
new_image_tag = "ampush/kraken:{}".format(sys.argv[1])


def get_new_container_def():
    """Reads the defifintion from last TD and updates new image tag"""
    try:
        latest_td_def = ecs.describe_task_definition(
           taskDefinition='kraken'
           )['taskDefinition']['containerDefinitions']
        latest_td_def[0]['image'] = new_image_tag
        return latest_td_def
    except Exception as e:
        print(e)

def register_new_td(container_def):
    """Registers a New TD with new image tag"""
    try:
        new_td_arn = ecs.register_task_definition(
                family='kraken',
                containerDefinitions=container_def
                )['taskDefinition']['taskDefinitionArn']
        print('Created new revision of task definition')
        return new_td_arn
    except Exception as e:
        print(e)

def ship_new_image(arn):
    """updates the service with the new TD containing new image tag to be released"""
    try:
        service = 'ecs_service_kraken'
        ecs.update_service(
                cluster=cluster,
                service=service,
                taskDefinition=arn)

        print('Awaiting Service events to report a steady state\
                New tasks may already be running')
        ecs.get_waiter('services_stable').wait(
        #ecs.get_waiter('tasks_running').wait(
                cluster=cluster,
                services=[service],
                #tasks=[arn.split('/')[1]],
                WaiterConfig={'Delay':15,'MaxAttempts':50}
                )
        print('Service has reached a steady state')
        print('\n{} Released Successfully with the New TD {}'.format(service,arn))
    except Exception as e:
        print(e)


def main():
    print('Release Kraken Image.......... {}'.format(new_image_tag))
    user_input = input('\tVerify the above image tag.\n\nAre you sure you wish to continue? [y/N] ')

    if user_input == 'y' or user_input == 'Y':
        print('Deploying new kraken image')
        new_task_def = get_new_container_def()
        new_td_arn=register_new_td(new_task_def)
        ship_new_image(new_td_arn)
    else:
        sys.exit()



if __name__ == "__main__":
    main()





