import json
import boto3
import time
 
def lambda_handler(event, context):
    
    client = boto3.client('sagemaker')
 
    #change the name of the targeted instance to start by modifying 'instance-name'
    instanceName = 'instance-name'
 
    status = client.describe_notebook_instance(NotebookInstanceName=instanceName).get('NotebookInstanceStatus')
    print('Notebook Instance Status = ', status)
 
    #check if the SageMaker notebook instance had been stopped.
    while status != 'Stopped':
        if status == 'InService':
            client.stop_notebook_instance(NotebookInstanceName=instanceName)
            print('SageMaker notebook instance was not stopped. Now stopping it.')
            time.sleep(60)
        elif status == 'Stopping':
            print('SageMaker notebook instance is still being stopped. Check the status again after 15 seconds.')
            time.sleep(15)
        elif status == 'Pending':
            return {
                'statusCode': 200,
                'body': json.dumps('SageMaker notebook instance is already being started.')
            }
            break
        elif status == 'Failed':
            return {
                'statusCode': 200,
                'body': json.dumps('SageMaker notebook instance is in failed state. No action will be taken from this run.')
            }
            break
        status = client.describe_notebook_instance(NotebookInstanceName=instanceName).get('NotebookInstanceStatus')
    else:
        #start the SageMaker Notebook instance that will trigger the lifecycle policy to execute the notebook.
        client.start_notebook_instance(NotebookInstanceName=instanceName)
        print('Starting instance...')
        return {
            'statusCode': 200,
            'body': json.dumps('SageMaker notebook instance is starting.')
        }
