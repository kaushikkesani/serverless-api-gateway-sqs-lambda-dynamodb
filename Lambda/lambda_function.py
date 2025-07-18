from __future__ import print_function
import boto3
import json

print('Loading function')

dynamodb = boto3.resource('dynamodb')

def lambda_handler(event, context):
    # Check if triggered by SQS (contains "Records")
    if "Records" in event:
        for record in event['Records']:
            process_message(record['body'])
        return {'statusCode': 200, 'body': 'Processed messages from SQS'}

    # Otherwise, handle as direct invocation (for testing)
    else:
        process_message(json.dumps(event))
        return {'statusCode': 200, 'body': 'Processed single event'}

def process_message(body_str):
    try:
        message = json.loads(body_str)
    except Exception as e:
        print(f"Error parsing message body: {e}")
        return

    operation = message.get('operation')
    table_name = message.get('tableName')
    payload = message.get('payload', {})

    if not table_name:
        print("No tableName provided in message.")
        return

    table = dynamodb.Table(table_name)

    # Supported operations
    if operation == 'create':
        table.put_item(**payload)
        print("Created item.")
    elif operation == 'read':
        response = table.get_item(**payload)
        print(f"Read item: {response}")
    elif operation == 'update':
        table.update_item(**payload)
        print("Updated item.")
    elif operation == 'delete':
        table.delete_item(**payload)
        print("Deleted item.")
    elif operation == 'list':
        response = table.scan(**payload)
        print(f"Scanned items: {response}")
    elif operation == 'echo':
        print(f"Echo: {payload}")
    elif operation == 'ping':
        print("Pong")
    else:
        print(f"Unrecognized operation: {operation}")
