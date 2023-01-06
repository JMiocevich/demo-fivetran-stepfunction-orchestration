import json
import requests
import boto3
from botocore.exceptions import ClientError
import base64
import os
import tempfile




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





SnowflakePrivateKeyB64=get_secret('SnowflakePrivateKey')


secret_file = "rsa_key.p8"
encoded_bytes = base64.b64decode(SnowflakePrivateKeyB64)

with open(secret_file, 'wb+') as f:
    f.write(encoded_bytes)


