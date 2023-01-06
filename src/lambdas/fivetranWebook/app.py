import json
import boto3


def lambda_handler(event, context):

    print(event)
    # This is to deal with fivetrans test run webhook which dosnt match the format of actual data 
    if "data" not in event['body']:
        return {     
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda! Real Test')}
    


    body=json.loads(event['body'])
    connector_id = body['connector_id']
    status=body['data']['status']

    print(connector_id)
    print(status)

    # Get the token from the dynamoDB table
    token = getWaitToken(connector_id)

    # Condtional Logic to send success or failure to step function
    client_stepfunction = boto3.client('stepfunctions')

    if status == 'SUCCESSFUL':
        resp= client_stepfunction.send_task_success(taskToken=token,output='{}')
        print('success')
        print(resp)
    else:
        print('error')
        resp = client_stepfunction.send_task_failure(taskToken=token)
        print(resp)

 

def getWaitToken(connector_id):
    client = boto3.resource('dynamodb')
    table = client.Table("stateTokenTable")
    response = table.get_item(
    Key={
        'id': connector_id
    }
    )       
    token = response['Item']['MyTaskToken']
    return token

