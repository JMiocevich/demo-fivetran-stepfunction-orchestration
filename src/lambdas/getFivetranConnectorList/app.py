import json
import requests
import boto3
from botocore.exceptions import ClientError


def lambda_handler(event, context):

    group_id = event['group_id']
    
    json_return = getConnectorList(group_id)

    return json_return

def getConnectorList(group_id): 
    FivetranKey=get_secret('FivetranKey')
    FivetranSecret=get_secret('FivetranSecret')
    
    url = "https://api.fivetran.com/v1/groups/" + group_id + "/connectors"

    query = {
    "cursor": "string",
    "limit": "0"
    }

    headers = {"Accept": "application/json"}

    response = requests.get(url, headers=headers, auth=(FivetranKey,FivetranSecret))

    data = response.json()
    print(data)
    print(data['data']['items'])

    connectors_list=[]
    for x in data['data']['items']:
        connectors_list.append(x['id'])

    json_return= {
        'group_id': group_id,
        'connectors_list': connectors_list
    }



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