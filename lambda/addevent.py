import json, boto3, os
from boto3.dynamodb.conditions import Key

TABLE_NAME = os.environ['TABLE_NAME']

def handler(event, context):
    dynamodb = boto3.resource('dynamodb')
    event_in_bytestream = event['queryStringParameters']['event']
    reader = event['queryStringParameters']['id']
    table = dynamodb.Table(TABLE_NAME)
    response = table.put_item(
        Item={
            'reader': reader,
            'event': event_in_bytestream
        }
    )
    return {
        'statusCode': 200,
        'body': json.dumps(response)
    }
