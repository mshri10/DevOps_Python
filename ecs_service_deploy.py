#!/usr/local/bin/python3
import boto3
import csv
session = boto3.session.Session(aws_access_key_id='',
                                aws_secret_access_key='',region_name='us-west-2')

ecs = session.client('ecs')

def get_new_container_def(service):
    """Reads the defifintion from last TD and updates new image tag"""
    try:
        latest_td_def = ecs.describe_task_definition(
           taskDefinition=service
           )['taskDefinition']['containerDefinitions']
        latest_td_arn = ecs.describe_task_definition(
            taskDefinition=service
        )['taskDefinition']['taskDefinitionArn']
        return latest_td_def, latest_td_arn
    except Exception as e:
        print(e)

def replace_image(latest_td_def, new_image_tag):
    """Reads the defifintion from last TD and updates new image tag"""
    try:
        latest_td_def[0]['image'] = new_image_tag
        return latest_td_def
    except Exception as e:
        print(e)

def register_new_td(container_def, service):
    """Registers a New TD with new image tag"""
    try:
        new_td_arn = ecs.register_task_definition(
                family=service,
                containerDefinitions=container_def
                )['taskDefinition']['taskDefinitionArn']
        print('Created new revision of task definition')
        return new_td_arn
    except Exception as e:
        print(e)

def ship_new_image(arn, service , cluster, desired_count):
    """updates the service with the new TD containing new image tag to be released"""
    try:
        service = 'ecs_service_'+service
        ecs.update_service(
                cluster=cluster,
                service=service,
                desiredCount=desired_count,
                taskDefinition=arn)

        print('Awaiting Service events to report a steady state')
        ecs.get_waiter('services_stable').wait(
                cluster=cluster,
                services=[service],
                WaiterConfig={'Delay':15,'MaxAttempts':50}
                )
        print('\n{} Released Successfully with the New TD {}'.format(service,arn))
    except Exception as e:
        print(e)

#This requires a input csv file as per the mentioned colume.
def main():
        with open('circle_ci_tools/ecs_config.csv') as csvDataFile:
            csvReader = csv.reader(csvDataFile)
            for row in csvReader:
                cluster = row[0]
                service= row[1]
                tag= row[2]
                desired_count=row[3]
                new_image_tag = "ampush/{}:{}".format(service, tag)
                existing_task_def, existing_arn = get_new_container_def(service)
                if existing_task_def[0]['image'] != new_image_tag:
                    new_task_def = replace_image(existing_task_def, new_image_tag)
                    new_td_arn=register_new_td(new_task_def, service)
                else:
                    new_td_arn= existing_arn
                ship_new_image(new_td_arn, service, cluster, int(desired_count))
        print('done')

if __name__ == "__main__":
    main()

#automateGAFilecheck
