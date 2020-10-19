import json, boto3, os
from boto3.dynamodb.conditions import Key

TABLE_NAME = os.environ['TABLE_NAME']

def handler(event, context):
    dynamodb = boto3.resource('dynamodb')
    event_id = event['queryStringParameters']['id']
    table = dynamodb.Table(TABLE_NAME)
    response = table.query(
        KeyConditionExpression=Key('id').eq(event_id)
    )
    
    return {
        'statusCode': 200,
        'body': json.dumps(response['Items'])
    }
