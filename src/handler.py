import boto3
import os
#import json


def lambda_handler(event, context):
    # the following code is for test purposes only
    # clearly there can be more than 1 records in the event, picked up from SQS
    event_source = event["Records"][0]["eventSource"]
    event_id = event["Records"][0]["messageId"]
    msg = event["Records"][0]["body"]

    tn = os.getenv('ddb_table')

    print(f'lambda_handler: invoked by {event_source}')
    print(f'lambda_handler: event id = {event_id}  body = {msg}')

    # store the incoming event in dynamo
    ddb = boto3.client('dynamodb')
    response = ddb.put_item(TableName=tn, Item={'id': {'S': event_id}, 'msg': {'S': msg}})

    return {"statusCode": 200, "headers": {"Content-Type": "application/json"} }
    # return {
    #     "statusCode": 200,
    #     "headers": {
    #         "Content-Type": "application/json"
    #     },
    #     "body": json.dumps({
    #         "Message ": message
    #     })
    # }

