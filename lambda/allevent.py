import json, boto3, os
from boto3.dynamodb.conditions import Key

# set environment variable
TABLE_NAME = os.environ['TABLE_NAME']

def handler(event, context):
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table(TABLE_NAME)
    response = table.scan()
    
    
    return {
        'statusCode': 200,
        'body': json.dumps(response['Items'])
    }
