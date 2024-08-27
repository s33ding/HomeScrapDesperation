import sys
import json
import os
import boto3

def create_boto3_session():
    # Initialize a session using Amazon DynamoDB
    session = boto3.Session()
    return session

session = create_boto3_session()

def create_dynamodb_table(session, table_name, attribute_definitions, key_schema):
    dynamodb = session.client('dynamodb')

    request = {
        "TableName": table_name,
        "KeySchema": key_schema,
        "AttributeDefinitions": attribute_definitions,
        "BillingMode": "PAY_PER_REQUEST"  # Set to on-demand (serverless) mode
    }

    print("Create Table Request:", request)  # Debugging line

    response = dynamodb.create_table(**request)

    return response

session = create_boto3_session()

response = create_dynamodb_table(
    session=session,
    table_name="apt-scrap",
    attribute_definitions=[
        {
            'AttributeName': 'pk',  # Attribute used as HASH key
            'AttributeType': 'S'  # S represents a string data type
        }
        ],
    key_schema=[
        {
            'AttributeName': 'pk',
            'KeyType': 'HASH'  # HASH indicates the partition key
        }
    ]
)

print("Table status:", response['TableDescription']['TableStatus'])

