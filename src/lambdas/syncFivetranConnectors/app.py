import json
import requests
import boto3
from botocore.exceptions import ClientError


def lambda_handler(event, context):


    connector_id = event['connectors_id']
    token= event['MyTaskToken']

    syncFivetranConnector(connector_id)
    storeToken(connector_id,token)


def syncFivetranConnector(connector_id):
    FivetranKey=get_secret('FivetranKey')
    FivetranSecret=get_secret('FivetranSecret')
    
    url = "https://api.fivetran.com/v1/connectors/" + connector_id + "/sync"

    headers = {"Accept": "application/json"}

    response = requests.post(url, headers=headers, auth=(FivetranKey,FivetranSecret))

    data = response.json()
    print(data)

def storeToken(connector_id,token):
    client = boto3.resource('dynamodb')
    table = client.Table("stateTokenTable")
    print(table.table_status)

    table.put_item(Item= {'id': connector_id,'MyTaskToken': token})

def get_secret(secret_name):

    region_name = "ap-southeast-2"

    # Create a Secrets Manager client
    session = boto3.session.Session()
    client = session.client(
        service_name='secretsmanager',
        region_name=region_name
    )

    try:
        get_secret_value_response = client.get_secret_value(
            SecretId=secret_name
        )
    except ClientError as e:
        # For a list of exceptions thrown, see
        # https://docs.aws.amazon.com/secretsmanager/latest/apireference/API_GetSecretValue.html
        raise e

    # Decrypts secret using the associated KMS key.
    secret = get_secret_value_response['SecretString']

    return secret